env: local.env
	@cp -n local.env .env || echo "NOTE: review your .env file comparing with local.env"
	@touch .env

test:
	@pytest -k 'not test_selenium' 

test-matching:
	@pytest -s -rx -k $(Q) --pdb core ./tests/

coverage:
	@pytest --cov=apps --cov=core --cov-report=term-missing --cov-report=xml ./tests/	

mypy:
	@mypy core/

flake8:
	@flake8 core/
	@flake8 tests/ --extend-ignore=ANN

isort-check:
	@isort -c --profile=black -l 120 .

isort:
	@isort --profile=black -l 120 .

blue:
	@blue .

blue-check:
	@blue --check .

dead-fixtures:
	@run pytest --dead-fixtures

lint: isort blue

lint-check: mypy flake8 isort isort-check blue-check dead-fixtures

build: lint-check test

run:
	@uvicorn core.main:app --reload

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(description)	