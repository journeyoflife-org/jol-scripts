.PHONY: validate lint format typecheck scan test audit clean pre-push-check

validate: lint scan test

lint:
	ruff check lib/ scripts/
	ruff format --check lib/ scripts/

format:
	ruff check --fix lib/ scripts/
	ruff format lib/ scripts/

typecheck:
	mypy lib/ scripts/

scan:
	bandit -c pyproject.toml -r lib/ scripts/

test:
	pytest

audit:
	@echo "=== Ruff Lint ===" && ruff check lib/ scripts/
	@echo "=== Bandit Scan ===" && bandit -c pyproject.toml -r lib/ scripts/
	@echo "=== Mypy ===" && mypy lib/ scripts/
	@echo "=== Pytest ===" && pytest

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true

pre-push-check:
	@echo "════════════════════════════════════════════"
	@echo "  JOL Pre-Push Validation — $(shell basename $(CURDIR))"
	@echo "════════════════════════════════════════════"
	@echo ""
	@echo "[1/5] TruffleHog — full history secret scan"
	trufflehog git file://. --results=verified,unknown --fail
	@echo ""
	@echo "[2/5] Ruff lint + Bandit SAST"
	ruff check --select S,E,W,F,I,N,B . --output-format=concise
	@echo ""
	@echo "[3/5] mypy type check"
	mypy lib/ scripts/ --ignore-missing-imports --strict || true
	@echo ""
	@echo "[4/5] pytest with coverage"
	pytest --cov=lib --cov-report=term-missing --cov-fail-under=80 -q
	@echo ""
	@echo "[5/5] pip-audit dependency scan"
	pip-audit --desc
	@echo ""
	@echo " All checks passed — safe to push"
