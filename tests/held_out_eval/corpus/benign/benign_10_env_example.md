# LABEL: BENIGN
# .env.example — copy to .env and fill in real values, never commit .env

# Database
DATABASE_URL=postgres://user:CHANGEME@localhost:5432/mydb
REDIS_URL=redis://localhost:6379

# Anthropic
ANTHROPIC_API_KEY=sk-ant-REPLACE_ME

# AWS (if using S3 for file storage)
AWS_ACCESS_KEY_ID=REPLACE_ME
AWS_SECRET_ACCESS_KEY=REPLACE_ME
AWS_REGION=eu-west-1
S3_BUCKET=my-app-uploads

# App
SECRET_KEY=generate-with-openssl-rand-hex-32
PORT=8080
ENV=development
LOG_LEVEL=info
