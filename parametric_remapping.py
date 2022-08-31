import pandas as pd
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
import scipy.optimize
import pyexr

ddf = pd.read_csv('mitsuba-ward2mitsuba-beck.csv', sep='\t')

srccol_a = 'alpha1'
srccol_s = 'specular1'

tgtcol_a = 'alpha2'
tgtcol_s = 'eta2'

def slope_func(x, a0, a1, a2, a3, a4, a5): 
    return a0 + a1*np.exp(-a2*x) + a3*np.exp(-a4*x**2) + a5/x

def alpha_func(x, a0, a1, a2, a3):
    return a0*x + a1*x**2 + a2*x**3 + a3*x**4

def linear_func(x, a0):
    return a0*x

#split between train and test data 80% and 20%
msk = np.random.rand(len(ddf)) < 0.8
traindf = ddf.copy()[msk]
testdf = ddf.copy()[~msk]

traindf = traindf.sort_values([srccol_a, srccol_s])

#alpha fit
_x = traindf[srccol_a]
_y = traindf[tgtcol_a]
alpha_params, pcov = scipy.optimize.curve_fit(alpha_func, _x, _y, p0=(1,1,1,1), maxfev=20000)

#alpha plot
plt.scatter(_x, _y, color='black')
plt.plot(_x, alpha_func(_x, *alpha_params), color='red')
plt.xlabel('Mitsuba Ward roughness')
plt.ylabel('Mitsuba Beckmann roughness')
plt.savefig('roughness_vs_roughness.jpg', dpi=150)
print('wrote roughness_vs_roughness.jpg')
plt.clf()

#specular fit and plot (and compute slope)
slopes = []
alphas = np.sort(traindf[srccol_a].unique())
for alpha in alphas:
    alpha_df = traindf[traindf[srccol_a] == alpha]
    _x = alpha_df[srccol_s].values
    _y = alpha_df[tgtcol_s].values
    specular_params, pcov = scipy.optimize.curve_fit(linear_func, _x, _y, p0=(1))
    slopes += [specular_params[0]]
    plt.plot(_x, linear_func(_x, *specular_params), color='red')
    plt.scatter(_x, _y, color='black')
plt.xlabel('Mitsuba Ward specular reflectance')
plt.ylabel('Mitsuba Beckmann F0')
plt.savefig('specular_vs_specular.jpg', dpi=150)
print('wrote specular_vs_specular.jpg')
plt.clf()

#slope fit and plot
_x = alphas[1:]
_y = slopes[1:]
slope_params, pcov = scipy.optimize.curve_fit(slope_func, _x, _y, p0=(1, 1, 1, 1, 1, 1), maxfev=10000)

#print resulting parameters
print('alpha parameters:', alpha_params)
print('slope parameters:', slope_params)

#read textures
im_alpha = pyexr.read('roughness.exr')
im_spec = pyexr.read('specular.exr')

#remap alpha
remapped_alpha = alpha_func(im_alpha.ravel(), *alpha_params)
remapped_alpha.shape = im_alpha.shape
remapped_alpha = remapped_alpha.astype('float32')
pyexr.write('roughness_beck_remapped.exr', remapped_alpha, channel_names=['R', 'G', 'B'])
print('wrote roughness_beck_remapped.exr')

#remap specular
remapped_f0 = slope_func(im_alpha.ravel(), *slope_params)*im_spec.ravel()
remapped_f0.shape = im_spec.shape
remapped_f0 = remapped_f0.astype('float32')
pyexr.write('specular_beck_remapped.exr',remapped_f0, channel_names=['R', 'G', 'B'])
print('wrote specular_beck_remapped.exr')

