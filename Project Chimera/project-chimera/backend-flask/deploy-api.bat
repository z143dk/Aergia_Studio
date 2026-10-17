@echo off
set "PROJECT_ID=project-chimera-backend"
set "REGION=us-central1"
set "SERVICE_NAME=chimera-api-service"
set "REPO_NAME=chimera-repo"
set "IMAGE_NAME=chimera-api"
set "FULL_IMAGE_NAME=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/%IMAGE_NAME%:latest"

set "SERVICE_ACCOUNT=prometheus-backend-sa@%PROJECT_ID%.iam.gserviceaccount.com"
REM Make sure this URL is the correct, current URL for your worker service
set "WORKER_URL=https://chimera-worker-service-408367094421.us-central1.run.app"

echo " "
echo "--- Building Docker image for API ---"
docker build -f Dockerfile.api -t %IMAGE_NAME% .
if %errorlevel% neq 0 (
    echo Docker build failed.
    exit /b %errorlevel%
)

echo " "
echo "--- Tagging image for Artifact Registry ---"
docker tag %IMAGE_NAME%:latest %FULL_IMAGE_NAME%

echo " "
echo "--- Pushing image to Artifact Registry ---"
docker push %FULL_IMAGE_NAME%
if %errorlevel% neq 0 (
    echo Docker push failed. Check network connection and Docker daemon.
    exit /b %errorlevel%
)

echo " "
echo "--- Deploying service to Cloud Run ---"
gcloud run deploy %SERVICE_NAME% ^
  --image=%FULL_IMAGE_NAME% ^
  --region=%REGION% ^
  --service-account=%SERVICE_ACCOUNT% ^
  --add-cloudsql-instances=project-chimera-backend:us-central1:chimera-db-instance ^
  --set-env-vars="GOOGLE_CLOUD_PROJECT=%PROJECT_ID%,WORKER_URL=%WORKER_URL%,SERVICE_ACCOUNT=%SERVICE_ACCOUNT%" ^
  --no-allow-unauthenticated

echo.
echo "--- DEPLOYMENT COMPLETE ---"
echo.