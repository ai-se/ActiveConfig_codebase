def median_mre_scores():
    def list_files():
        log_directory = "../NewLogs/"
        import os
        files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".txt"]
        return files

    def get_data(filename):
        data = {}
        lines = open(filename, "r").readlines()
        for i, line in enumerate(lines):
            if i == 0: continue
            temp = line.split(",")
            temp[-1] = temp[-1].replace("\n", "")
            if temp[-1] in data.keys(): data[temp[-1]].append(round(float(temp[1]) * 100, 2))
            else:  data[temp[-1]] = [round(float(temp[1])*100, 2)]
        return data

    data = {}
    files = list_files()
    for file in files:
        name = file[:-4].split("_")[1]
        data[name] = get_data(file)
    print data.keys()
    return data


left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height


#
print median_mre_scores()["apache"].keys()
# print evaluation_data()["apache"]["east_west_where"]

import numpy as np
import matplotlib.pyplot as plt
x_axis = [0.1 * i for i in xrange(1, 10)]

f, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex='col')
# plt.subplot(3, 2, 1)
ax1.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax1.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax1.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax1.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax1.set_xlim(0.05, 0.95)
# ax1.set_ylim(0.0, 30)
# ax1.set_yticks(np.arange(0, 30, 10))
ax1.text(right, 0.5*(bottom+top), 'Apache',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax1.transAxes)
# ax1.set_ylabel("MRE")

# plt.subplot(3, 2, 2)
ax2.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax2.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax2.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax2.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax2.set_title('Berkeley DB C')
ax2.set_xlim(0.05, 0.95)
ax2.set_yticks(np.arange(0, 180, 40))
# ax2.set_ylim(-5, 70)
# ax2.set_yticks(np.arange(0, 70, 20))
# ax2.set_ylabel("MRE")
ax2.text(right, 0.5*(bottom+top), 'BDBC',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax2.transAxes)

# plt.subplot(3, 2, 3)
ax3.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax3.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax3.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax3.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax3.set_ylim(0.0, 40)
# ax3.set_yticks(np.arange(0, 40, 10))
# ax3.set_xlim(0.05, 0.95)
# ax3.set_xlabel("Training Data (% of Data)")
# ax3.set_ylabel("MRE")
ax3.text(right, 0.5*(bottom+top), 'BDBJ',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax3.transAxes)

# plt.subplot(3, 2, 4)
ax4.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax4.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax4.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax4.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax4.set_ylim(-1, 18)
# ax4.set_xlim(0.05, 0.95)
# ax4.set_ylabel("MRE")
ax4.text(right, 0.5*(bottom+top), 'X264',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax6.transAxes)

# plt.subplot(3, 2, 5)
ax5.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax5.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax5.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax5.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax5.set_xlim(0.05, 0.95)
# ax5.set_ylim(0, 13)
# ax5.set_yticks(np.arange(0, 13, 5))
# ax5.set_ylabel("MRE")
ax5.text(right, 0.5*(bottom+top), 'SQL',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax5.transAxes)

# plt.subplot(3, 2, 6)
ax6.plot(x_axis, median_mre_scores()["apache"]["exemplar_where"], 'ko-', color='#cccccc')
ax6.plot(x_axis, median_mre_scores()["apache"]["random_where"], 'kv-', color='#636363')
ax6.plot(x_axis, median_mre_scores()["apache"]["east_west_where"], 'kx-', color='#969696')
ax6.plot(x_axis, median_mre_scores()["apache"]["base_line"], 'kx-', color='#252525')
# ax6.set_xlim(0.05, 0.95)
# ax6.set_ylim(0, 10)
# ax6.set_yticks(np.arange(0, 10, 5))
# ax6.set_ylabel("MRE")
ax6.text(right, 0.5*(bottom+top), 'LLVM',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax4.transAxes)

# plt.subplots_adjust(left=0.35, bottom=0.04, right=0.90, top=0.97, wspace=0.10, hspace=0.10)
plt.figlegend([ax1.lines[2], ax1.lines[1], ax1.lines[0], ax1.lines[3]], [ r'$S_1:Random$', r'$S_2:East West$', r'$S_3:Exemplar$', r'$Baseline$'], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.025), fancybox=True, ncol=2)
plt.xticks([.2, .4, .6, .8], ['20', '40', '60', '80'])
f.set_size_inches(5, 9)
f.subplots_adjust(wspace=0, hspace=0)
f.text(0.04, 0.5, 'MRE', va='center', rotation='vertical', fontsize=11)
plt.xlabel("Percentage of Data")
# plt.subplot_tool()
# f.tight_layout()
plt.savefig('NewSamplingAccuracy.eps', format='eps')
# plt.show()