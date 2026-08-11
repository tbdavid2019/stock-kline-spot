# Changelog

All notable changes to the **Candlestick Pattern & Technical Indicator Analysis (stock-kline-spot)** project will be documented in this file.

## [v1.4.0] - 2026-08-11

### 🚀 Features & Infrastructure
- **GitHub Actions Automated CI/CD**: Added `.github/workflows/docker-publish.yml` to automatically build and push Docker images to Docker Hub (`tbdavid2019/stock-kline-spot:latest` and commit tags) on push to `main`.
- **Automated Secrets Configuration**: Integrated Docker Hub authentication via GitHub Secrets (`DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`).

### ⚡ Performance & Docker Optimization
- **Modernized Base Image**: Upgraded Docker base image from `continuumio/miniconda3` to official lightweight `python:3.11-slim`.
- **TA-Lib C Library Compilation**: Compiled TA-Lib 0.4.0 C library from source, eliminating previous Python 3.10 and NumPy 1.23.5 version locks.
- **Docker Layer Caching**: Restructured `Dockerfile` to leverage layer caching for faster builds.

### 🛠️ Bug Fixes & Package Upgrades
- **Dependencies Upgrade**: Updated `requirements.txt` to support modern releases: `yfinance>=0.2.40`, `ta-lib`, `gradio>=4.0.0`, `pandas>=2.0.0`, `plotly>=5.18.0`, `numpy>=1.26.0`.
- **Robust yfinance Parsing**: Fixed `fetch_stock_data` in `app.py` to flexibly handle multi-index column level variations in newer `yfinance` releases.
- **Repository Cleanup**: Updated `.dockerignore` and `.gitignore` to prevent transient/temporary files from cluttering builds.

---

## [v1.3.0] - 2025-02-24

### Added
- Support for customizable technical indicators (MACD, RSI, BBANDS) and volume subplot.
- Script for auto-updating `yfinance` (`auto_update_yfinance.sh`).
