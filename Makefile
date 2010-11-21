build: bootstrap develop test coverage

bootstrap:
	@pip install -r requirements.txt

develop:
	@python -c 'from flaskext import mongoalchemy' 2>/dev/null || python setup.py develop

test: clean
	@specloud --config=tests/nose.cfg

coverage:
	@coverage html

documentation: clean
	@cd docs && make html
	@firefox docs/_build/html/index.html

clean:
	@echo 'Cleaning...'
	@find . -name '*.pyc' -exec rm -f {} \;
	@rm -rf cover .coverage docs/_build/*
