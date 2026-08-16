# ADR 006: Adoption of uv and Smart Makefile for Dependency Management

## Status
Accepted

## Context
The project needed a robust dependency management solution that would:
1. Work for all developers regardless of their local setup
2. Provide fast dependency installation
3. Support both local development and containerized deployment
4. Maintain compatibility with existing Python ecosystem

## Decision
We adopted:
1. **uv** - A modern, ultra-fast Python package installer and resolver
2. **Smart Makefile** - A Makefile that automatically detects uv availability and falls back to pip/venv

## Detailed Decision

### 1. Why uv?

#### Performance Benefits
- **10-100x faster** than pip for dependency installation
- **Efficient dependency resolution** - Uses Rust-based resolver
- **Parallel downloads** - Installs packages concurrently
- **Smart caching** - Avoids re-downloading unchanged packages

#### Developer Experience
- **Built-in virtual environment management** - `uv venv` is faster than `python -m venv`
- **Lock file support** - `uv.lock` ensures reproducible builds
- **Unified interface** - Single tool for all Python packaging needs
- **Better error messages** - Clear, actionable dependency conflict resolution

#### Production Benefits
- **Faster Docker builds** - Reduces CI/CD pipeline time
- **Deterministic installs** - `uv sync --frozen` uses exact versions
- **Smaller attack surface** - Fewer tools needed in production

### 2. Why Smart Makefile?

#### Problem Statement
Not all developers have uv installed, and we didn't want to:
- Force everyone to install a new tool immediately
- Break existing workflows
- Create onboarding friction

#### Solution
The Makefile automatically detects uv availability:

```makefile
UV_AVAILABLE := $(shell command -v uv 2> /dev/null)
ifeq ($(UV_AVAILABLE),)
    # Use pip/venv (fallback)
    PYTHON_CMD := python
    PIP_CMD := pip
    VENV_CMD := python3 -m venv
    ACTIVATE := source .venv/bin/activate &&
    INSTALL := $(PIP_CMD) install -e .
else
    # Use uv (preferred)
    PYTHON_CMD := uv run python
    PIP_CMD := uv pip
    VENV_CMD := uv venv
    ACTIVATE :=
    INSTALL := uv sync
endif
```

#### Benefits
- **Zero friction onboarding** - New developers can start immediately
- **Gradual adoption** - Teams can migrate to uv at their own pace
- **Consistent interface** - Same `make` commands work for everyone
- **Clear messaging** - Users know which tool is being used

## Consequences

### Positive
1. **Fast dependency installation** for uv users
2. **Universal compatibility** - Works with any Python setup
3. **Reduced CI/CD time** - Faster Docker builds and tests
4. **Better developer experience** - Clear error messages and faster feedback
5. **Future-proof** - uv is becoming the standard in Python packaging

### Negative
1. **Additional dependency** - Teams need to learn uv (optional)
2. **Makefile complexity** - Slightly more complex than simple commands
3. **Docker image size** - Small increase from installing uv (offset by faster builds)

### Neutral
1. **Lock file management** - Need to maintain `uv.lock` alongside `pyproject.toml`
2. **Command differences** - `uv run` vs `python` (abstracted by Makefile)

## Implementation Details

### Local Development
```bash
# With uv (preferred)
make install-dev  # Uses uv sync --dev
make api-test     # Uses uv run pytest

# Without uv (fallback)
make install-dev  # Uses pip install -e ".[dev,test]"
make api-test     # Uses pytest (with venv activated)
```

### Docker Deployment
```dockerfile
# Always uses uv in containers for speed
RUN pip install uv
RUN uv sync --frozen --no-dev
RUN uv run python challenge/train_model.py
CMD ["uv", "run", "uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Migration Path

### For Teams Without uv
1. Continue using existing `make` commands
2. No immediate changes required
3. Can install uv anytime for speed benefits

### For Teams With uv
1. All commands automatically use uv
2. Get immediate performance benefits
3. Use `uv.lock` for exact dependency control

## Alternatives Considered

### 1. Pip + requirements.txt Only
**Pros:**
- Standard Python approach
- Everyone knows it

**Cons:**
- Slow dependency installation
- No lock file support
- Manual virtual environment management

### 2. Poetry
**Pros:**
- Modern dependency management
- Lock file support

**Cons:**
- Slower than uv
- More complex learning curve
- Less adoption in the industry

### 3. Pipenv
**Pros:**
- Combines pip and venv

**Cons:**
- Slower than uv
- Less active development
- Dependency resolution issues

### 4. Force uv for Everyone
**Pros:**
- Consistent tooling
- Simpler Makefile

**Cons:**
- High onboarding friction
- Breaks existing workflows
- Not all environments support uv

## Decision Rationale

We chose the **smart Makefile approach** because it:
1. **Maximizes compatibility** - Works for every Python developer
2. **Minimizes friction** - Zero setup required for new developers
3. **Optimizes for speed** - Those with uv get significant performance benefits
4. **Future-proofs the project** - uv is becoming the de facto standard
5. **Maintains simplicity** - Same `make` commands for everyone

This approach provides the best of both worlds: cutting-edge performance for those who want it, and rock-solid compatibility for those who don't.

## References

- [uv documentation](https://docs.astral.sh/uv/)
- [uv vs pip benchmarks](https://docs.astral.sh/uv/benchmarks/)
- [Python packaging modernization](https://peps.python.org/pep-0665/)