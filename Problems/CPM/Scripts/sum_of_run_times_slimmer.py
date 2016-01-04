
def list_files():
    log_directory = "../Logs/"
    import os
    files = [log_directory+file for file in os.listdir(log_directory) if file[-4:]==".txt"]
    return files

def get_data(filename):
    filter = [0.4]  # [0.1, 0.2, 0.4, 0.8]
    data = {}
    lines = open(filename, "r").readlines()
    for i, line in enumerate(lines):
        if i == 0: continue
        temp = line[:-1].split(",")
        temp[-1] = temp[-1].replace("\n", "")
        if float(temp[0]) not in filter: continue
        run_time = (float(temp[-3]) - float(temp[-4]))/float(temp[-3]) * 100
        if temp[-1] in data.keys(): data[temp[-1]].append(run_time)
        else:  data[temp[-1]] = [run_time]

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


dataset_names = ["apache", "BDBC", 'BDBJ', 'LLVM', 'SQL', 'X264']

techniques_names = data['apache'].keys()

print dataset_names

transform_data = {}
for tnames in techniques_names:
    temp = []
    for dnames in dataset_names:
        temp.extend(data[dnames][tnames])
    transform_data[tnames] = temp

ind = np.arange(0, 12, 2)  # the x locations for the groups
width = 0.35       # the width of the bars

plt, ax = plt.subplots()
# ex_where = ax.bar(ind, transform_data['base_line'], width, color='r')

r_where = ax.bar(ind+width, transform_data['random_where'], width, color='y')
ew_where = ax.bar(ind+2*width, transform_data['east_west_where'], width, color='g')

# add some text for labels, title and axes ticks
ax.set_ylabel('Time Required (% of total runtime)')
# ax.set_xlabel('Dataset')
ax.set_xticks(ind+width)
ax.set_ylim(0, 25)
ax.set_xticklabels( ('Apache', 'BDBC', 'BDBJ', 'LLVM', 'SQL', 'X264') )

ax.text(0.5, transform_data['east_west_where'][0]*1.1, "78")
ax.text(2.5, transform_data['east_west_where'][1]*1.1, "56")
ax.text(4.5, transform_data['east_west_where'][2]*1.1, "312")
ax.text(6.5, transform_data['east_west_where'][3]*1.1, "67")
ax.text(8.5, transform_data['east_west_where'][4]*1.1, "19")
ax.text(10.5, transform_data['east_west_where'][5]*1.1, "148")

# ax.legend( (ex_where[0], r_where[0], ew_where[0]), ('Where Exemplar', 'Where Random', 'Where East West') )
plt.legend([ r_where[0], ew_where[0]], [ "Where Random",  "Where East West"], frameon=False, loc='lower center', bbox_to_anchor=(0.5, -0.0145), fancybox=True, ncol=3)



plt.savefig('sum_of_run_times_graph_slimmer_percentage.eps', format='eps')