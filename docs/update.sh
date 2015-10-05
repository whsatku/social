#!/bin/bash
cd `dirname $0`/..
sphinx-apidoc -f -M -H "Modules Index" -o docs . \
	*/urls.py */migrations */tests* */admin* \
	manage.py social ui docs
sphinx-build -b html docs docs/_build