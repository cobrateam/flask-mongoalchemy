build: bootstrap test coverage

bootstrap:
	@pip install -r requirements.txt

test: clean
	@specloud --config=test/nose.cfg

coverage:
	@coverage html

clean:
	@echo 'Cleaning...'
	@find . -name '*.pyc' -exec rm -f {} \;
	@rm -rf cover .coverage
