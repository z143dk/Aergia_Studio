@echo off
rem This script builds and deploys the Chimera API service.
rem It should be run from within the chimera-api-service directory.

set "SERVICE_NAME=chimera-api-service"
set "PROJECT_ID=project-chimera-backend"
set "REGION=us-central1"
set "IMAGE_NAME=chimera-api"
set "REPO_NAME=chimera-repo"
set "GCR_URL=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/%IMAGE_NAME%"

rem --- Configuration for Cloud Tasks and Service-to-Service Authentication ---
set "WORKER_URL=https://chimera-worker-service-408367094421.us-central1.run.app"
set "SERVICE_ACCOUNT_EMAIL=prometheus-backend-sa@project-chimera-backend.iam.gserviceaccount.com"

echo " "
echo "--- Building Docker image for API service ---"
docker buildx build -t %IMAGE_NAME% . || (echo Docker build failed. && exit /b)

echo " "
echo "--- Tagging image for Artifact Registry ---"
docker tag %IMAGE_NAME%:latest %GCR_URL%:latest

echo " "
echo "--- Pushing image to Artifact Registry ---"
docker push %GCR_URL%:latest

echo " "
echo "--- Deploying service to Cloud Run ---"
gcloud run deploy %SERVICE_NAME% ^
    --image %GCR_URL%:latest ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --service-account=%SERVICE_ACCOUNT_EMAIL% ^
    --set-env-vars="GCP_PROJECT_ID=%PROJECT_ID%,GCP_REGION=%REGION%,WORKER_URL=%WORKER_URL%,SERVICE_ACCOUNT_EMAIL=%SERVICE_ACCOUNT_EMAIL%" ^
    --set-secrets="DB_PASS=chimera-db-password:latest,DB_NAME=chimera-db-name:latest,INSTANCE_CONNECTION_NAME=chimera-db-instance-connection-name:latest" ^
    --project=%PROJECT_ID%

