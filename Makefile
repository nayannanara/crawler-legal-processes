test:
	@pytest -k 'not test_selenium' 

test-matching:
	@pytest -s -rx -k $(Q) --pdb core ./tests/

coverage-without-selenium:
	@pytest -k 'not test_selenium' --cov=apps --cov=core --cov-report=term-missing --cov-report=xml ./tests/

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

lint: isort blue

lint-check: mypy flake8 isort-check blue-check bandit dead-fixtures

build: lint-check test

run:
	@uvicorn core.main:app --reload

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(description)	