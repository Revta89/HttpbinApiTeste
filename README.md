# httpbin-api-tests: Pytest API Framework

Target API: https://httpbin.org

## Features
- Config via YAML (`config/config.yaml`) and `.env`
- Custom retry decorator with detailed logging
- Faker-based data generation
- Allure reporting (results + static HTML)

## 1) Local setup
```bash
cd /Users/revtart/httpbin-tests
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env .env
```

## 2) Running tests
```bash
# From project root
pytest
```
- By default, Allure results are written in `reports/allure` (see `pytest.ini`).

## 3) Generate and view Allure reports
- Static HTML locally (Allure CLI required)
```bash
# Install allure (macOS): brew install allure
pytest  
allure generate reports/allure --clean -o reports/allure-html
open reports/allure-html/index.html
```

## 4) Configuration
- YAML: `config/config.yaml`
- Environment variables: `.env` (см. `.env`)
- YAML path override: `export CONFIG_YAML=/absolute/path/to/config.yaml`

## 6) CI/CD
- Workflow: `.github/workflows/ci.yml`
  - Runs pytest, downloads `allure-results` artifact
  - Generates static HTML and downloads `allure-html` artifact
