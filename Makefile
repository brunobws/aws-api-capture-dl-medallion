# Breweries Project Makefile
# Useful commands for development and management

.PHONY: help venv install dev-install run test lint format clean

help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make install       - Install dependencies"
	@echo "  make dev-install   - Install with development tools"
	@echo "  make run           - Run Streamlit app"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code with Black"
	@echo "  make clean         - Clean cache and temp files"
	@echo "  make aws-check     - Verify AWS credentials"

venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  Windows: venv\Scripts\activate"
	@echo "  Unix/macOS: source venv/bin/activate"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

run:
	streamlit run streamlit_app/main.py

test:
	pytest tests/ -v --cov=streamlit_app

lint:
	flake8 streamlit_app/ tests/ --max-line-length=100

format:
	black streamlit_app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

aws-check:
	aws sts get-caller-identity

requirements-update:
	pip list --outdated

# Docker commands (optional)
docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

docker-down:
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	docker-compose -f docker/docker-compose.yml logs -f
