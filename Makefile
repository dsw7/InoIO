.PHONY = help wheel setup pypi test-pypi clean black mypy test
.DEFAULT_GOAL = help

define HELP_LIST_TARGETS

    To build the latest wheel:
        $$ make wheel
    To set up the package locally:
        $$ make setup
    To upload package to PyPI:
        $$ make pypi
    To upload package to TestPyPI:
        $$ make test-pypi
    To remove dist and Python egg directories:
        $$ make clean
    To run black code formatter over Python code
        $$ make black
    To run mypy over Python code
        $$ make mypy
    To run unit tests
        $$ make test

endef

export HELP_LIST_TARGETS

help:
	@echo "$$HELP_LIST_TARGETS"

wheel:
	@pip3 install --upgrade build
	@python3 -m build

setup: wheel
	@pip3 install dist/*whl --force-reinstall

pypi: wheel
	@pip3 install --upgrade twine
	@python3 -m twine upload dist/*

test-pypi:
	@pip3 install --upgrade twine
	@python3 -m twine upload --repository testpypi dist/*

clean:
	@rm -rfv dist/ *.egg-info/

black:
	@black inoio tests

mypy:
	@mypy --cache-dir=/tmp/mypy_cache_inoio inoio tests

test:
	@python3 tests/upload.py COM3
	@python3 -m pytest -vs tests
