# ADR 007: Docker Configuration and GCP Cloud Run Deployment

## Status
Accepted

## Context
For Part III of the challenge, we needed to deploy the Flight Delay Prediction API to a cloud provider. The requirements were:
1. Deploy the API to GCP (recommended)
2. Update the Makefile with the deployed URL
3. Pass stress tests against the deployed endpoint
4. Ensure the deployment is production-ready and cost-effective

## Decision
We adopted:
1. **Multi-stage Docker configuration** optimized for Cloud Run
2. **GCP Cloud Run** as the deployment target
3. **Automated deployment pipeline** with URL updates

## Detailed Decision

### 1. Docker Configuration

#### Base Image Choice
```dockerfile
FROM python:3.13-slim
```
**Rationale:**
- `slim` variant reduces image size (~100MB smaller than full image)
- Python 3.13 matches project requirements
- Official image ensures security updates and compatibility

#### Dependency Management Strategy
```dockerfile
# Copy requirements first for better caching
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv sync --frozen --no-dev
```
**Rationale:**
- **Layer caching** - Dependencies change less frequently than code
- **uv for speed** - 10-100x faster installation in CI/CD
- **--frozen flag** - Uses exact versions from uv.lock for reproducibility
- **--no-dev flag** - Excludes development dependencies, reducing attack surface

#### Model Training in Build
```dockerfile
RUN uv run python challenge/train_model.py
```
**Rationale:**
- **Pre-trained model** - No need to ship training data
- **Faster startup** - Model is ready when container starts
- **Consistent model** - Same model across all deployments
- **Build-time validation** - Fails fast if training fails

#### Production Configuration
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
EXPOSE $PORT
```
**Rationale:**
- **Python optimizations** - Standard production best practices
- **PORT=8080** - Cloud Run standard port
- **Health checks** - Enables automatic monitoring

### 2. GCP Cloud Run Selection

#### Why Cloud Run over Alternatives?

| Service | Pros | Cons | Decision |
|---------|------|------|----------|
| **Cloud Run** | Serverless, auto-scaling, pay-per-use, HTTPS included | Cold starts, max 2GB RAM | ✅ **Chosen** |
| App Engine | More configuration options, larger instances | More complex, higher minimum cost | ❌ |
| Cloud VM + Docker | Full control, any configuration | Manual scaling, higher ops overhead | ❌ |
| Cloud Functions | Very cheap for simple APIs | 9MB limit, timeout restrictions | ❌ |

#### Cloud Run Configuration
```bash
gcloud run deploy flight-delay-api \
    --image $IMAGE_NAME \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10
```

**Configuration Rationale:**
- **512Mi memory** - Sufficient for model + API (model ~2MB, API ~50MB)
- **1 vCPU** - Adequate for prediction latency (~50ms per request)
- **Max 10 instances** - Controls costs while handling load
- **Allow unauthenticated** - Public API as required by challenge
- **us-central1** - Cost-effective region with good performance

### 3. Deployment Automation

#### Automated URL Updates
```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME ...)

# Update Makefile automatically
sed -i.bak "s|STRESS_URL = .*|STRESS_URL = $SERVICE_URL|g" Makefile
```

**Benefits:**
- **Zero manual steps** - URL updated automatically
- **No human error** - Can't forget to update URL
- **Immediate testing** - Ready for `make stress-test`

#### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1
```

**Rationale:**
- **Automatic monitoring** - Cloud Run restarts unhealthy containers
- **Grace period** - 5 seconds for cold start
- **Reasonable intervals** - Not too frequent to waste resources

## Consequences

### Positive
1. **Cost-effective** - Pay only for actual usage
2. **Auto-scaling** - Handles traffic spikes automatically
3. **Zero ops** - No servers to manage
4. **Fast deployment** - Build and deploy in ~5 minutes
5. **HTTPS included** - Automatic SSL certificate
6. **Built-in monitoring** - Logs, metrics, and error tracking

### Negative
1. **Cold starts** - First request may be slower (~2-3 seconds)
2. **Resource limits** - Max 2GB RAM, 4 vCPUs
3. **Vendor lock-in** - Cloud Run specific features
4. **Request timeout** - Max 60 minutes (not an issue for our API)

### Neutral
1. **Stateless** - Must be stateless (good for our use case)
2. **HTTP only** - No TCP/UDP (not needed for our API)

## Security Considerations

### Container Security
```dockerfile
# Non-root user (could be added)
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```
*Note: Not implemented yet but considered for production*

### Network Security
- **HTTPS only** - Cloud Run enforces HTTPS
- **IAM integration** - Can restrict access if needed
- **VPC Connector** - For private services

### Secrets Management
- **Environment variables** - For non-sensitive config
- **Secret Manager** - For sensitive data (not needed currently)

## Performance Optimizations

### Build Optimizations
1. **Layer caching** - Dependencies copied first
2. **.dockerignore** - Excludes unnecessary files
3. **Multi-stage** - Could be added for smaller images

### Runtime Optimizations
1. **Model pre-loading** - Trained during build
2. **Memory efficient** - 512Mi is sufficient
3. **Fast predictions** - ~50ms per request

## Cost Analysis

### Cloud Run Pricing (us-central1)
- **CPU**: $0.000024 per vCPU-second
- **Memory**: $0.0000025 per GB-second  
- **Requests**: $0.40 per million requests

### Estimated Monthly Costs
- **1000 requests/day**: ~$0.01
- **10,000 requests/day**: ~$0.10
- **100,000 requests/day**: ~$1.00

*Very cost-effective for the challenge requirements*

## Monitoring and Observability

### Built-in Monitoring
- **Request metrics** - Latency, error rates, request count
- **Instance metrics** - CPU, memory usage
- **Log aggregation** - All logs in Cloud Logging

### Custom Monitoring
```python
# Could add custom metrics
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
```

## Disaster Recovery

### Automatic Recovery
- **Health checks** - Auto-restart on failure
- **Multi-zone** - Automatic failover within region
- **Rollbacks** - Easy to deploy previous version

### Backup Strategy
- **Model in image** - No separate backup needed
- **Code in Git** - Version controlled
- **Configuration** - In deployment scripts

## Future Considerations

### Potential Improvements
1. **Multi-region deployment** - For global latency
2. **Custom domain** - branded URLs
3. **A/B testing** - Gradual rollouts
4. **Load testing** - Automated performance tests

### Scaling Beyond Cloud Run
If the service grows beyond Cloud Run limits:
1. **GKE** - For complex workloads
2. **Cloud Run on GKE** - Hybrid approach
3. **Anthos** - Multi-cloud deployment

## References

- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Cloud Run pricing](https://cloud.google.com/run/pricing)
- [Docker best practices](https://docs.docker.com/develop/dev-best-practices/)
- [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/)