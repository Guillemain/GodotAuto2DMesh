"""
@author : antoine.guillemain@gmail.com
all right reserved.

"""

import matplotlib.pyplot as plt
import numpy as np
##

def drawMesh(mesh):
    tri = mesh.vertices[np.vstack((mesh.faces.T,mesh.faces[:,0].T)).T]
    for t in tri:
        plt.plot(t[:,1],t[:,0])

def drawMeshes(meshes):
    for m in meshes:
        drawMesh(m)