build: bootstrap develop test coverage

release: zip_docs
	python setup.py sdist upload

zip_docs: documentation
	cd docs/_build/html && zip -r docs.zip *

bootstrap:
	@pip install -qr requirements.txt

test: bootstrap clean
	@coverage run -m unittest discover
	@coverage report

coverage:
	coverage html

documentation: clean
	cd docs && make html

clean:
	@git clean -qdfX
