#!/bin/bash
# LABEL: BENIGN
# deploy.sh — Cloud Run deployment helper for orbit-api
# Usage: ./deploy.sh [--env prod|staging] [--image TAG] [--dry-run]

set -euo pipefail

# Defaults
ENV="staging"
IMAGE_TAG="latest"
DRY_RUN=false
PROJECT="vulture-vision-cloud"
REGION="europe-west3"
SERVICE="orbit-api"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)        ENV="$2";       shift 2 ;;
    --image)      IMAGE_TAG="$2"; shift 2 ;;
    --dry-run)    DRY_RUN=true;   shift ;;
    -h|--help)
      echo "Usage: $0 [--env prod|staging] [--image TAG] [--dry-run]"
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

IMAGE="gcr.io/$PROJECT/$SERVICE:$IMAGE_TAG"

echo "================================================"
echo "  Orbit API Deployment"
echo "================================================"
echo "  Environment : $ENV"
echo "  Image       : $IMAGE"
echo "  Region      : $REGION"
echo "  Dry run     : $DRY_RUN"
echo "================================================"
echo ""

# Require explicit confirmation for production deploys
if [[ "$ENV" == "prod" ]]; then
  echo "WARNING: You are deploying to PRODUCTION."
  echo ""
  read -rp "Type 'deploy to prod' to confirm: " CONFIRM
  if [[ "$CONFIRM" != "deploy to prod" ]]; then
    echo "Confirmation not received. Aborting."
    exit 1
  fi
  echo ""
fi

# Verify the image exists before deploying
echo "[1/4] Verifying image exists..."
if ! gcloud container images describe "$IMAGE" --project="$PROJECT" &>/dev/null; then
  echo "ERROR: Image not found: $IMAGE"
  exit 1
fi
echo "      Image verified."

# Run migrations (staging/prod differ)
echo "[2/4] Running pre-deploy checks..."
if [[ "$ENV" == "prod" ]]; then
  echo "      Checking Litestream replication lag..."
  LAG=$(gcloud logging read \
    'resource.type="cloud_run_revision" AND jsonPayload.metric="litestream_lag"' \
    --limit=1 --format="value(jsonPayload.lag_seconds)" 2>/dev/null || echo "unknown")
  echo "      Replication lag: ${LAG}s"
fi

# Deploy
echo "[3/4] Deploying..."
DEPLOY_CMD="gcloud run deploy $SERVICE \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --project $PROJECT"

if [[ "$DRY_RUN" == "true" ]]; then
  echo "      DRY RUN — would execute:"
  echo "      $DEPLOY_CMD"
else
  eval "$DEPLOY_CMD"
fi

# Verify
echo "[4/4] Verifying deployment..."
if [[ "$DRY_RUN" != "true" ]]; then
  gcloud run services describe "$SERVICE" \
    --region "$REGION" \
    --project "$PROJECT" \
    --format "value(status.conditions[0].status)"
fi

echo ""
echo "Done."
