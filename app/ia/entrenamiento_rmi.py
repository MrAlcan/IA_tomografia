import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm import tqdm
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, TensorBoard, ModelCheckpoint
from sklearn.metrics import classification_report,confusion_matrix
import ipywidgets as widgets
import io
from PIL import Image
from IPython.display import display,clear_output
from warnings import filterwarnings

etiquetas = ['sin_tumor','con_tumor']

X_entrenamiento = []
y_entrenamiento = []
tamano_imagen = 150
for i in etiquetas:
    direccion_carpeta = os.path.join('./resonancia','Entrenamiento',i)
    for j in tqdm(os.listdir(direccion_carpeta)):
        imagen = cv2.imread(os.path.join(direccion_carpeta,j))
        imagen = cv2.resize(imagen,(tamano_imagen, tamano_imagen))
        X_entrenamiento.append(imagen)
        y_entrenamiento.append(i)
        
for i in etiquetas:
    direccion_carpeta = os.path.join('./resonancia','Pruebas',i)
    for j in tqdm(os.listdir(direccion_carpeta)):
        imagen = cv2.imread(os.path.join(direccion_carpeta,j))
        imagen = cv2.resize(imagen,(tamano_imagen,tamano_imagen))
        X_entrenamiento.append(imagen)
        y_entrenamiento.append(i)
        
X_entrenamiento = np.array(X_entrenamiento)
y_entrenamiento = np.array(y_entrenamiento)

colores_oscuros = ["#1F1F1F", "#313131", '#636363', '#AEAEAE', '#DADADA']
colores_rojos = ["#331313", "#582626", '#9E1717', '#D35151', '#E9B4B4']
colores_verdes = ['#01411C','#4B6F44','#4F7942','#74C365','#D0F0C0']
k=0
figura, ax = plt.subplots(1,4,figsize=(20,20))
figura.text(s='Imagen de muestra de cada etiqueta',size=18,fontweight='bold',
             fontname='monospace',color=colores_oscuros[1],y=0.62,x=0.4,alpha=0.8)
for i in etiquetas:
    j=0
    while True :
        if y_entrenamiento[j]==i:
            ax[k].imshow(X_entrenamiento[j])
            ax[k].set_title(y_entrenamiento[j])
            ax[k].axis('off')
            k+=1
            break
        j+=1
X_entrenamiento, y_entrenamiento = shuffle(X_entrenamiento,y_entrenamiento, random_state=101)
X_entrenamiento.shape

X_entrenamiento,X_test,y_entrenamiento,y_pruebas = train_test_split(X_entrenamiento,y_entrenamiento, test_size=0.1,random_state=101)
y_nuevo_entrenamiento = []
for i in y_entrenamiento:
    y_nuevo_entrenamiento.append(etiquetas.index(i))
y_entrenamiento = y_nuevo_entrenamiento
y_entrenamiento = tf.keras.utils.to_categorical(y_entrenamiento)
y_nuevo_pruebas = []
for i in y_pruebas:
    y_nuevo_pruebas.append(etiquetas.index(i))
y_pruebas = y_nuevo_pruebas
y_pruebas = tf.keras.utils.to_categorical(y_pruebas)

effnet = EfficientNetB0(weights='imagenet',include_top=False,input_shape=(tamano_imagen,tamano_imagen,3))
modelo = effnet.output
modelo = tf.keras.layers.GlobalAveragePooling2D()(modelo)
modelo = tf.keras.layers.Dropout(rate=0.5)(modelo)
modelo = tf.keras.layers.Dense(2,activation='softmax')(modelo)
modelo = tf.keras.models.Model(inputs=effnet.input, outputs = modelo)
modelo.summary()

modelo.compile(loss='categorical_crossentropy',optimizer = 'Adam', metrics= ['accuracy'])
tensorboard = TensorBoard(log_dir = 'logs')
punto_control = ModelCheckpoint("deteccion_tumor.keras",monitor="val_accuracy",save_best_only=True,mode="auto",verbose=1)
reducir_lr = ReduceLROnPlateau(monitor = 'val_accuracy', factor = 0.3, patience = 2, min_delta = 0.001,
                              mode='auto',verbose=1)
historia = modelo.fit(X_entrenamiento,y_entrenamiento,validation_split=0.1, epochs =12, verbose=1, batch_size=32,
                   callbacks=[tensorboard,punto_control,reducir_lr])
filterwarnings('ignore')

epocas = [i for i in range(12)]
figura, ax = plt.subplots(1,2,figsize=(14,7))
exactitud_entrenamiento = historia.history['accuracy']
perdida_entrenamiento = historia.history['loss']
exactitud_valoracion = historia.history['val_accuracy']
perdida_valoracion = historia.history['val_loss']

figura.text(s='Entrenamiento vs. Entrenamiento y Validacion Exactitud/Perdida',size=18,fontweight='bold',
             fontname='monospace',color=colores_oscuros[1],y=1,x=0.28,alpha=0.8)

sns.despine()
ax[0].plot(epocas, exactitud_entrenamiento, marker='o',markerfacecolor=colores_verdes[2],color=colores_verdes[3],
           label = 'Exactitud Entrenamiento')
ax[0].plot(epocas, exactitud_valoracion, marker='o',markerfacecolor=colores_rojos[2],color=colores_rojos[3],
           label = 'Exactitud Validacion')
ax[0].legend(frameon=False)
ax[0].set_xlabel('Epocas')
ax[0].set_ylabel('Exactitud')

sns.despine()
ax[1].plot(epocas, perdida_entrenamiento, marker='o',markerfacecolor=colores_verdes[2],color=colores_verdes[3],
           label ='Perdida Entrenamiento')
ax[1].plot(epocas, perdida_valoracion, marker='o',markerfacecolor=colores_rojos[2],color=colores_rojos[3],
           label = 'Perdida Validacion')
ax[1].legend(frameon=False)
ax[1].set_xlabel('Epocas')
ax[1].set_ylabel('Perdida de Entrenamiento y Validacion')

figura.show()

prediccion = modelo.predict(X_test)
prediccion = np.argmax(prediccion,axis=1)
y_nuevo_pruebas = np.argmax(y_pruebas,axis=1)

print(classification_report(y_nuevo_pruebas,prediccion))

figura,ax=plt.subplots(1,1,figsize=(14,7))
sns.heatmap(confusion_matrix(y_nuevo_pruebas,prediccion),ax=ax,xticklabels=etiquetas,yticklabels=etiquetas,annot=True,
           cmap=colores_verdes[::-1],alpha=0.7,linewidths=2,linecolor=colores_oscuros[3])
figura.text(s='Mapa de la Matriz de Confusion',size=18,fontweight='bold',
             fontname='monospace',color=colores_oscuros[1],y=0.92,x=0.28,alpha=0.8)

plt.show()
