# GitHub Actions Updates - Fix Deprecated Actions

## Issue
GitHub Actions workflows were failing due to deprecated action versions:
- `actions/upload-artifact@v3` - Deprecated as of April 16, 2024
- `actions/cache@v3` - Also deprecated

## Changes Made

### 1. Updated upload-artifact actions
- **Files affected**: `.github/workflows/ci.yml`, `.github/workflows/cd.yml`
- **Changes**: 4 occurrences updated from `v3` to `v4`
  - ci.yml: Model test artifacts upload
  - ci.yml: API test artifacts upload  
  - ci.yml: Stress test artifacts upload
  - cd.yml: Stress test report upload

### 2. Updated cache actions
- **Files affected**: `.github/workflows/ci.yml`
- **Changes**: 3 occurrences updated from `v3` to `v4`
  - Model tests job cache
  - API tests job cache
  - Stress tests job cache

## Current Action Versions
- ✅ `actions/checkout@v4` - Latest
- ✅ `actions/setup-python@v4` - Latest
- ✅ `actions/upload-artifact@v4` - Latest
- ✅ `actions/cache@v4` - Latest
- ✅ `actions/github-script@v7` - Latest

## Notes
- No breaking changes were required for these updates
- All parameters and configurations remain compatible
- The workflows should now run without deprecation warnings