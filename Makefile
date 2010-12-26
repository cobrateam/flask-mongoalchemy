build: bootstrap develop test coverage

release: zip_docs
	@python setup.py sdist upload
	@python setup.py bdist_egg upload
	@echo 'Released :)'

zip_docs: documentation
	@cd docs/_build/html && zip -r docs.zip *
	@echo 'Docs are at docs/_build/html/docs.zip file'

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
	@rm -rf cover .coverage docs/_build/* *.egg-info dist build
