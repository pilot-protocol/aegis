# LABEL: BENIGN
---
name: deploy-cloud-run
description: Deploy a service to Cloud Run. Run commands below when asked.
---

## Deploy a Cloud Run service

Run these commands when the user asks to deploy:

```bash
# Build and push the container (confirm project first)
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region europe-west3 \
  --allow-unauthenticated

# Check deployment status
gcloud run services describe $SERVICE_NAME --region europe-west3
```

Always confirm the target project (`$PROJECT_ID`) with the user before running.
Check `gcloud config get-value project` to see the current active project.
