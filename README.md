# MLLogger: simple utilities for machine learning experiment

## Functionalities
* Auto creation of unique directory
* Otherwise, you can specify directory name as use like by setting init=False
* Arguments save/load

## Dependencies
* Python 2.7+ or 3.4+

## Installation
```
python setup.py install
```

## Quick use

```
$ cd tests/
$ python test_mllogger.py --cond sample.json --lr 0.001
Logger test
{'option': None, 'decay_step': [100, 300, 500], 'cond_dir': '', 'dataset': 'MNIST', 'cond': 'sample.json', 'lr': 0.001, 'momentum': 0.9}
$ ls outputs_test/
yymmdd_HHMMSS
```
