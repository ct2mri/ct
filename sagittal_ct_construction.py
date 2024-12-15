import os
from os import walk
import numpy as np
from pydicom import dcmread
import matplotlib.pyplot as plt

def interpolate_slices(stack, new_depth):
    interpolated_stack = []
    for i in range(len(stack) - 1):
        interpolated_stack.append(stack[i])
        for j in range(new_depth):  # Divide the z-space
            weight = j / new_depth
            interpolated_slice = (1 - weight) * stack[i] + weight * stack[i + 1]
            interpolated_stack.append(interpolated_slice)
    return np.array(interpolated_stack)

path = './Hr36f/'

stack = []
for (dirpath, _, filenames) in walk(path):
    pass
for fname in filenames:
    stack.append(dcmread(dirpath+fname).pixel_array)

stack = np.array(stack)
new_volume = interpolate_slices(stack, 5)
print(new_volume.shape)
# slice = stack[:,:,1]
# # print(slice.shape)
plt.imshow(new_volume[:,30,:], cmap=plt.cm.gray)
plt.show()
'''
https://stackoverflow.com/questions/59690451/how-to-turn-ct-segmentation-into-3d-model-in-python
For new folks stumbling upon this question that are looking to convert pixels / voxels to an STL file or files, this Python workflow has worked for me:

    Load stack of images as a 3D NumPy array using imageio.imread().
    Segment the foreground from the background using one of the many segmentation algorithms from the scikit-image submodule skimage.segmentation, creating a 3D binary image.
    Use the marching cubes algorithm from the scikit-image submodule skimage.measure to convert the voxels of interest to a list of faces defined by vertices on the surface of the volume.
    Use numpy-stl to create an stl.Mesh object from the list of faces and vertices (as done in this example) then save the mesh with stl.Mesh.save().

As a bonus, you can use the Python package for the Open3D library to open & view multiple STL files!
'''

...



