# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:18:05 2019

@author: Thaiane Gambarra
"""
import os
import matplotlib as mp
import numpy as np

def processamento_imagens(longitude,latitude):
    ###############################################
    # DIRETÓRIO ONDE ESTÃO LOCALIZADAS AS IMAGENS #
    ###############################################

    os.chdir('C:\\Users\\Thaiane Gambarra\\Desktop\\ClearSky\\Dumortier\\Input')
    listar_arquivos = os.listdir('.')
    arquivo=[]

    for nomes in listar_arquivos:
        if nomes.endswith('.tif'):
            arquivo.append(nomes)

    turbidity_values=np.zeros(len(arquivo))

    for a in range(len(arquivo)):
        I= mp.pyplot.imread(arquivo[a])
        [m,k] = I.shape
        bin_lat=180/m
        bin_lon=360/k
        lat= np.arange(90,-90,-bin_lat)
        lon= np.arange(-180,180,bin_lon)

        [linha] = np.where(latitude == lat)
        if linha.size == 0:
            lat_lin_maior = np.where(lat<latitude)
            lat_val_maior = lat[lat_lin_maior]
            lat_val_maior = lat_val_maior[0]
            lat_div_maior = lat_val_maior - latitude

            lat_lin_menor = np.where(lat > latitude)
            lat_val_menor = lat[lat_lin_menor]
            lat_val_menor = lat_val_menor[len(lat_val_menor)-1]
            lat_div_menor = latitude - lat_val_menor
            if lat_div_menor <= lat_div_maior:
                lat_s = lat_val_maior
            else:
                lat_s = lat_val_menor
        else:
            lat_s = lat[linha]

        [coluna] = np.where(longitude == lon)
        if coluna.size == 0:
            lon_lin_maior = np.where(lon<longitude)
            lon_val_maior = lon[lon_lin_maior]
            lon_val_maior = lon_val_maior[len(lon_val_maior)-1]
            lon_div_maior = lon_val_maior - longitude

            lon_lin_menor = np.where(lon > longitude)
            lon_val_menor = lon[lon_lin_menor]
            lon_val_menor = lon_val_menor[0]
            lon_div_menor = longitude - lon_val_menor
            if lon_div_menor <= lon_div_maior:
                lon_s = lon_val_maior
            else:
                lon_s = lon_val_menor
        else:
            lon_s = lon[linha]

        [linha] = np.where(lat_s == lat)
        [coluna] = np.where(lon_s == lon)
        turbidity_values[a] = float(I[linha,coluna])
        turbidity = dict(zip(arquivo,turbidity_values))
        return turbidity
