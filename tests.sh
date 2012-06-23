#!/bin/sh

(cd pidatastore && python setup.py nosetests) && \
(cd piui && python setup.py nosetests)
exit $?
