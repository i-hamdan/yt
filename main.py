import random
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import pickle

#st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# FUNCTIONS
def print_plot_plain(dataNumber, title):
    figure = plt.figure()
    ax = figure.add_subplot()
    (x, y, color) = points[dataNumber]
    plt.scatter(x, y, color=color)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    plt.title(label=title)
    return figure

def generate_random_index(k):
    return [random.randrange(500) for i in range(k)]

def get_coordinates_for_random_centroids(randPointIndex, k):
    centroidsx = {}
    centroidsy = {}
    for i in range(k):
        centroidsx[i] = x[randPointIndex[i]]
        centroidsy[i] = y[randPointIndex[i]]
    return (centroidsx.values(), centroidsy.values())

def print_plot_plain_star(dataNumber, centXval, centYval, k, title):
    figure = plt.figure()
    ax = figure.add_subplot()
    (x, y, color) = points[dataNumber]
    plt.scatter(x, y, color=color)
    plt.scatter(centXval, centYval,
                color=['r', 'b', 'g', 'y'][:k],
                marker="*",
                edgecolor="black",
                s=150)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    plt.title(label=title)
    return figure

def zip_coordinates(centXval, centYval, dataNumber):
    centCoord = tuple(zip(centXval, centYval))
    centCoord = np.asarray(centCoord)
    (x, y, color) = points[dataNumber]
    allCoord = tuple(zip(x, y))
    allCoord = np.asarray(allCoord)
    return (centCoord, allCoord)

def update_centroid_z_times(z, centCoord, allCoord, k):
    for i in range(z):
        groupedCoord = {}
        for i in range(k):
            groupedCoord[i] = []

        for i in allCoord:
            distances = []
            for j in range(k):
                distances.append((np.linalg.norm(i - centCoord[j]), j))
            minCentroid = min(distances)[1]
            groupedCoord[minCentroid].append(i)

        for j in range(k):
            groupedCoord[j] = np.asarray(groupedCoord[j])
            if len(groupedCoord[j]) != 0:
                centCoord[j] = groupedCoord[j].mean(axis=0)

    return (centCoord, groupedCoord)

def print_plot_with_centroid_and_bins(centCoord, groupedCoord, k, title):
    coordnew = list(zip(*centCoord))
    xnew = {}
    ynew = {}
    figure = plt.figure()
    ax = figure.add_subplot()
    for i in range(k):
        xnew[i], ynew[i] = list(zip(*groupedCoord[i]))
        plt.scatter(xnew[i], ynew[i],
                    color=['indianred', 'royalblue', 'springgreen', 'khaki'][i])
    plt.scatter(coordnew[0], coordnew[1],
                color=['r', 'b', 'g', 'y'][:k],
                marker="*",
                edgecolor="black",
                s=150)
    ax.set_aspect('equal', adjustable='box')
    plt.xticks([])
    plt.yticks([])
    plt.title(label=title)
    return figure

#END OF FUNCTIONS



filehandler = open('pointList.pkl', 'rb')
points = pickle.load(filehandler)
filehandler.close()

st.title('K-Means Clustering Algorithm Visualization')


col1, col2 = st.columns((1,2))
with col1:
    st.write('')
    option = st.selectbox(
        'Please select a dataset to analyse?',
        ('One', 'Two', 'Three', 'Four', 'Five',
         'Six', 'Seven', 'Eight', 'Nine'))

    dict = {
        'One':8,
        'Two':5,
        'Three':3,
        'Four':4,
        'Five':2,
        'Six':6,
        'Seven':7,
        'Eight':1,
        'Nine':0
    }
    (x, y, color) = points[dict[option]]



    fig = print_plot_plain(dict[option], '')
    st.pyplot(fig)


    st.write('')
    st.write('')
    numClusters = st.slider('Please select the number of clusters?', 2, 4, 3)
    st.write('You selected', numClusters, 'Clusters')




# CODE FOR KMEANS
dataNumber = dict[option]
fig0 = print_plot_plain(dataNumber, 'Starting Dataset')

randPointIndex = generate_random_index(numClusters)
centXval, centYval = get_coordinates_for_random_centroids(randPointIndex, numClusters)
fig1 = print_plot_plain_star(dataNumber, centXval,
                             centYval, numClusters,
                             'Choose {}-random centroids'.format(numClusters))

centCoord, allCoord = zip_coordinates(centXval, centYval, dataNumber)

centCoord, groupedCoord = update_centroid_z_times(1, centCoord, allCoord, numClusters)
figOne = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=1] Clusters after first iteration\n'+
                                      'with new centroids as mean of new clusters')

centCoord, groupedCoord = update_centroid_z_times(1, centCoord, allCoord, numClusters)
figTwo = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=2] Clusters after second iteration\n'+
                                      'with new centroids as mean of new clusters')

centCoord, groupedCoord = update_centroid_z_times(1, centCoord, allCoord, numClusters)
figThree = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=3] Clusters after third iteration\n'+
                                      'with new centroids as mean of new clusters')

centCoord, groupedCoord = update_centroid_z_times(1, centCoord, allCoord, numClusters)
figFour = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=4] Clusters after fourth iteration\n'+
                                      'with new centroids as mean of new clusters')

centCoord, groupedCoord = update_centroid_z_times(6, centCoord, allCoord, numClusters)
figTen = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=10] Clusters after tenth iteration\n'+
                                      'with new centroids as mean of new clusters')

centCoord, groupedCoord = update_centroid_z_times(90, centCoord, allCoord, numClusters)
figHundred = \
    print_plot_with_centroid_and_bins(centCoord,
                                      groupedCoord, numClusters,
                                      '[n=100] Clusters after 100th iteration\n'+
                                      'with new centroids as mean of new clusters')

with col2:
    if st.button('Analyze'):
        element = st.pyplot(fig0)
        time.sleep(3)
        element.empty()
        element = st.pyplot(fig1)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figOne)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figTwo)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figThree)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figFour)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figTen)
        time.sleep(3)
        element.empty()
        element = st.pyplot(figHundred)


