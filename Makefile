#
# Simple Makefile for the Wiring project.
#

.PHONY: docs

all:
	@echo "The following make targets are available:"
	@echo "    make install"
	@echo "    make docs"

install:
	@python setup.py install
	@rm -rf build

docs:
	@make -C docs html

pdf:
	@make -C docs latexpdf

clean:
	@make -C docs clean

autopep8:
	@find . -name "*.py" -exec autopep8 -i --ignore=E501 {} \;

readthedocs:
	@curl -X POST http://readthedocs.org/build/wiring-x86

