# Pipeline Orchestration

This directory contains pipeline orchestration scripts and configurations.

## Structure
- `dags/` - Airflow DAGs (if using Airflow in future)
- `scripts/` - Pipeline execution scripts
- `config/` - Pipeline configurations

All pipeline scripts must include a `--debug-mode` flag for fast testing with synthetic data. Debug mode execution should not exceed 1 minute.