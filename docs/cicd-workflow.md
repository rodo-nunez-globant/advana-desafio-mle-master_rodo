# CI/CD Workflow Documentation

## Overview

This project uses GitHub Actions for Continuous Integration and Continuous Delivery. The workflow is designed to be simple, reliable, and aligned with our Git Flow branching strategy.

## Workflow Structure

### Continuous Integration (CI) - `workflows/ci.yml`

**Triggers**: Pull requests to `dev`, `stage`, or `main` branches

**Jobs**:
- **model-tests**: Runs `make model-test` - Unit tests for model components
- **api-tests**: Runs `make api-test` - Unit tests for API components  
- **stress-tests**: Runs `make stress-test` - Load testing (optional, requires label)

**Artifacts**:
- Test reports (JUnit XML)
- Coverage reports (HTML/XML)
- Stress test reports (HTML)
- Retention: 30 days

### Continuous Delivery (CD) - `workflows/cd.yml`

**Triggers**: Push to `main` branch only

**Jobs**:
- **build-docker**: Builds and pushes Docker image to GitHub Container Registry

**Artifacts**:
- Docker image (ghcr.io/rodo-nunez-globant/advana-desafio-mle-master_rodo)
- Software Bill of Materials (SBOM)

## Branch Protection

The following branches are protected and require pull requests:

- **dev**: Development integration branch
- **stage**: Staging/pre-production branch  
- **main**: Production branch (project owner only)

**Required Status Checks**:
- model-tests
- api-tests
- stress-tests (when label is applied)

## Usage

### Creating a Pull Request

1. Create a feature branch from `dev`
2. Make your changes
3. Create a pull request to `dev`
4. CI will automatically run all tests
5. Once tests pass and PR is approved, merge to `dev`

### Running Stress Tests

Stress tests are resource-intensive and only run when explicitly requested:

1. Add the `run-stress-tests` label to your pull request
2. Stress tests will execute along with other tests
3. Results will be available in the artifacts

### Merging to Production

1. Merge changes through the branch progression: `dev` → `stage` → `main`
2. Only project owners can merge to `stage` and `main`
3. CD workflow automatically builds Docker image on `main` merge

## Troubleshooting

### Common Issues

**Tests Fail Locally but Pass in CI**
- Check for environment differences
- Ensure all dependencies are in `pyproject.toml`
- Verify test data is properly mocked

**CI Tests Fail**
- Check the workflow logs for specific error messages
- Download test artifacts for detailed reports
- Ensure Makefile targets work correctly

**Docker Build Fails**
- Verify `Dockerfile` is valid
- Check for missing dependencies in container
- Review build logs for specific errors

### Getting Help

1. Check workflow logs in GitHub Actions tab
2. Download and review test artifacts
3. Refer to the project constitution for guidelines
4. Contact the project team for assistance

## Configuration

### Environment Variables

The workflows use standard GitHub Actions environment variables:
- `GITHUB_TOKEN`: For registry authentication
- `GITHUB_REPOSITORY`: For image naming
- Standard GitHub context variables

### Caching

- **Dependencies**: Cached in `~/.cache/uv` for faster installs
- **Docker layers**: Cached using GitHub Actions cache
- **Cache keys**: Based on `pyproject.toml` and `uv.lock`

### Secrets

The workflows use GitHub's built-in `GITHUB_TOKEN` for authentication. No additional secrets are required for basic operation.

## Future Enhancements

Planned improvements as the project evolves:

- **Security scanning**: Add vulnerability scanning to CD workflow
- **Notifications**: Configure Slack/email notifications
- **Deployment**: Add automated deployment to GCP
- **Performance monitoring**: Add workflow performance metrics
- **Test optimization**: Implement smart test selection

## Maintenance

### Regular Tasks

- Monitor workflow execution times
- Review and update action versions
- Check artifact storage usage
- Validate branch protection rules

### Updates

- Update GitHub Actions versions regularly
- Review and optimize caching strategies
- Update documentation as workflows evolve
- Monitor for deprecated features

---

*Last Updated: 2026-08-14*  
*Version: 1.0*