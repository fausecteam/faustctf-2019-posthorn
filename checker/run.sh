#!/bin/zsh

export PYTHONPATH=`pwd`
backend=`mktemp -d`

for i in {0..100}
do
  ctf-testrunner --first 1437258032 --backend $backend --tick $i --ip vulnbox-test.faust.ninja --team 1 --service 1 posthorn:PosthornChecker
done

