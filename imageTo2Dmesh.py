"""
@author : antoine.guillemain@gmail.com
all right reserved.
"""
import matplotlib.pyplot as plt
from plotter import *
from DataProcessing import *

img = plt.imread(r"E:\Projet\EssaiRig2D\RigGodot\2DAssets\player\rig0037.png")

labelmap = get_cluster(img,0.1,5,2)
##
meshes = get_meshes_from_clusters(labelmap)
plt.imshow(img)
drawMeshes(meshes)
plt.show()
###
