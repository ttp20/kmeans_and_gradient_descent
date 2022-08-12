import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

img = plt.imread('tree.jpg')
height = img.shape[0]
width = img.shape[1]

img = img.reshape(height*width, 3)

kmeans = KMeans(n_clusters=4).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

img_two = np.zeros_like(img)
for i in range(len(img_two)):
    img_two[i] = clusters[labels[i]]

img_two = img_two.reshape(height,width,3)
plt.imshow(img_two)
plt.show()

print(labels)
print(clusters)