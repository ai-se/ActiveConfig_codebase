def list_files():
    log_directory = "../data/"
    import os
    files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".csv"]
    return files

def get_data(filename):
    import pandas as pd
    content = pd.read_csv(filename)
    dependent = [c for c in content.columns if '$<' in c][-1]
    dependent = sorted(content[dependent])
    return dependent


data = {}
left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height
files = list_files()
for file in files:
    name = file.split('/')[-1].split('_')[0]
    data[name] = get_data(file)
print data.keys()

import numpy as np
import matplotlib.pyplot as plt

error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

# plt.ylabel("Time saved(%)", fontsize=11)
# ax1.set_title('Apache')
r1 = ax1.plot(range(len(data["Apache"])), data["Apache"], color='r')
r1 = ax1.plot([7], [data["Apache"][6]], 'ro', markersize=7)
r1 = ax1.plot([3], [data["Apache"][2]], 'bo', markersize=7)
r1 = ax1.plot([10], [data["Apache"][9]], 'yo', markersize=7)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)
ax1.set_xticks(np.arange(0, 210, 50))
ax1.set_xlim(-10, 210)
ax1.text(left, 1.43*top, 'Apache',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax1.transAxes)

r1 = ax2.plot(range(len(data["BDBC"])), data["BDBC"], color='r')
r1 = ax2.plot([1], [data["BDBC"][0]], 'ro', markersize=7)
r1 = ax2.plot([1], [data["BDBC"][0]], 'bo', markersize=7)
r1 = ax2.plot([1], [data["BDBC"][0]], 'yo', markersize=7)
ax2.yaxis.offsetText.set_visible(False)
ax2.set_xlim(-100, 3100)
ax2.set_ylim(-5, 45)
ax2.set_xticks(np.arange(0, 3100, 1000))
ax2.text(left, 1.43*top, 'BDBC',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax2.transAxes)


# ax3.set_title('Berkeley DB Java')
r1 = ax3.plot(range(len(data["BDBJ"])), data["BDBJ"], color='r')
r1 = ax3.plot([5], [data["BDBJ"][4]], 'ro', markersize=7)
r1 = ax3.plot([10], [data["BDBJ"][9]], 'bo', markersize=7)
r1 = ax3.plot([13], [data["BDBJ"][12]], 'yo', markersize=7)
ax3.yaxis.offsetText.set_visible(False)
ax3.set_xticks(np.arange(0, 190, 60))
ax3.set_xlim(-10, 190)
ax3.text(left, 1.43*top, 'BDBJ',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax3.transAxes)


# ax4.set_title('LLVM')
r1 = ax4.plot(range(len(data["LLVM"])), data["LLVM"], color='r')
r1 = ax4.plot([1], [data["LLVM"][0]], 'ro', markersize=7)
r1 = ax4.plot([3], [data["LLVM"][2]], 'bo', markersize=7)
r1 = ax4.plot([4], [data["LLVM"][3]], 'yo', markersize=7)
ax4.yaxis.offsetText.set_visible(False)
ax4.set_xticks(np.arange(0, 1300, 400))
ax4.set_xlim(-100, 1300)
ax4.set_ylim(190, 280)
ax4.text(left, 1.43*top, 'LLVM',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax4.transAxes)


r1 = ax5.plot(range(len(data["SQL"])), data["SQL"], color='r')
r1 = ax5.plot([5], [data["SQL"][4]], 'ro', markersize=7)
r1 = ax5.plot([2], [data["SQL"][1]], 'bo', markersize=7)
r1 = ax5.plot([4], [data["SQL"][3]], 'yo', markersize=7)
ax5.set_xticks(np.arange(0, 5000, 1500))
ax5.yaxis.offsetText.set_visible(False)
ax5.set_xlim(-300, 5100)
ax5.set_ylim(11, 17)
ax5.text(left, 1.43*top, 'SQL',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax5.transAxes)

# ax6.set_title('X264')
r1 = ax6.plot(range(len(data["X264"])), data["X264"], color='r')
r1 = ax6.plot([5], [data["X264"][4]], 'ro', markersize=7)
r1 = ax6.plot([2], [data["X264"][1]], 'bo', markersize=7)
r1 = ax6.plot([4], [data["X264"][3]], 'yo', markersize=7)
ax6.set_xticks(np.arange(0, 1300, 400))
ax6.set_xlim(-100, 1300)
ax6.yaxis.offsetText.set_visible(False)
ax6.text(left, 1.43*top, 'X264',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=0,
        fontsize=11,
        transform=ax6.transAxes)



# plt.figlegend([r1, r2, r3, r4], ["BaseLine", "Where Exemplar", "Where Random",  "Where East West"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=2)
f.set_size_inches(9, 6)
f.subplots_adjust(wspace=0.25, hspace=0.30)
f.text(0.04, 0.5, 'Performance Measures', va='center', rotation='vertical', fontsize=11)
f.text(0.30, 0.05, 'Number of instances (sorted based on performance scores)', va='center',  fontsize=11)
plt.savefig('test_v.eps', format='eps')
