build: bootstrap develop test coverage

release: zip_docs
	python setup.py sdist upload
	@echo 'Released :)'

zip_docs: documentation
	cd docs/_build/html && zip -r docs.zip *
	@echo 'Docs are at docs/_build/html/docs.zip file'

bootstrap:
	@pip install -qr requirements.txt

test: bootstrap clean
	@nosetests --config=tests/nose.cfg

coverage:
	coverage html

documentation: clean
	cd docs && make html

clean:
	@git clean -qdfX
