install:
	    pip install --upgrade pip &&\
		    pip install -r requirements.txt

test:
	    python -m pytest -vv test_howdy.py

format:
	    black *.py


lint:
	    pylint --disable=R,C howdy.py

All: install lint test
