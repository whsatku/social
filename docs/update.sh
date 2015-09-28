#!/bin/bash
cd `dirname $0`/..
sphinx-apidoc -f -M -H Youniversity -o docs . \
	*/urls.py */migrations manage.py social ui
mv docs/modules.rst docs/index.rst
sphinx-build -b html docs docs/_build