def change_image(fname):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    def rgb2gray(rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

    img = mpimg.imread(fname)
    gray = rgb2gray(img)
    plt.imshow(gray, cmap = plt.get_cmap('gray'))
    plt.axis('off')
    plt.savefig('grey_compare_graph_h.eps', bbox_inches='tight', format='eps')

change_image("compare_graph.eps")