build: bootstrap test coverage

bootstrap:
	@pip install -r requirements.txt

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
