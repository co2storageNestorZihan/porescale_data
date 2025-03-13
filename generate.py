#%%
import porespy as ps
import numpy as np
from skimage.io import imsave

# generate 9 random blob networks porosity ranging from 0.1 to 0.9
# save the images to sample_blobs folder with porosity as the file name
# sample sequentially from 0.1 to 0.9
for porosity in np.arange(0.1, 1.0, 0.1):
    blob_network = ps.generators.blobs(shape=[80, 80], porosity=porosity)
    imsave(f'sample_blobs/blob_network_{porosity:.1f}.png', blob_network.astype(np.uint8)*255)

# %% code for validation
# generate a random 3D network
blob_3d = ps.generators.blobs(shape=[80, 80, 80], porosity=0.5)
np.save('sample_blobs/binary_3d.npy', blob_3d)


# generate a random blob network
# blob_network = ps.generators.blobs(shape=[80, 80], porosity=0.5)
# print(f'porosity: {ps.metrics.porosity(blob_network)}')
# # visualize the image
# f = plt.figure()
# plt.imshow(blob_network,cmap='gray')
# plt.axis('off')

# imsave('blob_network.png', blob_network.astype(np.uint8)*255)

# # %%
# sample_image = plt.imread('blob_network.png')
# # make sample image boolean
# sample_image = sample_image.astype(bool)
# f = plt.figure()
# plt.imshow(sample_image,cmap='gray')
# plt.axis('off')
# print(f'porosity: {ps.metrics.porosity(sample_image)}')
# %%
