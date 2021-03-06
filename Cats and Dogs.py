# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iIhIdGtoguwm8rdrRCKI7Fiiffo32M-r
"""

pip install tensorflow-gpu==2.4.0



pip install mlxtend==0.17.0

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPool2D, Dropout

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from tensorflow.keras.datasets import cifar10

(X_train, y_train), (X_test, y_test) = cifar10.load_data()

classes_name = ['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']

X_train.max()

X_train = X_train/255
X_test = X_test/255

X_train.shape

plt.imshow(X_test[0])

y_test[0]

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3,3),padding='same',activation='relu', input_shape = [32,32,3]))

model.add(Conv2D(filters=32, kernel_size=(3,3),padding='same',activation='relu'))
model.add(MaxPool2D(pool_size=(2,2),strides=2,padding='valid'))
model.add(Dropout(0.5))
# Keep on adding 
model.add(Flatten())
model.add(Dense(units=128, activation= 'relu'))
model.add(Dense(units=10, activation='softmax'))

model.summary()

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['sparse_categorical_accuracy'])

history = model.fit(X_train, y_train, batch_size=10, epochs=2, verbose=1, validation_data=(X_test, y_test))

history.history

#Plot training and validationa accuracy values
epoch_range = range(1,3)
plt.plot(history.history['sparse_categorical_accuracy'])
plt.plot(history.history['val_sparse_categorical_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()

#Plot training and validationa loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()

from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix

y_pred = model.predict_classes(X_test)
y_pred

y_test

mat = confusion_matrix(y_test, y_pred)

mat

plot_confusion_matrix(mat, figsize=(9,9), class_names = classes_name, show_normed=True)

"""Use of Dropout and batch normalization"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPool2D, Dropout, ZeroPadding2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.optimizers import SGD

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

!git clone https://github.com/laxmimerit/dog-cat-full-dataset.git

test_data_dir = '/content/dog-cat-full-dataset/data/test'
train_data_dir = '/content/dog-cat-full-dataset/data/train'

img_width = 32
img_height = 32
batch_size = 20

datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_directory(directory=train_data_dir, target_size= (img_width, img_height), 
                                              classes =['dogs','cats'],
                                              class_mode = 'binary',
                                              batch_size = batch_size)

train_generator.classes

validation_generator = datagen.flow_from_directory(directory=test_data_dir, target_size= (img_width, img_height), 
                                              classes =['dogs','cats'],
                                              class_mode = 'binary',
                                              batch_size = batch_size)

len(train_generator)

"""## CNN Base model"""

model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(3,3),padding='same',kernel_initializer='he_uniform', input_shape = (img_width, img_height,3)))
model.add(MaxPool2D(2,2))

model.add(Flatten())
model.add(Dense(units=128, activation= 'relu',kernel_initializer='he_uniform'))
model.add(Dense(1, activation='sigmoid'))

opt = SGD(learning_rate=0.01, momentum=0.9)
model.compile(optimizer=opt, loss = 'binary_crossentropy', metrics= ['accuracy'])

history = model.fit_generator(generator=train_generator, steps_per_epoch=len(train_generator), epochs = 3,validation_data=validation_generator, validation_steps=len(validation_generator),verbose = 1)

history.history

#Plot training and validationa accuracy values 
epoch_range= range(1,3)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()

#Plot training and validationa loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()



"""## Implement first 3 blocks of VGG16 Model"""

model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform', input_shape = (img_width, img_height,3)))
model.add(MaxPool2D(2,2))

model = Sequential()
model.add(Conv2D(filters=128, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform'))
model.add(MaxPool2D(2,2))

model = Sequential()
model.add(Conv2D(filters=256, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform'))
model.add(MaxPool2D(2,2))

model.add(Flatten())
model.add(Dense(units=128, activation= 'relu',kernel_initializer='he_uniform'))
model.add(Dense(1, activation='sigmoid'))

opt = SGD(learning_rate=0.01, momentum=0.9)
model.compile(optimizer=opt, loss = 'binary_crossentropy', metrics= ['accuracy'])

history = model.fit_generator(generator=train_generator, steps_per_epoch=len(train_generator), epochs = 3,validation_data=validation_generator, validation_steps=len(validation_generator),verbose = 1)

"""## Add batch normalisation and drop out to improve accuracy"""

model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform', input_shape = (img_width, img_height,3)))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.2))

model = Sequential()
model.add(Conv2D(filters=128, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.3))

model = Sequential()
model.add(Conv2D(filters=256, kernel_size=(3,3),activation= 'relu',padding='same',kernel_initializer='he_uniform'))
model.add(BatchNormalization())
model.add(MaxPool2D(2,2))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(units=128, activation= 'relu',kernel_initializer='he_uniform'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))

opt = SGD(learning_rate=0.01, momentum=0.9)
model.compile(optimizer=opt, loss = 'binary_crossentropy', metrics= ['accuracy'])

history = model.fit_generator(generator=train_generator, steps_per_epoch=len(train_generator),epochs = 3,validation_data=validation_generator, validation_steps=len(validation_generator),verbose = 1)

"""## Breast Cancer Analysis"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv2D, MaxPool2D, Dropout, ZeroPadding2D, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.optimizers import Adam

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

cancer = datasets.load_breast_cancer()

print(cancer.DESCR)

X = pd.DataFrame(data=cancer.data, columns=cancer.feature_names)
X.head()

y = cancer.target
y

cancer.target_names

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =0.2, random_state = 0, stratify=y)

X_train.shape,X_test.shape, y_train.shape, y_test.shape  #For Neural networks bring the data in 3d)

scaler = StandardScaler()
X_train= scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

X_train = X_train.reshape(455,30,1)
X_test = X_test.reshape(114,30,1)

epochs=50
model=Sequential()
model.add(Conv2D(filters=32, kernel_size=2, activation='relu',input_shape=(114,30,1)))
model.add(BatchNormalization())
model.add(Dropout(0.2))

model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(64,activation='relu',))
model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer=Adam(learning_rate=0.00005), loss = 'binary_crossentropy', metrics=['accuracy'])

history=model.fit(X_train,y_train, epochs=10, validation_data=(X_test,y_test), verbose=1 )



""" Bank Customer Satisfaction Prediction Using CNN"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout, ZeroPadding1D, BatchNormalization
from tensorflow.keras.optimizers import Adam

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.feature_selection import VarianceThreshold



"""Bank Customer Satisfaction Prediction Using CNN"""



"""# Bank Customer Satisfaction Prediction Using CNN"""

!git clone https://github.com/laxmimerit/Data-Files-for-Feature-Selection

data = pd.read_csv('/content/Data-Files-for-Feature-Selection/santander-train.csv')

data.head()

data.shape

X = data.drop(labels=['ID','TARGET'],axis=1)

X.shape

y = data['TARGET']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =0.2, random_state = 0, stratify=y)

X_train.shape, X_test.shape

"""## Remove constant, Quasi constant, duplicates"""

filter = VarianceThreshold(0.01)

X_train = filter.fit_transform(X_train)
X_test = filter.transform(X_test)

X_train.shape, X_test.shape

X_train_t = X_train.T
X_test_t = X_test.T

X_train_t = pd.DataFrame(X_train_t)
X_test_t = pd.DataFrame(X_test_t)

X_train_t.shape

X_train_t.duplicated().sum()

duplicated_features = X_train_t.duplicated()
duplicated_features

featurestokeep = [not index for index in duplicated_features]
featurestokeep

X_train = X_train_t[featurestokeep].T
X_train.shape

X_test = X_test_t[featurestokeep].T
X_test.shape

X_train.head()

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train

X_train.shape, X_test.shape

X_train = X_train.reshape(60816, 256, 1)
X_test = X_test.reshape(15204, 256, 1)

y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

model = Sequential()
model.add(Conv1D(32,3, activation='relu', input_shape=(256,1)))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.3))

model.add(Conv1D(64,3, activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.5))


model.add(Conv1D(128,3, activation='relu', input_shape=(256,1)))
model.add(BatchNormalization())
model.add(MaxPool1D(2))
model.add(Dropout(0.3))

model.add(Flatten())   #Converts into vector
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer=Adam(lr=0.00005),loss = 'binary_crossentropy',metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs = 3, validation_data=(X_test, y_test), verbose =1)

history.history

#Plot training and validationa accuracy values 
epoch_range= range(1,4)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()

#Plot training and validationa loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc = 'upper left')
plt.show()



"""# LSTM IMDB Review"""

