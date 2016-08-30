import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

intrinsic_dimension = [2.02431272052, 2.45199687314,1.33502961536,2.63340546809,1.61490528611,2.30468805888]
actual_dimension = [9, 18, 26, 11, 39, 16]
labels = ['Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQLite', 'x264']

datas = [
    [9, 2.02431272052, 'Apache'],
    [18, 2.45199687314, 'BDBC'],
    [26, 1.33502961536, 'BDBJ'],
    [11, 2.63340546809, 'LLVM'],
    [39, 1.61490528611, 'SQLite'],
    [16, 2.30468805888, 'x264']
]
datas = sorted(datas, key=lambda x:x[0])
plt.scatter([d[0] for d in datas], [d[1] for d in datas], marker='o', color='r', s=55)
for i, xy in enumerate(zip([d[0]+0.75 for d in datas], [d[1]*0.985 for d in datas])):
    ax.annotate('%s' % datas[i][-1], xy=xy, textcoords='data')
plt.xlabel("Actual Dimensions", fontsize=15)
plt.ylabel("Instrinsic Dimensions", fontsize=15)
plt.xlim(0, 45)
plt.ylim(0, 3.5)
plt.savefig("./underlying_dimension.eps")
