import os
import numpy as np
import matplotlib.pyplot as plt

def image_turbidity(latitude, longitude):
    # Mudar diretório para images
    os.chdir('./images')
    file_list = os.listdir('.')
    files = []

    for name in file_list:
        if name.endswith('.tif'):
            files.append(name)

    turbidity_values = np.zeros(len(files))

    for f in range(len(files)):
        img = plt.imread(files[f])
        [m,k] = img.shape
        bin_lat = 180/m
        bin_lon = 360/k
        lat = np.arange(90, -90+1, -bin_lat)
        lon = np.arange(-180, 180+1, bin_lon)

        [row] = np.where(latitude == lat)
        if row.size == 0:
            lat_row_major = np.where(lat < latitude)
            lat_val_major = lat[lat_row_major]
            lat_val_major = lat_val_major[0]
            lat_div_major = lat_val_major - latitude

            lat_row_minor = np.where(lat > latitude)
            lat_val_minor = lat[lat_row_minor]
            lat_val_minor = lat_val_minor[len(lat_val_minor)-1]
            lat_div_minor = latitude - lat_val_minor

            if lat_div_minor <= lat_div_major:
                lat_s = lat_val_major
            else:
                lat_s = lat_val_minor
        else:
            lat_s = lat[row]

        [col] = np.where(longitude == lon)
        if col.size == 0:
            lon_row_major = np.where(lon < longitude)
            lon_val_major = lon[lon_row_major]
            lon_val_major = lon_val_major[len(lon_val_major)-1]
            lon_div_major = lon_val_major - longitude

            lon_row_minor = np.where(lon > longitude)
            lon_val_minor = lon[lon_row_minor]
            lon_val_minor = lon_val_minor[0]
            lon_div_minor = longitude - lon_val_minor

            if lon_div_minor <= lon_div_major:
                lon_s = lon_val_major
            else:
                lon_s = lon_val_minor
        else:
            lon_s = lon[row]

        [row] = np.where(lat_s == lat)
        [col] = np.where(lon_s == lon)
        turbidity_values[f] = float(img[row, col])
        turbidity = dict(zip(files, turbidity_values))
    os.chdir('../')
    return turbidity
