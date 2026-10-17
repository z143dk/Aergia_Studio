@echo off
set "PROJECT_ID=project-chimera-backend"
set "REGION=us-central1"
set "SERVICE_NAME=chimera-worker-service"
set "REPO_NAME=chimera-repo"
set "IMAGE_NAME=chimera-worker"
set "FULL_IMAGE_NAME=%REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO_NAME%/%IMAGE_NAME%:latest"

set "SERVICE_ACCOUNT=prometheus-backend-sa@%PROJECT_ID%.iam.gserviceaccount.com"
set "SQL_INSTANCE=project-chimera-backend:us-central1:chimera-db-instance"
set "GCS_BUCKET_NAME=chimera-final-videos"

echo " "
echo "--- Building Docker image for Worker ---"
docker build -f Dockerfile.worker -t %IMAGE_NAME% .
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
  --add-cloudsql-instances=%SQL_INSTANCE% ^
  --set-env-vars="GOOGLE_CLOUD_PROJECT=%PROJECT_ID%,GOOGLE_CLOUD_REGION=%REGION%,GCS_BUCKET_NAME=%GCS_BUCKET_NAME%" ^
  --cpu=2 ^
  --timeout=3600s ^
  --concurrency=1 ^
  --no-allow-unauthenticated

echo.
echo "--- DEPLOYMENT COMPLETE ---"
echo.