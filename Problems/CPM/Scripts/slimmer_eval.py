
def list_files():
    log_directory = "../Logs/"
    import os
    files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".txt"]
    return files

def get_data(filename):
    filter = [0.4]#[0.1, 0.2, 0.4, 0.8]
    data = {}
    lines = open(filename, "r").readlines()
    for i, line in enumerate(lines):
        if i == 0: continue
        temp = line[:-1].split(",")
        temp[-1] = temp[-1].replace("\n", "")
        if float(temp[0]) not in filter: continue
        # saved_percentage = float(temp[-2])/float(temp[-2]) * 100
        if temp[-1] in data.keys(): data[temp[-1]].append(float(temp[-2]))
        else:  data[temp[-1]] = [float(temp[-2])]

    return data

data = {}
left, width = .55, .5
bottom, height = .25, .5
right = left + width
top = bottom + height
files = list_files()
for file in files:
    name = file[:-4].split("_")[1]
    data[name] = get_data(file)

import numpy as np
import matplotlib.pyplot as plt


dataset_names = data.keys()
techniques_names = data['apache'].keys()

transform_data = {}
for tnames in techniques_names:
    temp = []
    for dnames in dataset_names:
        temp.extend(data[dnames][tnames])
    transform_data[tnames] = temp



ind = np.arange(0, 12, 2)  # the x locations for the groups
width = 0.35       # the width of the bars

plt, ax = plt.subplots()
ex_where = ax.bar(ind, transform_data['base_line'], width, color='r')

r_where = ax.bar(ind+width, transform_data['random_where'], width, color='y')
ew_where = ax.bar(ind+2*width, transform_data['east_west_where'], width, color='g')

# add some text for labels, title and axes ticks
ax.set_ylabel('Number of Evaluations')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQL', 'X264') )

# ax.legend( (ex_where[0], r_where[0], ew_where[0]), ('Where Exemplar', 'Where Random', 'Where East West') )
plt.legend([ex_where[0], r_where[0], ew_where[0]], [ "Where Exemplar", "Where Random",  "Where East West"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=3)
# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
#                 ha='center', va='bottom')
#
# autolabel(rects1)
# autolabel(rects2)

plt.show()



plt.savefig('evaluation_graph_slimmer.eps', format='eps')