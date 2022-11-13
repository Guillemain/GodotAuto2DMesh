import numpy as np
import scipy.spatial as scispa
import skimage.morphology as morpho

##

class Mesh():
    """
    Simple mesh.
    """
    def __init__(self,faces,vertices):
        self.faces = faces
        self.vertices = vertices


def get_cluster(img,alpha_thr=0.1,n_dilatation=3,n_erosion=2):
    """
    Récupère les groupes de pixels voisins
    à terme représentant chaque éléments de l'image.

    alpha_thr : Seuil alpha pour trouver les éléments.
    n_dilatation : La marge appliquée sur les éléments (en px).
    n_erosion : (noise filtering) retire les petits éléments.
    """
    masque = img[...,-1] > alpha_thr

    for _ in range(n_erosion): # noise filtering
        masque = morpho.binary_erosion(masque)
    for _ in range(n_dilatation+n_erosion): # on retire la dentelle.
        masque = morpho.binary_dilation(masque)

    return morpho.label(masque)

def get_contour(labelmap):
    """
    Retient que les pixels contour d'un groupe.
    """
    masque = labelmap != 0
    interieur = morpho.binary_erosion(masque)
    return (masque & (~interieur)) * labelmap

def get_meshes_from_clusters(labelmap,bigshape_thr=300):
    """
    retourne un mesh par groupe dans la label map.

    """
    contour = get_contour(labelmap)
    groupe = np.unique(labelmap)
    group_mesh = [None for _ in range(len(groupe)-1)]
    for idx,lbl in enumerate(groupe):
        cassimple = True
        if(lbl==0):
            continue
        pts_rw = np.argwhere(contour==lbl)
        midlePoint=None
        if (len(pts_rw)>bigshape_thr):
            cassimple=False
            midlePoint = np.argwhere(labelmap==lbl)
            np.random.shuffle(midlePoint)
            midlePoint=midlePoint[:10]
        pts_rw = pts_rw[scispa.ConvexHull(pts_rw).vertices]
        if(cassimple):
            group_mesh[idx-1] = Mesh(np.array([np.arange(0,len(pts_rw))]),pts_rw)

        else:
            pts=np.vstack((pts_rw,midlePoint))
            #np.random.shuffle(pts) # for sampling.
            #pts = pts_rw[:10,:] # sampling
            face = scispa.Delaunay(pts)
            group_mesh[idx-1] = Mesh(face.simplices,pts)

    return group_mesh












