from __future__ import division

from pdb import set_trace

from numpy import *


def splits(data, num = 10):
  Val = [];
  for d in data: Val += d[1:]
  hi = max(Val)
  lo = min(Val)
  return linspace(lo, hi, num)

def draw(val, length = 50):
  return int(val * length) * '*'

def deno(Val):
  return sum([sum(v) for v in Val])


def histplot(Data, bins = []):
  if not bins: bins = splits(Data, num = 10)
  Names = []; Values = []
  for dat in Data:
    Names.append(dat[0])
    counts = histogram(dat[1:], bins = bins)[0].tolist()
    Values.append(counts)

  line = 20 * '-'
  # Print header
  print ('%12s %6s' % ('Name', 'Range')); print line
  for n in xrange(len(bins) - 1):
    for m in xrange(len(Data)):
      # print sum(Values[m])
      print ('%12s %6s|' % (Names[m],
             '' + str(bins[n]))), draw((Values[m][n]) / deno(Values)), Values[m][n]
    print ""

def _test():
  import random
  before = [random.randint(0, 100) for _ in xrange(100)]
  before.insert(0, 'Before')
  After = [random.randint(0, 100) for _ in xrange(100)]
  After.insert(0, 'After')
  histplot([before, After], bins = [1, 5, 10, 100])

if __name__ == '__main__':
  _test()
  _test()
