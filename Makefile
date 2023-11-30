install:
	python -m venv venv;\
	. venv/bin/activate ;\
	pip install -r requirements.txt;


install-windows:
	python -m venv venv;\
	. venv/Scripts/Activate ;\
	pip install -r requirements.txt;


run-local-tests:
	python -m pytest tests/conftest.py
