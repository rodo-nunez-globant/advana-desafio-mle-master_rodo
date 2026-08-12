# Configuration Files

This directory contains YAML configuration files with hierarchical overrides.

## Structure
- `global/` - Global settings applied to all environments
- `dev/` - Development environment settings
- `stage/` - Staging environment settings
- `prod/` - Production environment settings

## Override Order
Configurations are applied in the following order (later ones override earlier):
1. Global settings
2. Environment-specific settings
3. Runtime settings (if provided)

## Configuration Categories
- Model parameters
- Data processing settings
- API configuration
- Logging levels
- Monitoring settings

All configurations must be in YAML format and follow the hierarchical override pattern.