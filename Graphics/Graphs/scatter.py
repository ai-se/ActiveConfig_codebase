def plot_scatter(lista, listb, colora="Blue", colorb="red"):
    import matplotlib.pyplot as plt

    # Create some data to plot
    x_lista = [l[0] for l in lista]
    y_lista = [l[1] for l in lista]

    x_listb = [l[0] for l in listb]
    y_listb = [l[1] for l in listb]


    # Create a Figure object.
    fig = plt.figure(figsize=(5, 4))

    # Create an Axes object.
    ax = fig.add_subplot(1,1,1) # one row, one column, first plot

    # Plot the data.
    ax.scatter(x_lista, y_lista, color=colora)
    ax.scatter(x_listb, y_listb, color=colorb)

    # Add a title.
    ax.set_title("Simple Figure of $y=x^{1.6}$")
    # Add some axis labels.
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    # Produce an image.
    fig.savefig("lineplot.png")
