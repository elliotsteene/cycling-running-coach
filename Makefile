notebook:
	@poetry run python -m jupyter notebook

run:
	@poetry run python coach/main.py

install:
	@poetry install
