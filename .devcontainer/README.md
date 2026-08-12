# DevContainer Configuration

This directory should contain the DevContainer configuration for VS Code.

## Required Configuration

Create a `devcontainer.json` file with the following configuration:

```json
{
  "name": "Flight Delay Prediction - SDD Project",
  "dockerFile": "../Dockerfile",
  "context": "..",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "ms-toolsai.jupyter",
        "quarto.quarto",
        "ms-vscode.vscode-yaml",
        "redhat.vscode-yaml"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.formatting.provider": "black",
        "python.linting.enabled": true,
        "python.linting.flake8Enabled": true,
        "python.linting.mypyEnabled": true,
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.organizeImports": true
        }
      }
    }
  },
  "forwardPorts": [8000, 8080],
  "postCreateCommand": "pip install -r requirements-dev.txt && pip install -r requirements-test.txt",
  "remoteUser": "root"
}
```

## Features
- Python development environment
- Black formatting
- Flake8 linting
- MyPy type checking
- Jupyter support
- Quarto support
- YAML support

## Usage
1. Install VS Code Dev Containers extension
2. Open the project in VS Code
3. Run "Dev Containers: Reopen in Container"