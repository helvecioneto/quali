import numpy as np
import math
import os
import sys
import csv

np.seterr(all='ignore')

clearsky = []
code_list = []

stations = {
    'BAB': [-1.9311, -59.4197],
    'BJL': [-13.2335, -43.3760],
    'BRB': [-15.6008, -47.7131],
    'CPA': [-22.6896, -45.0062],
    'CAI': [-6.4669, -37.0847],
    'CGR': [-20.4383, -54.5383],
    'CHP': [-27.0800, -52.6144],
    'CBA': [-15.5553, -56.0700],
    'CTB': [-25.4954, -49.3312],
    'FLN': [-27.6017, -48.5178],
    'JOI': [-26.2525, -48.8578],
    'LEB': [-26.9886, -50.7150],
    'MCL': [-16.6864, -43.8688],
    'NAT': [-5.8367, -35.2064],
    'ORN': [-22.9486, -49.8942],
    'PMA': [-10.1778, -48.3619],
    'PTR': [-9.0689, -40.3197],
    'RLM': [-11.5817, -61.7736],
    'SLZ': [-2.5933, -44.2122],
    'SMS': [-29.4428, -53.8231],
    'SBR': [-29.0956, -49.8133],
    'TMA': [-5.3829, -36.8191],
    'TLG': [-20.7507, -51.6642],
    'UBE': [-19.998, -47.900],
}

# Constant values used to get solar geometry data
d0 = 0.006918
dc1 = 0.399912
dc2 = 0.006758
dc3 = 0.002697
ds1 = 0.070257
ds2 = 0.000907
ds3 = 0.001480
et0 = 0.000075
tc1 = 0.001868
tc2 = 0.014615
ts1 = 0.032077
ts2 = 0.040890
e1 = 1.000110
e2 = 0.034221
e3 = 0.001280
e4 = 0.000719
e5 = 0.000077
CDR = np.pi / 180

# Variables for clear sky model
Isc = 1367.0
Wo = 0.95
Fc = 0.84

if len(sys.argv) == 1:
    directory = '.'
    pathnames = os.listdir('.')
else:
    if sys.argv[1] == '-d':
        directory = './' + sys.argv[2]
        pathnames = os.listdir(directory)
    else:
        directory = '.'
        pathnames = sys.argv[1:]


for path in pathnames:
    if path[7:][:-4] == 'ED':
        data_name = directory + '/' + path
        code_name = directory + '/' + path[:-4] + '_DQC.csv'
        latitude, longitude = stations[path[:3]]
        try:
            with open(os.path.abspath(data_name), 'r') as datafile, open(os.path.abspath(code_name), 'r') as codefile:
                read_data = csv.reader(datafile, delimiter=';')
                read_code = csv.reader(codefile, delimiter=';')
                for data, code in zip(read_data, read_code):
                    code = list(map(int, code))
                    Iglob = -1367
                    num = int(data[3])
                    div = num / 60
                    dia_jul = int(data[2])

                    # Calculating astronomical geometry data
                    day_angle = (2 * np.pi / 365.25 * dia_jul)
                    dec = (d0 - dc1 * np.cos(day_angle) + ds1 * np.sin(day_angle) - dc2 * np.cos(2 * day_angle) + ds2 * np.sin(2 * day_angle) - dc3 * np.cos(3 * day_angle) + ds3 * np.sin(3 * day_angle))
                    eqtime = (et0 + tc1 * np.cos(day_angle) - ts1 * np.sin(day_angle) - tc2 * np.cos(2 * day_angle) - ts2 * np.sin(2 * day_angle)) * 229.18
                    tcorr = (eqtime + 4 * (longitude - 0)) / 60
                    horacorr = tcorr + div
                    hour_angle = (12.00 - horacorr) * 15
                    e0 = e1 + e2 * np.cos(day_angle) + e3 * np.sin(day_angle) + e4 * np.cos(2 * day_angle) + e5 * np.sin(2 * day_angle)
                    u0 = np.sin(dec) * np.sin(latitude * CDR) + np.cos(dec) * np.cos(latitude * CDR) * np.cos(hour_angle * CDR)
                    zenith_angle = (np.arccos(u0)) * 180 / np.pi
                    sa = 1368 * e0

                    # Define vertical ozone layer thickness value (cm)
                    # Iqbal average table (5.3.2)
                    if latitude >= -10:
                        L = 0.24
                    elif -10 > latitude >= -20:
                        L = 0.25
                    elif -20 > latitude >= -30:
                        L = 0.28
                    elif -30 > latitude >= -40:
                        L = 0.30

                    if code[10] == 999 and code[11] == 9 and code[12] == 99:
                        # Relative optical mass applied
                        Mr = 1 / (np.cos(zenith_angle))

                        # Relative optical mass
                        Ma = Mr * (float(data[12]) / 1013.25)

                        # Ozone relative optical path length
                        U3 = L * Mr

                        # Water vapor
                        Ps = np.exp(26.23 - (5416 / float(data[10]) + 273.15))

                        # Precipitable water in terms of relative humidity
                        Pw = 0.493 * (float(data[11]) / 100) * (Ps / (float(data[10]) + 273.15))

                        # Pressure-corrected relative optical path length of precipitable water
                        U1 = Pw * Mr

                        # Transmittance by Rayleigh scattering
                        Tr = np.exp(-0.0903 * (Ma ** 0.84) * (1.0 + Ma - (Ma ** 1.01)))

                        # Transmittance by ozone
                        To = 1 - (0.1611 * U3 * ((1.0 + 139.48 * U3) ** (-0.3035)) - 0.002715 * U3 * ((1.0 + 0.44 * U3 + 0.0003 * (U3 ** 2)) ** (-1)))

                        # Transmittance by uniformely mixed gases
                        Tg = np.exp(-0.0127 * Ma ** 0.26)

                        # Transmittance by water vapor
                        Tw = 1 - 2.4959 * U1 * ((((1.0 + 79.034 * U1) ** 0.6828) + (6.385 * U1)) ** (-1))

                        # Aerosol optical thickness - Kah(0.38)=0.087 and Kah(0.5)=0.069
                        Ka = (0.2758 * 0.087) + (0.35 * 0.069)

                        # Aerosol transmittance
                        Ta = np.exp(-Ka ** 0.0873 * (1.0 + Ka - (Ka ** 0.07088)) * (Ma ** 0.9108))

                        # Ecentricy correction factor of the earth's orbit
                        Eo = 1 + (0.033 * np.cos(((2 * np.pi * dia_jul) / 365)))

                        # Direct normal irradiance
                        Irn = Eo * 0.9751 * Isc * Tr * To * Tg * Tw * Ta

                        # Extraterrestrial irradiance on a horizontal surface
                        Io = Eo * Isc * np.cos(zenith_angle)

                        # Total beam irradiance on a horizontal surface
                        Ib = Irn * np.cos(zenith_angle)

                        # Transmittance of direct radiation due to aerosol absortance
                        Taa = 1 - (1 - Wo) * (1 - Ma + (Ma ** 1.06) * (1 - Ta))

                        # Ration between Ta/Taa
                        Tas = Ta / Taa

                        # Reyleigh-scattered diffuse irradiance
                        Idr = Eo * 0.79 * Isc * (np.cos(zenith_angle)) * To * Tg * Tw * Taa * 0.5 * ((1 - Tr) / (1 - Ma + (Ma ** 1.02)))

                        # Aerosol-scattered diffuse irradiance
                        Ida = Eo * 0.79 * Isc * (np.cos(zenith_angle)) * To * Tg * Tw * Taa * (Fc * (1 - Tas)) / (1 - Ma + (Ma ** 1.02))

                        # Albedo for cloudless sky
                        Pa = 0.0685 + (1 - Fc) * (1 - Tas)

                        # Ground albedo
                        Pg = 0.2

                        # Diffuse irradiance produced by multiple reflections between ground and atmosphere
                        Idm = (Irn * (np.cos(zenith_angle)) + Idr + Ida) * Pg * Pa / (1 - Pg * Pa)

                        # Total diffuse irradiance on a horizontal surface
                        Idiff = Idr + Ida + Idm

                        # Total global irradiance on a horizontal surface
                        Iglob = Ib + Idiff

                        # Validation for global irradiance
                        if code[4] != 3333 and code[4] != -5555 and code[4] != -6999 and code[4] != 552 and code[4] != 529 and \
                                code[4] != 299:
                            if data[4]:
                                if Iglob > 1367 or Idiff <= 0:
                                    code[4] += 2000
                                else:
                                    if float(data[4]) <= Iglob:
                                        code[4] += 9000
                                    else:
                                        code[4] += 2000
                        elif code[4] == 552 or code[4] == 529 or code[4] == 299:
                            code[4] += 5000
                    elif code[4] != 3333 and code[4] != -5555 and code[4] != -6999:
                        code[4] += 5000

                    code_list.append(code)
                    clearsky.append([Iglob, float(data[4])])

                codefile_w = open(os.path.abspath(code_name), 'w')
                clearsky_w = open(directory + '/' + path[:-6] + 'CS.csv', 'w')
                write_code = csv.writer(codefile_w, delimiter=';')
                write_clearsky = csv.writer(clearsky_w, delimiter=';')

                for code, cldata in zip(code_list, clearsky):
                    write_code.writerow(code)
                    if math.isnan(cldata[0]) or cldata[0] > 1367 or cldata[0] < -1367:
                        write_clearsky.writerow([code[0], code[1], code[2], code[3], code[4], 'N/A', f'{cldata[1]:5.3f}'])
                    else:
                        write_clearsky.writerow([code[0], code[1], code[2], code[3], code[4], f'{cldata[0]:5.3f}', f'{cldata[1]:5.3f}'])



        except IOError:
            raise IOError
