test:
	python -m pytest

smoke:
	python -m pytest -m smoke

regression:
	python -m pytest -m regression

.PHONY: test smoke regression
