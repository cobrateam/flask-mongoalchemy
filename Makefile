build: bootstrap test coverage

bootstrap:
	@pip install -r requirements.txt

test: clean
	@specloud --config=test/nose.cfg

coverage:
	@coverage html

themes_dir=`pwd`
documentation:
	@cd docs && make html
	@firefox docs/_build/html/index.html

clean:
	@echo 'Cleaning...'
	@find . -name '*.pyc' -exec rm -f {} \;
	@rm -rf cover .coverage
