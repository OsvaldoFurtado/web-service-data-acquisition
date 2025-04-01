.PHONY: lint type-check test format docs clean

lint:
	tox -e lint

type-check:
	tox -e type

test:
	tox

format:
	tox -e format

docs:
	cd docs && make html

clean:
	rm -rf .pytest_cache .mypy_cache __pycache__ .tox dist build
