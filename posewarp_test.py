import tensorflow as tf
import os
import numpy as np
import sys
import cv2
import datareader
import datageneration
import networks
import scipy.io as sio
import param
from keras.models import load_model,Model
from keras.optimizers import Adam
from keras.applications.vgg19 import VGG19
import h5py
import util

def train(dataset,gpu_id):	

	params = param.getParam(dataset)
	gpu = '/gpu:' + str(gpu_id)

	ex_train,ex_test = datareader.makeWarpExampleList(params)
	test_feed = datageneration.warpExampleGenerator(ex_test,params)
	
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	config.allow_soft_placement = True
	
	#f = h5py.File('../results/networks/gan100/20000.h5', 'r+')
	#del f['optimizer_weights']
	#f.close()

	with tf.Session(config=config) as sess:

		sess.run(tf.global_variables_initializer())
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)

		with tf.device(gpu):
			vgg_model = VGG19(weights='imagenet',include_top=False,input_shape=(128,128,3))
			networks.make_trainable(vgg_model,False)
			generator = networks.network_warp(params,vgg_model)
			#generator.summary()
			#discriminator = networks.discriminator(params)
			#gan = networks.gan(generator,discriminator,params)
			#gan.load_weights('../results/networks/gan/5000.h5')
			#discriminator.compile(loss='binary_crossentropy',optimizer=Adam(lr=1e-4))
			generator.load_weights('../results/networks/L2+VGG_0.001/60000.h5')
			rnn = networks.warp_rnn(params,generator)

		'''
		n_batches = 1
		for j in xrange(n_batches):	

			X,Y = next(test_feed)			
			#X_feat = vgg_model.predict(util.vgg_preprocess(Y))
			#mask = mask.predict(X)
			sio.savemat('test.mat', {'X': X[0], 'pose': X[1], 'mask': X[2], 'trans': X[3],
							'Y': Y})

			#pred = gan.predict([X_src,X_pose,X_mask,X_trans])
			#print pred[2]
			#y = np.zeros((8,2))
			#y[:,0] = 1
			#gan_loss = gan.train_on_batch([X_src,X_pose,X_mask,X_trans],[X_tgt,X_feat,y])

			#test_loss = discriminator.test_on_batch([X_src,X_tgt,X_pose],y)		
			#pred = discriminator.predict([X_src,X_tgt,X_pose])

			#print pred
			#print test_loss

			#I_warp = model_warp.predict([X_src,X_pose,X_mask])
			#I_gan = model_gan.predict([X_src,X_pose,X_mask])
			#I_mask = model_mask.predict([X_src,X_pose,X_mask])	

			#sio.savemat('tests/' + str(j) + '.mat',
         	#{'X_src': X_src,'X_tgt': X_tgt, 'mask0': X_mask, 'mask1': I_mask}), 
			#	'I_warp': I_warp}) #, 'I_gan': I_gan[0]})	
		'''
if __name__ == "__main__":
	train('golfswinghd',sys.argv[1])
