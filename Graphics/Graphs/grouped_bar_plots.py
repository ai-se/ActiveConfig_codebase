import matplotlib.pyplot as plt
import matplotlib.cm as cm
import operator as o

import numpy as np


def barplot(dpoints, file_name, title, color):
    '''
    Create a barchart for data across different categories with
    multiple conditions for each category.

    @param ax: The plotting axes from matplotlib.
    @param dpoints: The data set as an (n, 3) numpy array
    '''

    fig = plt.figure()
    ax = fig.add_subplot(111)


    # # Aggregate the conditions and the categories according to their
    # # mean values
    # conditions = [(c, np.mean(dpoints[dpoints[:,0] == c][:,2].astype(float)))
    #               for c in np.unique(dpoints[:,0])]
    # categories = [(c, np.mean(dpoints[dpoints[:,1] == c][:,2].astype(float)))
    #               for c in np.unique(dpoints[:,1])]
    #
    # # sort the conditions, categories and data so that the bars in
    # # the plot will be ordered by category and condition
    # conditions = [c[0] for c in sorted(conditions, key=o.itemgetter(1))]
    # categories = [c[0] for c in sorted(categories, key=o.itemgetter(1))]

    conditions = list(set([c[0] for c in dpoints]))
    categories = list(set([c[1] for c in dpoints]))

    # dpoints = np.array(sorted(dpoints, key=lambda x: categories.index(x[1])))

    # the space between each set of bars
    space = 0.3
    n = len(conditions)
    width = (1 - space) / (len(conditions))

    # Create a set of bars at each position
    for i,cond in enumerate(conditions):
        indeces = range(1, len(categories)+1)
        vals = dpoints[dpoints[:,0] == cond][:,2].astype(np.float)
        pos = [j - (1 - space) / 2. + i * width for j in indeces]
        ax.bar(pos, vals, width=width, label=cond, color=color[conditions[i]]) #cm.Accent(float(i) / n))

    # Set the x-axis tick labels to be equal to the categories
    ax.set_xticks(indeces)
    ax.set_xticklabels(categories, rotation='vertical')
    plt.setp(plt.xticks()[1])

    # Add the axis labels
    ax.set_ylabel("Ratio of Algorithm/BaseLine")
    ax.set_title(title)

    # Add a legend
    handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles[::-1], labels[::-1])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
    fig.savefig(file_name)


if __name__ == "__main__":
    dpoints = np.array([['rosetta', '1mfq', 9.97],
           ['rosetta', '1gid', 27.31],
           ['rosetta', '1y26', 5.77],
           ['rnacomposer', '1mfq', 5.55],
           ['rnacomposer', '1gid', 37.74],
           ['rnacomposer', '1y26', 5.77],
           ['random', '1mfq', 10.32],
           ['random', '1gid', 31.46],
           ['random', '1y26', 18.16]])

    color = {"rosetta":"Black", "rnacomposer": "Green", "random": "Red"}
    barplot(dpoints, 'barchart_3.png', "blah", color)