bootstrap:
	@pip install -e .

lint:
	@flake8 mrf_murl

test:
	python test.py
