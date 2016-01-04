#! /Users/rkrsn/anaconda/bin/python
from os import environ, getcwd, walk
import sys
# Update PYTHONPATH
# HOME = environ['HOME']
# axe = HOME + '/git/axe/axe/'  # AXE
# pystat = HOME + '/git/pystats/'  # PySTAT
# cwd = getcwd()  # Current Directory
# sys.path.extend([axe, pystat, cwd])
from axe.dtree import *
from axe.table import *
from _imports.where2 import *
import makeAmodel
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
# import smote


def explore(dir):
  datasets = []
  for (dirpath, dirnames, filenames) in walk(dir):
    datasets.append(dirpath)

  training = []
  testing = []
  for k in datasets[1:]:
    train = [[dirPath, fname] for dirPath, _, fname in walk(k)]
    test = [train[0][0] + '/' + train[0][1].pop(-1)]
    training.append(
        [train[0][0] + '/' + p for p in train[0][1] if not p == '.DS_Store'])
    testing.append(test)
  return training, testing


def newTable(tbl, headerLabel, Rows):
  tbl2 = clone(tbl)
  newHead = Sym()
  newHead.col = len(tbl.headers)
  newHead.name = headerLabel
  tbl2.headers = tbl.headers + [newHead]
  return clone(tbl2, rows=Rows)


def createTbl(
    data,
    settings=None,
    _smote=False,
    isBin=False,
    bugThres=1,
        duplicate=False):
  """
  kwargs:
  _smote = True/False : SMOTE input Data (or not)
  _isBin = True/False : Reduce bugs to defects/no defects
  _bugThres = int : Threshold for marking stuff as defective,
                    default = 1. Not defective => Bugs < 1
  """
  makeaModel = makeAmodel.makeAModel()
  _r = []
  for t in data:
      m = makeaModel.csv2py(t, _smote=_smote, duplicate=duplicate)
      _r += m._rows
  m._rows = _r
  prepare(m, settings=None)  # Initialize all parameters for where2 to run
  # print("WHERE start")

  tree = where2(m, m._rows)  # Decision tree using where2
  # print tree
  # import pdb
  # pdb.set_trace()
  # print("WHERE end")
  tbl = table(t)

  headerLabel = '=klass'
  Rows = []
  for k, _ in leaves(tree):  # for k, _ in leaves(tree):
      for j in k.val:
          tmp = j.cells
          if isBin:
              tmp[-1] = 0 if tmp[-1] < bugThres else 1
          tmp.append('_' + str(id(k)))
          j.__dict__.update({'cells': tmp})
          Rows.append(j.cells)

  return newTable(tbl, headerLabel, Rows)


def wrapper_createTbl(dir):
    return createTbl([dir], _smote=False)


def test_createTbl():
  dir = '../../Data/Apache_AllMeasurements.csv'
  newTbl = createTbl([dir], _smote=False)
  # import pdb
  # pdb.set_trace()
  print(len(newTbl._rows))
  # print [x.cells for x in newTbl._rows]
  print len(set([z[-1] for z in map(lambda x: x.cells, newTbl._rows)]))



def drop(test, tree):
  loc = apex(test, tree)
  return loc


if __name__ == '__main__':
  test_createTbl()