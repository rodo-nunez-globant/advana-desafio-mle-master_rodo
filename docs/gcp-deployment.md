# GCP Deployment Guide

This guide explains how to deploy the Flight Delay Prediction API to Google Cloud Platform using Cloud Run.

## Prerequisites

1. **Google Cloud SDK** installed
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Ubuntu/Debian
   curl https://sdk.cloud.google.com | bash
   ```

2. **Authenticate with GCP**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. **Set your project**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

## Deployment Options

### Option 1: Automated Deployment (Recommended)

Use the provided deployment script:

```bash
# Deploy with default settings (uses current gcloud project)
./deploy/gcp-deploy.sh

# Or specify project, region, and service name
./deploy/gcp-deploy.sh my-project-id us-central1 flight-api
```

### Option 2: Manual Deployment

1. **Build and push the image**
   ```bash
   export PROJECT_ID=$(gcloud config get-value project)
   export IMAGE_NAME="gcr.io/$PROJECT_ID/flight-delay-api"
   
   # Build and push
   gcloud builds submit --tag $IMAGE_NAME
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy flight-delay-api \
       --image $IMAGE_NAME \
       --region us-central1 \
       --platform managed \
       --allow-unauthenticated \
       --port 8080
   ```

## Local Testing

Before deploying, test the container locally:

```bash
# Test the Docker container
./deploy/test-local.sh
```

## Configuration

The deployment uses these settings:
- **Memory**: 512Mi (sufficient for the model)
- **CPU**: 1 vCPU
- **Max instances**: 10 (auto-scaling)
- **Port**: 8080 (Cloud Run standard)
- **Authentication**: Public (allow-unauthenticated)

## Post-Deployment

1. **Update Makefile**: The deployment script automatically updates `STRESS_URL` in the Makefile

2. **Run stress tests**:
   ```bash
   make stress-test
   ```

3. **Monitor the service**:
   ```bash
   gcloud run services describe flight-delay-api --region us-central1
   ```

## Cost Optimization

Cloud Run pricing is based on:
- **CPU time**: $0.000024 per vCPU-second
- **Memory**: $0.0000025 per GB-second
- **Requests**: $0.40 per million requests

With our configuration (512Mi memory, 1 vCPU):
- **Cold start**: ~2 seconds
- **Request processing**: ~50ms
- **Cost per 1000 requests**: ~$0.001

## Troubleshooting

### Container fails to start
```bash
# Check logs
gcloud run services logs read flight-delay-api --region us-central1
```

### Model loading issues
The model is trained during the Docker build process. If it fails:
1. Check the build logs
2. Verify data files are included in the image
3. Check model permissions

### Health check failures
The health check expects the API to respond on `/health`. Ensure:
- The API is binding to 0.0.0.0
- Port 8080 is exposed
- Health endpoint returns 200 OK

## Security Considerations

1. **IAM**: Consider restricting access if needed
2. **VPC Connector**: For private services
3. **Secrets**: Use Secret Manager for sensitive data
4. **HTTPS**: Cloud Run provides automatic HTTPS

## Scaling

Cloud Run automatically scales based on traffic:
- **Min instances**: 0 (by default)
- **Max instances**: 10 (configurable)
- **Concurrency**: 1000 (default)

For high-traffic scenarios, consider:
- Increasing max instances
- Setting min instances for warm starts
- Using Cloud Load Balancer for global distribution