data = {}





data["BDBC"] = {}
data["BDBC"]["norbert"] = {"mean": 3.9, "std": 5.3, "measurement": 100 * 139/2560}
data["BDBC"]["guo_2n"] = {"mean": 48, "std": 48, "measurement": 100 * 36/2560}
data["BDBC"]["guo_pw"] = {"mean": 7.8, "std": 13.2, "measurement": 100 * 139/2560}
data["BDBC"]["atri"] = {"mean": 1.44, "std": 1.04, "measurement": 100 * 191/2560}
data["BDBC"]["us"] = {"mean": 7.0, "std": 5.6, "measurement": 100 * 64/2560}

data["BDBJ"] = {}
data["BDBJ"]["norbert"] = {"mean": 8.5, "std": 9.6, "measurement": 100 * 48/400}
data["BDBJ"]["guo_2n"] = {"mean": 2.2, "std": 2.3, "measurement": 100 * 52/400}
data["BDBJ"]["guo_pw"] = {"mean": 2.7, "std": 2.5, "measurement": 100 * 48/400}
data["BDBJ"]["atri"] = {"mean": 3.66, "std": 6.34, "measurement": 100 * 57/400}
data["BDBJ"]["us"] = {"mean": 4.5, "std": 5.9, "measurement": 100 * 16/400}

data["apache"] = {}
data["apache"]["norbert"] = {"mean": 7.7, "std": 11.2, "measurement": 100 * 29/192}
data["apache"]["guo_2n"] = {"mean": 11.6, "std": 14.4, "measurement": 100 * 18/192}
data["apache"]["guo_pw"] = {"mean": 9.7, "std": 10.8, "measurement": 100 * 29/192}
data["apache"]["atri"] = {"mean": 7.61, "std": 0.63, "measurement": 100 * 55/192}
data["apache"]["us"] = {"mean": 10.7, "std": 3.1, "measurement": 100 * 16/192}

data["LLVM"] = {}
data["LLVM"]["norbert"] = {"mean": 7.4, "std": 10.2, "measurement": 100 * 62/1024}
data["LLVM"]["guo_2n"] = {"mean": 4.5, "std": 4.2, "measurement": 100 * 22/1024}
data["LLVM"]["guo_pw"] = {"mean": 3.3, "std": 2.4, "measurement": 100 * 64/1024}
data["LLVM"]["atri"] = {"mean": 3.67, "std": 0.54, "measurement": 100 * 43/1024}
data["LLVM"]["us"] = {"mean": 3.3, "std": 0.6, "measurement": 100 * 32/1024}

data["SQL"] = {}
data["SQL"]["norbert"] = {"mean": 9.3, "std": 12.5, "measurement": 100 * 566/4653}
data["SQL"]["guo_2n"] = {"mean": 8.1, "std": 4.4, "measurement": 100 * 78/4653}
data["SQL"]["guo_pw"] = {"mean": 7.2, "std": 4.2, "measurement": 100 * 566/4653}
data["SQL"]["atri"] = {"mean": 3.46, "std": 0.12, "measurement": 100 * 925/4653}
data["SQL"]["us"] = {"mean": 5.5, "std": 0.5, "measurement": 100 * 64/4653}

data["x264"] = {}
data["x264"]["norbert"] = {"mean": 17.9, "std": 27.2, "measurement": 100 * 81/1152}
data["x264"]["guo_2n"] = {"mean": 8.5, "std": 7.5, "measurement": 100 * 32/1152}
data["x264"]["guo_pw"] = {"mean": 6.4, "std": 5.7, "measurement": 100 * 81/1152}
data["x264"]["atri"] = {"mean": 6.42, "std": 0.40, "measurement": 100 * 93/1152}
data["x264"]["us"] = {"mean": 6.6, "std": 1.3, "measurement": 100 * 32/1152}



import numpy as np
import matplotlib.pyplot as plt



def get_data(method, field):
    datasets = ["apache", "BDBC", "BDBJ", "LLVM", "SQL", "x264"]
    return_arr = []
    for dataset in datasets:
        return_arr.append(data[dataset][method][field])
    return return_arr

index = np.array([10, 40, 70, 100, 130, 160])
# index = np.array([75*(i+1) for i in xrange(6)])
print index



left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

bar_width = 4
#
opacity = 0.2
error_config = {'ecolor': '0.3'}
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'], 'size':9.5})
# rc('text', usetex=True)

f, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)

# plt.ylabel("Time saved(%)", fontsize=11)
# ax1.set_title('Apache')
r1 = ax1.bar(index, get_data("norbert", "mean"), bar_width,alpha=opacity,color='#000000',error_kw=error_config)
r2 = ax1.bar(index+bar_width, get_data("guo_2n", "mean"), bar_width,alpha=opacity,color='#999999',error_kw=error_config)
r3 = ax1.bar(index + 2*bar_width, get_data("guo_pw", "mean"), bar_width,alpha=opacity,color='#333333',error_kw=error_config)
r4 = ax1.bar(index + 3*bar_width, get_data("atri", "mean"), bar_width,alpha=opacity,color='#666666',error_kw=error_config)
r5 = ax1.bar(index + 4*bar_width, get_data("us", "mean"), bar_width,alpha=opacity,color='#d9d9d9',error_kw=error_config)
ax1.set_xlim(5, 190)
# ax1.set_ylim(0, 119)
# ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.yaxis.offsetText.set_visible(False)

# ax1.set_ylabel("Mean(%) Fault Rate")
ax1.text(0.5, 0.95*(bottom+top), 'Mean(%) Fault Rate',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=0,
        fontsize=12,
        transform=ax1.transAxes)
ax1.set_yticks([0, 10, 20, 48],)
ax1.set_yticklabels([0, 10, 20, 98.2])
ax1.set_yscale('log', basey=10)
ax1.set_xticks([15, 45, 75, 105, 135, 165])
ax1.set_xticklabels(['Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQLite', 'X264'], rotation='vertical', fontsize='large')
ax1.tick_params(axis='y', labelsize=12)
# ax1.set_ylim(0,100)


# ax2.set_title('Berkeley DB C')
r1 = ax2.bar(index, get_data("norbert", "std"), bar_width,alpha=opacity,color='#000000',error_kw=error_config)
r2 = ax2.bar(index+bar_width, get_data("guo_2n", "std"), bar_width,alpha=opacity,color='#999999',error_kw=error_config)
r3 = ax2.bar(index + 2*bar_width, get_data("guo_pw", "std"), bar_width,alpha=opacity,color='#333333',error_kw=error_config)
r4 = ax2.bar(index + 3*bar_width, get_data("atri", "std"), bar_width,alpha=opacity,color='#666666',error_kw=error_config)
r5 = ax2.bar(index + 4*bar_width, get_data("us", "std"), bar_width,alpha=opacity,color='#d9d9d9',error_kw=error_config)
ax2.set_xlim(5, 190)
# ax2.set_ylim(0, 52)
# ax2.set_yscale("log")

# ax2.yaxis.offsetText.set_visible(False)
# ax2.set_ylabel("Standard Deviation (%) Fault Rate")
ax2.text(0.5, 0.95*(bottom+top), 'Standard Deviation (%) Fault Rate',
        horizontalalignment='center',
        verticalalignment='top',
        rotation=0,
        fontsize=12,
        transform=ax2.transAxes)

ax2.set_yscale('log', basey=10)
ax2.set_ylim(0.1, 99)
ax2.set_xticks([15, 45, 75, 105, 135, 165])
ax2.set_xticklabels(['Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQLite', 'X264'], rotation='vertical', fontsize='large')
ax2.tick_params(axis='y', labelsize=12)



# ax3.set_title('Berkeley DB Java')
r1 = ax3.bar(index, get_data("norbert", "measurement"), bar_width,alpha=opacity,color='#000000',error_kw=error_config)
r2 = ax3.bar(index+bar_width, get_data("guo_2n", "measurement"), bar_width,alpha=opacity,color='#999999',error_kw=error_config)
r3 = ax3.bar(index + 2*bar_width, get_data("guo_pw", "measurement"), bar_width,alpha=opacity,color='#333333',error_kw=error_config)
r4 = ax3.bar(index + 3*bar_width, get_data("atri", "measurement"), bar_width,alpha=opacity,color='#666666',error_kw=error_config)
r5 = ax3.bar(index + 4*bar_width, get_data("us", "measurement"), bar_width,alpha=opacity,color='#d9d9d9',error_kw=error_config)
ax3.set_xlim(5, 190)
# ax3.set_ylim(0, 32)


ax3.yaxis.offsetText.set_visible(False)
# ax3.set_ylabel("Measurement (%) wrt Config")

ax3.text(0.25, 0.95*(bottom+top), 'Measurement (%) wrt Config',
        horizontalalignment='left',
        verticalalignment='top',
        rotation=0,
        fontsize=12,
        transform=ax3.transAxes)
ax3.set_yticks([0, 10, 20, 30])
ax3.set_yticklabels([0, 10, 20, 30])
ax3.set_yscale('log', basey=10)
ax3.set_xticks([15, 45, 75, 105, 135, 165])
ax3.set_xticklabels(['Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQLite', 'X264'], rotation='vertical', fontsize='large')
ax3.tick_params(axis='y', labelsize=12)

plt.figlegend([r1, r2, r3, r4, r5], ["Siegmund", "Guo (2N)", "Guo (PW)",  "Sarkar", "WHAT"], frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.023), fancybox=True, ncol=5)
# f.text(0.04, 0.5, 'Time Saved(%)', va='center', rotation='vertical', fontsize=11)
# plt.xlim(5, 125)
f.set_size_inches(12, 5)
# f.subplots_adjust(wspace=0, hspace=0)
# plt.ylabel("Time saved(%)", fontsize=11)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.tight_layout()
# plt.show()
plt.savefig('compare_graph_h.eps', bbox_inches='tight', format='eps')