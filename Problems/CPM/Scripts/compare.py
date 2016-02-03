data = {}





data["BDBC"] = {}
data["BDBC"]["norbert"] = {"mean": 3.9, "std": 5.3, "measurement": 100 * 139/2560}
data["BDBC"]["guo_2n"] = {"mean": 48, "std": 48, "measurement": 100 * 36/2560}
data["BDBC"]["guo_pw"] = {"mean": 7.8, "std": 13.2, "measurement": 100 * 139/2560}
data["BDBC"]["atri"] = {"mean": 2.035, "std": 1.28, "measurement": 100 * 145/2560}
data["BDBC"]["us"] = {"mean": 7.5, "std": 21.9, "measurement": 100 * 64/2560}

data["BDBJ"] = {}
data["BDBJ"]["norbert"] = {"mean": 8.5, "std": 9.6, "measurement": 100 * 48/400}
data["BDBJ"]["guo_2n"] = {"mean": 2.2, "std": 2.3, "measurement": 100 * 52/400}
data["BDBJ"]["guo_pw"] = {"mean": 2.7, "std": 2.5, "measurement": 100 * 48/400}
data["BDBJ"]["atri"] = {"mean": 4.39, "std": 6.98, "measurement": 100 * 52/400}
data["BDBJ"]["us"] = {"mean": 9.2, "std": 14.0, "measurement": 100 * 16/400}

data["apache"] = {}
data["apache"]["norbert"] = {"mean": 7.7, "std": 11.2, "measurement": 100 * 29/192}
data["apache"]["guo_2n"] = {"mean": 11.6, "std": 14.4, "measurement": 100 * 18/192}
data["apache"]["guo_pw"] = {"mean": 9.7, "std": 10.8, "measurement": 100 * 29/192}
data["apache"]["atri"] = {"mean": 7.76, "std": 1.2, "measurement": 100 * 54/192}
data["apache"]["us"] = {"mean": 11.3, "std": 3.5, "measurement": 100 * 16/192}

data["LLVM"] = {}
data["LLVM"]["norbert"] = {"mean": 7.4, "std": 10.2, "measurement": 100 * 62/1024}
data["LLVM"]["guo_2n"] = {"mean": 4.5, "std": 4.2, "measurement": 100 * 22/1024}
data["LLVM"]["guo_pw"] = {"mean": 3.3, "std": 2.4, "measurement": 100 * 64/1024}
data["LLVM"]["atri"] = {"mean": 1.8, "std": 0.18, "measurement": 100 * 131/1024}
data["LLVM"]["us"] = {"mean": 3.5, "std": 0.8, "measurement": 100 * 32/2014}

data["SQL"] = {}
data["SQL"]["norbert"] = {"mean": 9.3, "std": 12.5, "measurement": 100 * 566/4653}
data["SQL"]["guo_2n"] = {"mean": 8.1, "std": 4.4, "measurement": 100 * 78/4653}
data["SQL"]["guo_pw"] = {"mean": 7.2, "std": 4.2, "measurement": 100 * 566/4653}
data["SQL"]["atri"] = {"mean": 3.86, "std": 0.102, "measurement": 100 * 595/4653}
data["SQL"]["us"] = {"mean": 5.5, "std": 0.4, "measurement": 100 * 64/4653}

data["x264"] = {}
data["x264"]["norbert"] = {"mean": 17.9, "std": 27.2, "measurement": 100 * 81/1152}
data["x264"]["guo_2n"] = {"mean": 8.5, "std": 7.5, "measurement": 100 * 32/1152}
data["x264"]["guo_pw"] = {"mean": 6.4, "std": 5.7, "measurement": 100 * 81/1152}
data["x264"]["atri"] = {"mean": 6.54, "std": 0.47, "measurement": 100 * 94/1152}
data["x264"]["us"] = {"mean": 6.7, "std": 1.2, "measurement": 100 * 32/1152}



import numpy as np
import matplotlib.pyplot as plt



def get_data(method, field):
    datasets = ["apache", "BDBC", "BDBJ", "LLVM", "SQL", "x264"]
    return_arr = []
    for dataset in datasets:
        return_arr.append(data[dataset][method][field])
    return return_arr

index = np.array([10, 30, 50, 70, 90, 110])


left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

bar_width = 2
#
opacity = 0.2
error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='col', sharey='row')

# plt.ylabel("Time saved(%)", fontsize=11)
# ax1.set_title('Apache')
r1 = ax1.bar(index, get_data("norbert", "mean"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax1.bar(index+bar_width, get_data("guo_2n", "mean"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax1.bar(index + 2*bar_width, get_data("guo_pw", "mean"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax1.bar(index + 3*bar_width, get_data("atri", "mean"), bar_width,alpha=opacity,color='g',error_kw=error_config)
r5 = ax1.bar(index + 4*bar_width, get_data("us", "mean"), bar_width,alpha=opacity,color='b',error_kw=error_config)
# ax1.set_xlim(5, 50)
# ax1.set_ylim(0, 119)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)


ax1.text(right, 0.5*(bottom+top), 'Mean(%) \n Fault Rate',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax1.transAxes)
ax1.set_yticks([0, 10, 20, 48],)
ax1.set_yticklabels([0, 10, 20, 98.2])


# ax2.set_title('Berkeley DB C')
r1 = ax2.bar(index, get_data("norbert", "std"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax2.bar(index+bar_width, get_data("guo_2n", "std"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax2.bar(index + 2*bar_width, get_data("guo_pw", "std"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax2.bar(index + 3*bar_width, get_data("atri", "std"), bar_width,alpha=opacity,color='g',error_kw=error_config)
r5 = ax2.bar(index + 4*bar_width, get_data("us", "std"), bar_width,alpha=opacity,color='b',error_kw=error_config)
# ax2.set_xlim(5, 50)
ax2.set_ylim(0, 52)
# ax2.set_yscale("log")

# ax2.yaxis.offsetText.set_visible(False)
ax2.text(right, 0.5*(bottom+top), 'Standard Deviation (%) \n Fault Rate',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax2.transAxes)
ax2.set_yticks([0, 10, 20, 28, 48],)
ax2.set_yticklabels([0, 10, 20, 28,  243.2])



# ax3.set_title('Berkeley DB Java')
r1 = ax3.bar(index, get_data("norbert", "measurement"), bar_width,alpha=opacity,color='#660066',error_kw=error_config)
r2 = ax3.bar(index+bar_width, get_data("guo_2n", "measurement"), bar_width,alpha=opacity,color='#CC0000',error_kw=error_config)
r3 = ax3.bar(index + 2*bar_width, get_data("guo_pw", "measurement"), bar_width,alpha=opacity,color='y',error_kw=error_config)
r4 = ax3.bar(index + 3*bar_width, get_data("atri", "measurement"), bar_width,alpha=opacity,color='g',error_kw=error_config)
r5 = ax3.bar(index + 4*bar_width, get_data("us", "measurement"), bar_width,alpha=opacity,color='b',error_kw=error_config)
# ax3.set_xlim(5, 50)
ax3.set_ylim(0, 32)

ax3.yaxis.offsetText.set_visible(False)
ax3.text(right, 0.5*(bottom+top), 'Measurement (%) \n wrt Config',
        horizontalalignment='center',
        verticalalignment='center',
        rotation=270,
        fontsize=11,
        transform=ax3.transAxes)
ax3.set_yticks([0, 10, 20, 30])
ax3.set_yticklabels([0, 10, 20, 30])



plt.figlegend([r1, r2, r3, r4, r5], ["Norbert", "Guo (2N)", "Guo (PW)",  "Sarkar", "WHAT"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=3)
# f.text(0.04, 0.5, 'Time Saved(%)', va='center', rotation='vertical', fontsize=11)
plt.xticks([15, 35, 55, 75, 95, 115], ['Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQLite', 'X264'])
plt.xlim(5, 125)
f.set_size_inches(5, 9)
f.subplots_adjust(wspace=0, hspace=0)
# plt.ylabel("Time saved(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
# plt.tight_layout()
# plt.show()
plt.savefig('compare_graph.eps', format='eps')