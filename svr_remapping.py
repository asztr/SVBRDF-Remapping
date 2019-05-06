import pandas as pd
import numpy as np
import pyexr

from sklearn.svm import SVR
from scipy.optimize import least_squares
import os, sys
import time
import pickle

mpl.rcParams['lines.markersize'] = 4


df = pd.read_csv('mitsuba-ward2mitsuba-as.csv', sep='\t')

srccol_a = 'alpha1'
srccol_s = 'specular1'

tgtcol_a = 'alpha2'
tgtcol_s = 'eta2'

#split between train and test data 80% and 20%
msk = np.random.rand(len(df)) < 0.8
traindf = df.copy()[msk]
testdf = df.copy()[~msk]

traindf = traindf.sort_values([srccol_a, srccol_s])

def error_of_f0_regression(x): #epsilon=1e-4
	f0fit = SVR(kernel='rbf', C=x[0]*100, gamma=x[1], epsilon=epsilonf0).fit(traindf[[srccol_a, srccol_s]], traindf[tgtcol_s])
	testdf['svr_'+tgtcol_s] = f0fit.predict(testdf[[srccol_a, srccol_s]])
	cost = np.linalg.norm(testdf[tgtcol_s].values-testdf['svr_'+tgtcol_s].values)
	sys.stdout.write('\r'+'loss:'+str(cost))
	time.sleep(0.5)
	return cost

def error_of_alpha_regression(x):
	alphafit = SVR(kernel='rbf', C=x[0]*100, gamma=x[1], epsilon=epsilonalpha).fit(traindf[[srccol_a, srccol_s]], traindf[tgtcol_a])
	testdf['svr_'+tgtcol_a] = alphafit.predict(testdf[[srccol_a, srccol_s]])
	cost = np.linalg.norm(testdf[tgtcol_a].values-testdf['svr_'+tgtcol_a].values)
	sys.stdout.write('\r'+'loss:'+str(cost))
	time.sleep(0.5)
	return cost

f0_pickle = 'f0fit.pickle'
if (os.path.exists(f0_pickle)):
	print('reading f0 svr fit from', f0_pickle)
	f0fit = pickle.load(open(f0_pickle, 'rb'))
else:
	epsilonf0 = 1e-4
	diff_step = 0.05
	x0 = np.array([1, 1]) #C, gamma

	print(f0_pickle, 'not found. Starting f0 optimization.')

	res_f0 = least_squares(error_of_f0_regression, x0, bounds=([0.001, 0.001], [1e5, 1e5]), diff_step=diff_step)
	print('res_f0: ', res_f0.x, 'cost = ', res_f0.cost)
	f0fit = SVR(kernel='rbf', C=res_f0.x[0]*100, gamma=res_f0.x[1], epsilon=epsilonf0).fit(df[[srccol_a, srccol_s]], df[tgtcol_s])
	df['svr_'+tgtcol_s] = f0fit.predict(df[[srccol_a, srccol_s]])
	pickle.dump(f0fit, open(f0_pickle, 'wb'))
	print('wrote ', f0_pickle)

alpha_pickle = 'alphafit.pickle'
if (os.path.exists(alpha_pickle)):
	print('reading roughness svr fit from', alpha_pickle)
	alphafit = pickle.load(open(alpha_pickle, 'rb'))
else:
	epsilonalpha = 5e-4
	diff_step = 0.05
	x0 = np.array([1, 1]) #C, gamma

	print(alpha_pickle, 'not found. Starting alpha (roughness) optimization.')

	res_alpha = least_squares(error_of_alpha_regression, x0, bounds=([0.001, 0.001], [1e5, 1e5]), diff_step=diff_step)
	print('res_alpha: ', res_alpha.x, 'cost = ', res_alpha.cost)
	alphafit = SVR(kernel='rbf', C=res_alpha.x[0]*100, gamma=res_alpha.x[1], epsilon=epsilonalpha).fit(df[[srccol_a, srccol_s]], df[tgtcol_a])
	df['svr_'+tgtcol_a] = alphafit.predict(df[[srccol_a, srccol_s]])
	pickle.dump(alphafit, open(alpha_pickle, 'wb'))

#read textures
im_alpha = pyexr.read('roughness.exr')
im_spec = pyexr.read('specular.exr')

#remap alpha
tmpcols = np.array([im_alpha.ravel(), im_spec.ravel()])
tmpcols = np.swapaxes(tmpcols, 0, 1)
remapped_alpha = alphafit.predict(tmpcols)
remapped_alpha.shape = im_alpha.shape
remapped_alpha = remapped_alpha.astype('float32')
pyexr.write('svr_roughness_as_remapped.exr', remapped_alpha, channel_names=['R', 'G', 'B'])
print('wrote svr_roughness_as_remapped.exr')

#remap specular
tmpcols = np.array([im_alpha.ravel(), im_spec.ravel()])
tmpcols = np.swapaxes(tmpcols, 0, 1)
remapped_f0 = f0fit.predict(tmpcols)
remapped_f0.shape = im_spec.shape
remapped_f0 = remapped_f0.astype('float32')
pyexr.write('svr_specular_as_remapped.exr',remapped_f0, channel_names=['R', 'G', 'B'])
print('wrote svr_specular_as_remapped.exr')

