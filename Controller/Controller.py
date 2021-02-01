import os
import numpy as np

from tqdm import *

from Loader import Loader

class Controller:
    def __init__(self, input1=None, input2=None):
        # Constant values used to get solar geometry data
        self.d0 = 0.006918
        self.dc1 = 0.399912
        self.dc2 = 0.006758
        self.dc3 = 0.002697
        self.ds1 = 0.070257
        self.ds2 = 0.000907
        self.ds3 = 0.001480
        self.et0 = 0.000075
        self.tc1 = 0.001868
        self.tc2 = 0.014615
        self.ts1 = 0.032077
        self.ts2 = 0.040890

        self.e1 = 1.000110
        self.e2 = 0.034221
        self.e3 = 0.001280
        self.e4 = 0.000719
        self.e5 = 0.000077

        # Threshold values used to qualify solar and meteorological data  - level 1
        self.HUMI_MX = 100
        self.HUMI_MI = 0

        self.PRES_MX = None
        self.PRES_MI = None

        self.TEMP_MX = None
        self.TEMP_MI = None

        self.PREC_MX = None
        self.PREC_MI = 0

        self.WS10_MX = 25
        self.WS10_MI = 0

        self.WD10_MX = 360
        self.WD10_MI = 0

        # BSRN criteria for solar data qualification
        self.LWDN_MX = 700
        self.LWDN_MI = 40

        self.GLOBAL_MX = None
        self.GLOBAL_MI = -4

        self.DIFUSE_MX = None
        self.DIFUSE_MI = -4

        self.DIRECT_MX = None
        self.DIRECT_MI = -4

        self.PAR_MX = None
        self.PAR_MI = -4

        self.LUX_MX = None
        self.LUX_MI = -4

        # Variables used to validate meteorological data  - levels 2 and  3
        self.temp_max = 0
        self.temp_min = 999
        self.temp1h = 59
        self.temp12h = 719
        self.variation_temp1h = None
        self.variation_temp12h = None

        self.pres_max = 0
        self.pres_min = 999
        self.pres3h = 179
        self.variation_pres3h = None

        self.prec_max = 0
        self.prec_min = 999
        self.prec1h = 59
        self.prec24h = 1439
        self.variation_prec1h = None
        self.variation_prec24h = None

        self.ws10_max = 0
        self.ws10_min = 999
        self.ws103h = 179
        self.ws1012h = 719
        self.variation_ws103h = None
        self.variation_ws1012h = None

        self.wd10_max = 0
        self.wd10_min = 999
        self.wd103h = 179
        self.wd1018h = 1079
        self.variation_wd103h = None
        self.variation_wd1018h = None

        # Variables used to get solar geometry data
        self.e0 = None
        self.u0 = None              # Cosine of solar zenith angle
        self.zenith_angle = None    # Zenith angle
        self.rtoa = None            # Solar Irradiation at the top of atmosphere
        self.sa = None
        self.day_angle = None       # Diary angle
        self.dec = None             # Declination angle
        self.eqtime = None          # Equation time
        self.tcorr = None           # Time correction
        self.hour_angle = None      # Hour angle

        # Other variables
        self.CDR = np.pi / 180
        self.rows = None        # total file lines
        self.cont = 0           # Count rows number
        self.num = None         # Measurement time in minutes
        self.dia_jul = None     # Day number
        self.horacorr = None    # Time correction considering longitude data for the measurement site
        self.div = None         # Measurement time in decimal hours
        self.i = None
        self.cont_std = 0

        self.pb = None
        self.dialog = None
        self.title = None

        # Variables used to count meteorological data valid - level 2 and 3
        self.contTempValid = 0
        self.contPresValid = 0
        self.contPrecValid = 0
        self.contWspdValid = 0
        self.contWdirValid = 0

        # Variables used to save the last valid meteorological data - level 2 and 3
        self.lastTempValid = None
        self.lastPresValid = None
        self.lastPrecValid = None
        self.lastWs10Valid = None
        self.lastWd10Valid = None

        # Variables for clear sky model
        self.Isc = 1367.0
        self.Wo = 0.95
        self.Fc = 0.84
        self.Iglob = None
        self.porc = None


        self.kt = None
        self.kn = None

        self.loader = None

        if input1 is not None:
            self.loader = Loader.Loader()
            self.loader.buildsMatrixData(input1)
            self.loader.buildsMatrixCode(input1)



        if input2 is not None:
            self.title = input2

    def progressBar(self):
        self.pb = tqdm(total=self.rows*4, desc="Validação - "+self.title)

    def validate(self, latitude, longitude, station, month):
        self.rows = self.loader.getRows() - 1
        self.progressBar()

        for i in range(self.rows+1):

            # Funções de atribuição repetidas a cada nível de validação - talvez não necessário
            self.num = self.loader.data[i][3]
            self.div = self.num / 60    # Measurement time in utc time
            self.dia_jul = int(self.loader.data[i][2])

            # Calculating astronomical data
            self.day_angle = (2 * np.pi / 365.25 * self.dia_jul)
            self.dec = (self.d0 - self.dc1 * np.cos(self.day_angle) + self.ds1 * np.sin(self.day_angle) - self.dc2 * np.cos(2 * self.day_angle) + self.ds2 * np.sin(2 * self.day_angle) - self.dc3 * np.cos(3 * self.day_angle) + self.ds3 * np.sin(3 * self.day_angle))
            self.eqtime = (self.et0 + self.tc1 * np.cos(self.day_angle) - self.ts1 * np.sin(self.day_angle) - self.tc2 * np.cos(2 * self.day_angle) - self.ts2 * np.sin(2 * self.day_angle)) * 229.18
            self.tcorr = (self.eqtime + 4 * (longitude - 0)) / 60
            self.horacorr = self.tcorr + self.div   # Local time obtained from utc time
            self.hour_angle = (12.00 - self.horacorr) * 15
            self.e0 = self.e1 + self.e2 * np.cos(self.day_angle) + self.e3 * np.sin(self.day_angle) + self.e4 * np.cos(2 * self.day_angle) + self.e5 * np.sin(2 * self.day_angle)
            self.u0 = np.sin(self.dec) * np.sin(latitude * self.CDR) + np.cos(self.dec) * np.cos(latitude * self.CDR) * np.cos(self.hour_angle * self.CDR)
            self.zenith_angle = np.arccos(self.u0) * 180 / np.pi
            self.sa = 1368 * self.e0

            # Start level 1

            # Routine to check the misalignment of the tracker
            if self.zenith_angle < 87:
                if self.loader.data[i][4] != 3333 and self.loader.data[i][4] != -5555 and self.loader.data[i][4] != -6999:
                    if self.loader.data[i][28] != 3333 and self.loader.data[i][28] != -5555 and self.loader.data[i][28] != -6999:
                        if self.loader.data[i][4] > 50:
                            self.rtoa = self.sa * self.u0
                            self.kt = self.loader.data[i][4] / self.rtoa
                            self.kn = self.loader.data[i][28] / self.loader.data[i][4]
                            if self.kt >= 0.50:
                                if self.kn > 0.30:
                                    self.loader.code[i][8] = 9
                                    self.loader.code[i][28] = 9
                                else:
                                    self.loader.code[i][8] = 552
                                    self.loader.code[i][28] = 552
                            elif self.kt >= 0.40 and self.kt < 0.50:
                                if self.kn > 0.10:
                                    self.loader.code[i][8] = 9
                                    self.loader.code[i][28] = 9
                                else:
                                    self.loader.code[i][8] = 552
                                    self.loader.code[i][28] = 552

            # End of routine to check the misalignment of the tracker

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Global Radiation (W/m²) level 1

            if self.loader.data[i][4] != 3333:
                if self.loader.data[i][4] != -5555:
                    if self.loader.data[i][4] != -6999:
                        if self.loader.data[i][5] != 0:
                            if self.u0 > 0:
                                self.GLOBAL_MX = (self.sa * 1.5 * (self.u0**1.2) + 100)
                            else:
                                self.GLOBAL_MX = 100

                            if self.loader.data[i][4] > self.GLOBAL_MI and self.loader.data[i][4] < self.GLOBAL_MX:
                                self.loader.code[i][4] = 9
                            else:
                                self.loader.code[i][4] = 552
                        else:
                            if self.zenith_angle > 90:
                                if self.u0 > 0:
                                    self.GLOBAL_MX = (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                else:
                                    self.GLOBAL_MX = 100

                                if self.loader.data[i][4] > self.GLOBAL_MI and self.loader.data[i][4] < self.GLOBAL_MX:
                                    self.loader.code[i][4] = 9
                                else:
                                    self.loader.code[i][4] = 552
                            else:
                                self.cont_std += 1
                                if self.loader.data[i][4] != self.loader.data[i-1][4] and self.loader.data[i][4] != self.loader.data[i+1][4]:
                                    if self.u0 > 0:
                                        self.GLOBAL_MX = (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                    else:
                                        self.GLOBAL_MX = 100

                                    if self.loader.data[i][4] > self.GLOBAL_MI and self.loader.data[i][4] < self.GLOBAL_MX:
                                        self.loader.code[i][4] = 9
                                    else:
                                        self.loader.code[i][4] = 552
                                else:
                                    self.loader.code[i][4] = 552
                    else:
                        self.loader.code[i][4] = -6999
                else:
                    self.loader.code[i][4] = -5555
            else:
                self.loader.code[i][4] = 3333

            # End of the routine validation: Global Radiation (W/m²) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Diffuse Radiation (W/m²) level 1

            if self.loader.data[i][8] != 3333:
                if self.loader.data[i][8] != -5555:
                    if self.loader.data[i][8] != -6999:
                        if self.loader.code[i][8] != 552:
                            if self.loader.data[i][9] != 0:
                                if self.u0 > 0:
                                    self.DIFUSE_MX = (self.sa * 0.95 * (self.u0**1.2) + 50)
                                else:
                                    self.DIFUSE_MX = 50

                                if self.loader.data[i][8] > self.DIFUSE_MI and self.loader.data[i][8] < self.DIFUSE_MX:
                                    self.loader.code[i][8] = 9
                                else:
                                    self.loader.code[i][8] = 552
                            else:
                                if self.zenith_angle > 90:
                                    if self.u0 > 0:
                                        self.DIFUSE_MX = (self.sa * 0.95 * (self.u0**1.2) + 50)
                                    else:
                                        self.DIFUSE_MX = 50

                                    if self.loader.data[i][8] > self.DIFUSE_MI and self.loader.data[i][8] < self.DIFUSE_MX:
                                        self.loader.code[i][8] = 9
                                    else:
                                        self.loader.code[i][8] = 552
                                else:
                                    self.cont_std += 1
                                    if self.loader.data[i][8] != self.loader.data[i-1][8] and self.loader.data[i][8] != self.loader.data[i+1][8]:
                                        if self.u0 > 0:
                                            self.DIFUSE_MX = (self.sa * 0.95 * (self.u0 ** 1.2) + 50)
                                        else:
                                            self.DIFUSE_MX = 50

                                        if self.loader.data[i][8] > self.DIFUSE_MI and self.loader.data[i][8] < self.DIFUSE_MX:
                                            self.loader.code[i][8] = 9
                                        else:
                                            self.loader.code[i][8] = 552
                                    else:
                                        self.loader.code[i][8] = 552
                    else:
                        self.loader.code[i][8] = -6999
                else:
                    self.loader.code[i][8] = -5555
            else:
                self.loader.code[i][8] = 3333

            # End of the routine validation: Diffuse Radiation (W/m²) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Par Radiation (�mols s� m�) level 1

            if self.loader.data[i][12] != 3333:
                if self.loader.data[i][12] != -5555:
                    if self.loader.data[i][12] != -6999:
                        if self.loader.data[i][13] != 0:
                            if self.u0 > 0:
                                self.PAR_MX = 2.07 * (self.sa * 1.5 * (self.u0**1.2) + 100)
                            else:
                                self.PAR_MX = 2.07 * 100

                            if self.loader.data[i][12] > self.PAR_MI and self.loader.data[i][12] < self.PAR_MX:
                                self.loader.code[i][12] = 9
                            else:
                                self.loader.code[i][12] = 552
                        else:
                            if self.zenith_angle > 90:
                                if self.u0 > 0:
                                    self.PAR_MX = 2.07 * (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                else:
                                    self.PAR_MX = 2.07 * 100

                                if self.loader.data[i][12] > self.PAR_MI and self.loader.data[i][12] < self.PAR_MX:
                                    self.loader.code[i][12] = 9
                                else:
                                    self.loader.code[i][12] = 552
                            else:
                                self.cont_std += 1
                                if self.loader.data[i][12] != self.loader.data[i-1][12] and self.loader.data[i][12] != self.loader.data[i+1][12]:
                                    if self.u0 > 0:
                                        self.PAR_MX = 2.07 * (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                    else:
                                        self.PAR_MX = 2.07 * 100

                                    if self.loader.data[i][12] > self.PAR_MI and self.loader.data[i][12] < self.PAR_MX:
                                        self.loader.code[i][12] = 9
                                    else:
                                        self.loader.code[i][12] = 552
                                else:
                                    self.loader.code[i][12] = 552
                    else:
                        self.loader.code[i][12] = -6999
                else:
                    self.loader.code[i][12] = -5555
            else:
                self.loader.code[i][12] = 3333


            # End of the routine validation: Par Radiation (�mols s� m�) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Lux Radiation (kLux) level 1

            if self.loader.data[i][16] != 3333:
                if self.loader.data[i][16] != -5555:
                    if self.loader.data[i][16] != -6999:
                        if self.loader.data[i][17] != 0:
                            if self.u0 > 0:
                                self.LUX_MX = 0.115 * (self.sa * 1.5 * (self.u0**1.2) + 100)
                            else:
                                self.LUX_MX = 0.115 * 100

                            if self.loader.data[i][16] > self.LUX_MI and self.loader.data[i][16] < self.LUX_MX:
                                self.loader.code[i][16] = 9
                            else:
                                self.loader.code[i][16] = 552
                        else:
                            if self.zenith_angle > 90:
                                if self.u0 > 0:
                                    self.LUX_MX = 0.115 * (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                else:
                                    self.LUX_MX = 0.115 * 100

                                if self.loader.data[i][16] > self.LUX_MI and self.loader.data[i][16] < self.LUX_MX:
                                    self.loader.code[i][16] = 9
                                else:
                                    self.loader.code[i][16] = 552
                            else:
                                self.cont_std += 1
                                if self.loader.data[i][16] != self.loader.data[i-1][16] and self.loader.data[i][16] != self.loader.data[i+1][16]:
                                    if self.u0 > 0:
                                        self.LUX_MX = 0.115 * (self.sa * 1.5 * (self.u0 ** 1.2) + 100)
                                    else:
                                        self.LUX_MX = 0.115 * 100

                                    if self.loader.data[i][16] > self.LUX_MI and self.loader.data[i][16] < self.LUX_MX:
                                        self.loader.code[i][16] = 9
                                    else:
                                        self.loader.code[i][16] = 552
                                else:
                                    self.loader.code[i][16] = 552
                    else:
                        self.loader.code[i][16] = -6999
                else:
                    self.loader.code[i][16] = -5555
            else:
                self.loader.code[i][16] = 3333

            # End of the routine validation: Lux Radiation (kLux) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Air Temperature (°C) level 1

            if self.loader.data[i][20] != 3333:
                if self.loader.data[i][20] != -5555:
                    self.TEMP_MX = self.loader.getTempMax(os.path.abspath(".")+ os.path.sep + "." + "limits" + os.path.sep + "temp.max", station, month)
                    self.TEMP_MI = self.loader.getTempMin(os.path.abspath(".")+ os.path.sep + "." + "limits" + os.path.sep + "temp.min", station, month)
                    if self.loader.data[i][20] > self.TEMP_MI and self.loader.data[i][20] < self.TEMP_MX:
                        self.loader.code[i][20] = 9
                    else:
                        self.loader.code[i][20] = 552
                else:
                    self.loader.code[i][20] = -5555
            else:
                self.loader.code[i][20] = 3333

            # End of the routine validation: Air Temperature (°C) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Relative Air Humidity (%) level 1

            if self.loader.data[i][21] != 3333:
                if self.loader.data[i][21] != -5555:
                    if self.loader.data[i][21] > self.HUMI_MI and self.loader.data[i][21] <= self.HUMI_MX:
                        self.loader.code[i][21] = 9
                    else:
                        self.loader.code[i][21] = 552
                else:
                    self.loader.code[i][21] = -5555
            else:
                self.loader.code[i][21] = 3333

            # End of the routine validation: Relative Air Humidity (%) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Atmospheric Pressure (mbar) level 1

            if self.loader.data[i][22] != 3333:
                if self.loader.data[i][22] != -5555:
                    self.PRES_MX = self.loader.getPresMax(os.path.abspath(".")+ os.path.sep + "." +"limits" + os.path.sep + "pres.max", station)
                    self.PRES_MI = self.loader.getPresMin(os.path.abspath(".")+ os.path.sep + "." + "limits" + os.path.sep + "pres.min", station)
                    if self.loader.data[i][22] > self.PRES_MI and self.loader.data[i][22] < self.PRES_MX:
                        self.loader.code[i][22] = 9
                    else:
                        self.loader.code[i][22] = 552
                else:
                    self.loader.code[i][22] = -5555
            else:
                self.loader.code[i][22] = 3333

            # End of the routine validation: Atmospheric Pressure (mbar) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Accumulated Precipitation (mm) level 1

            if self.loader.data[i][23] != 3333:
                if self.loader.data[i][23] != -5555:
                    self.PREC_MX = self.loader.getPrecMax(os.path.abspath(".")+ os.path.sep + "." + "limits" + os.path.sep + "prec.max", station, month)
                    if self.loader.data[i][23] >= self.PREC_MI and self.loader.data[i][23] < self.PREC_MX:
                        self.loader.code[i][23] = 9
                    else:
                        self.loader.code[i][23] = 552
                else:
                    self.loader.code[i][23] = -5555
            else:
                self.loader.code[i][23] = 3333

            # End of the routine validation: Accumulated Precipitation (mm) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Wind Speed 10m (m/s) level 1

            if self.loader.data[i][24] != 3333:
                if self.loader.data[i][24] != -5555:
                    if self.loader.data[i][24] > self.WS10_MI and self.loader.data[i][24] < self.WS10_MX:
                        self.loader.code[i][24] = 9
                    else:
                        self.loader.code[i][24] = 552
                else:
                    self.loader.code[i][24] = -5555
            else:
                self.loader.code[i][24] = 3333

            # End of the routine validation: Wind Speed 10m (m/s) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Wind Direction 10m (°) level 1

            if self.loader.data[i][25] != 3333:
                if self.loader.data[i][25] != -5555:
                    if self.loader.data[i][26] != 0:
                        if self.loader.data[i][25] > self.WD10_MI and self.loader.data[i][25] < self.WD10_MX:
                            self.loader.code[i][25] = 9
                        else:
                            self.loader.code[i][25] = 552
                    else:
                        self.loader.code[i][25] = 552
                else:
                    self.loader.code[i][25] = -5555
            else:
                self.loader.code[i][25] = 3333

            # End of the routine validation: Wind Direction 10m (°) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Direct Radiation (W/m²) level 1

            if self.loader.data[i][28] != 3333:
                if self.loader.data[i][28] != -5555:
                    if self.loader.data[i][28] != -6999:
                        if self.loader.code[i][28] != 552:
                            if self.loader.data[i][29] != 0:
                                if self.u0 > 0:
                                    self.DIRECT_MX = self.sa
                                else:
                                    self.DIRECT_MX = 50

                                if self.loader.data[i][28] > self.DIRECT_MI and self.loader.data[i][28] < self.DIRECT_MX:
                                    self.loader.code[i][28] = 9
                                else:
                                    self.loader.code[i][28] = 552
                            else:
                                if self.zenith_angle > 90:
                                    if self.u0 > 0:
                                        self.DIRECT_MX = self.sa
                                    else:
                                        self.DIRECT_MX = 50

                                    if self.loader.data[i][28] > self.DIRECT_MI and self.loader.data[i][28] < self.DIRECT_MX:
                                        self.loader.code[i][28] = 9
                                    else:
                                        self.loader.code[i][28] = 552
                                else:
                                    self.cont_std+=1

                                    if self.loader.data[i][28] != self.loader.data[i-1][28] and self.loader.data[i][28] != self.loader.data[i+1][28]:
                                        if self.u0 > 0:
                                            self.DIRECT_MX = self.sa
                                        else:
                                            self.DIRECT_MX = 50

                                        if self.loader.data[i][28] > self.DIRECT_MI and self.loader.data[i][28] < self.DIRECT_MX:
                                            self.loader.code[i][28] = 9
                                        else:
                                            self.loader.code[i][28] = 552
                                    else:
                                        self.loader.code[i][28] = 552
                    else:
                        self.loader.code[i][28] = -6999
                else:
                    self.loader.code[i][28] = -5555
            else:
                self.loader.code[i][28] = 3333

            # End of the routine validation: Direct Radiation (W/m²) level 1

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Long Wave Radiation (W/m²) level 1

            if self.loader.data[i][32] != 3333:
                if self.loader.data[i][32] != -5555:
                    if self.loader.data[i][32] != -6999:
                        if self.loader.data[i][33] != 0:
                            if self.loader.data[i][32] > self.LWDN_MI and self.loader.data[i][32] < self.LWDN_MX:
                                self.loader.code[i][32] = 9
                            else:
                                self.loader.code[i][32] = 552
                        else:
                            if self.zenith_angle > 90:
                                if self.loader.data[i][32] > self.LWDN_MI and self.loader.data[i][32] < self.LWDN_MX:
                                    self.loader.code[i][32] = 9
                                else:
                                    self.loader.code[i][32] = 552
                            else:
                                self.cont_std+=1

                                if self.loader.data[i][32] != self.loader.data[i-1][32] and self.loader.data[i][32] != self.loader.data[i+1][32]:
                                    if self.loader.data[i][32] > self.LWDN_MI and self.loader.data[i][32] < self.LWDN_MX:
                                        self.loader.code[i][32] = 9
                                    else:
                                        self.loader.code[i][32] = 552
                                else:
                                    self.loader.code[i][32] = 552
                    else:
                        self.loader.code[i][32] = -6999
                else:
                    self.loader.code[i][32] = -5555
            else:
                self.loader.code[i][32] = 3333

            self.pb.update(1)

            # End of the routine validation: Long Wave Radiation (W/m²) level 1

            # ----------------------------------------------------------------------------------------------------------------------

    	    # End of loop level 1

        # Start level 2

        for i in range(self.rows + 1):
            self.num = self.loader.data[i][3]
            self.div = self.num / 60
            self.dia_jul = int(self.loader.data[i][2])

            # Calculating astronomical data
            self.day_angle = (2 * np.pi / 365.25 * self.dia_jul)
            self.dec = (self.d0 - self.dc1 * np.cos(self.day_angle) + self.ds1 * np.sin(self.day_angle) - self.dc2 * np.cos(2*self.day_angle) + self.ds2 * np.sin(2*self.day_angle) - self.dc3 * np.cos(3*self.day_angle) + self.ds3 * np.sin(3*self.day_angle))
            self.eqtime = (self.et0 + self.tc1 * np.cos(self.day_angle) - self.ts1 *np.sin(self.day_angle) - self.tc2 * np.cos(2*self.day_angle) - self.ts2 * np.sin(2*self.day_angle)) * 229.18
            self.tcorr = (self.eqtime + 4 * (longitude - 0)) / 60
            self.horacorr = self.tcorr + self.div
            self.hour_angle = (12.00 - self.horacorr) * 15
            self.e0 = self.e1 + self.e2 * np.cos(self.day_angle) + self.e3 * np.sin(self.day_angle) + self.e4 * np.cos(2*self.day_angle) + self.e5 * np.sin(2*self.day_angle)
            self.u0 = np.sin(self.dec) * np.sin(latitude * self.CDR) + np.cos(self.dec) * np.cos(latitude * self.CDR) * np.cos(self.hour_angle * self.CDR)
            self.zenith_angle = (np.arccos(self.u0)) * 180 / np.pi
            self.sa = 1368 * self.e0

            # BSRN criteria used to qualify solar data as RARE events
            self.GLOBAL_MI = -2
            self.DIFUSE_MI = -2
            self.DIRECT_MI = -2
            self.PAR_MI = -2
            self.LUX_MI = -2
            self.LWDN_MX = 500
            self.LWDN_MI = 60

            # Variables used to validate meteorological data - level 2
            totalTemp1h_1 = self.rows - self.temp1h
            totalTemp1h_2 = self.rows - self.temp1h + 1

            totalPres3h_1 = self.rows - self.pres3h
            totalPres3h_2 = self.rows - self.pres3h + 1

            totalPrec1h_1 = self.rows - self.prec1h
            totalPrec1h_2 = self.rows - self.prec1h + 1

            totalWs103h_1 = self.rows - self.ws103h
            totalWs103h_2 = self.rows - self.ws103h

            totalWd103h_1 = self.rows - self.wd103h
            totalWd103h_2 = self.rows - self.wd103h + 1

            # Start of the routine validation: Global Radiation (W/m²) level 2

            if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552:
                if self.u0 > 0:
                    self.GLOBAL_MX = (self.sa * 1.2 * (self.u0**1.2) + 50)
                else:
                    self.GLOBAL_MX = 50

                if self.loader.data[i][4] > self.GLOBAL_MI and self.loader.data[i][4] < self.GLOBAL_MX:
                    self.loader.code[i][4] = 99
                else:
                    self.loader.code[i][4] = 29

            # End of the routine validation: Global Radiation (W/m²) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Diffuse Radiation (W/m²) level 2

            if self.loader.code[i][8] != 3333 and self.loader.code[i][8] != -5555 and self.loader.code[i][8] != -6999 and self.loader.code[i][8] != 552:
                if self.u0 > 0:
                    self.DIFUSE_MX = (self.sa * 0.75 * (self.u0**1.2) + 30)
                else:
                    self.DIFUSE_MX = 30

                if self.loader.data[i][8] > self.DIFUSE_MI and self.loader.data[i][8] < self.DIFUSE_MX:
                    self.loader.code[i][8] = 99
                else:
                    self.loader.code[i][8] = 29

            # End of the routine validation: Diffuse Radiation (W/m²) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Par Radiation (�mols s� m�) level 2

            if self.loader.code[i][12] != 3333 and self.loader.code[i][12] != -5555 and self.loader.code[i][12] != -6999 and self.loader.code[i][12] != 552:
                if self.u0 > 0:
                    self.PAR_MX = 2.07 * (self.sa * 1.2 * (self.u0**1.2) + 50)
                else:
                    self.PAR_MX = 2.07 * 50

                if self.loader.data[i][12] > self.PAR_MI and self.loader.data[i][12] < self.PAR_MX:
                    self.loader.code[i][12] = 99
                else:
                    self.loader.code[i][12] = 29

            # End of the routine validation: Par Radiation (�mols s� m�) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Lux Radiation (kLux) level 2

            if self.loader.code[i][16] != 3333 and self.loader.code[i][16] != -5555 and self.loader.code[i][16] != -6999 and self.loader.code[i][16] != 552:
                if self.u0 > 0:
                    self.LUX_MX = 0.115 * (self.sa * 1.2 * (self.u0**1.2) + 50)
                else:
                    self.LUX_MX = 0.115 * 50

                if self.loader.data[i][16] > self.LUX_MI and self.loader.data[i][16] < self.LUX_MX:
                    self.loader.code[i][16] = 99
                else:
                    self.loader.code[i][16] = 29

            # End of the routine validation: Lux Radiation (kLux) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Air Temperature (°C) level 2
            if self.loader.code[i][20] != 3333 and self.loader.code[i][20] != -5555 and self.loader.code[i][20] != 552:
                if i <= totalTemp1h_1:
                    j = 0
                    while j <= self.temp1h:
                        if self.loader.code[i+j][20] != 3333 and self.loader.code[i+j][20] != 552:
                            self.contTempValid += 1

                            if self.loader.data[i+j][20] > self.temp_max:
                                self.temp_max = self.loader.data[i+j][20]

                            if self.loader.data[i+j][20] < self.temp_min:
                                self.temp_min = self.loader.data[i+j][20]

                            self.variation_temp1h = self.temp_max - self.temp_min
                        j += 1

                    if self.contTempValid >= 40:
                        if self.variation_temp1h < 5:
                            self.loader.code[i][20] = 99
                            self.lastTempValid = self.loader.code[i][20]
                        else:
                            self.loader.code[i][20] = 529
                    else:
                        l = 0
                        while l <= self.temp1h:
                            if self.loader.code[i+l][20] != 3333 and self.loader.code[i+l][20] != 552:
                                if i == 0:
                                    self.loader.code[i][20] = 559
                                else:
                                    self.loader.code[i][20] = self.lastTempValid
                            l += 1

                    self.contTempValid = 0
                    self.temp_max = 0
                    self.temp_min = 999

                if i >= totalTemp1h_2:
                    self.loader.code[i][20] = self.loader.code[totalTemp1h_1][20]

            # End of the routine validation: Air Temperature (°C) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Atmospheric Pressure (mbar) level 2

            if self.loader.code[i][22] != 3333 and self.loader.code[i][22] != -5555 and self.loader.code[i][22] != 552:
                if i <= totalPres3h_1:
                    j = 0
                    while j <= self.pres3h:
                        if self.loader.code[i+j][22] != 3333 and self.loader.code[i+j][22] != 552:
                            self.contPresValid += 1

                            if self.loader.data[i+j][22] > self.pres_max:
                                self.pres_max = self.loader.data[i+j][22]

                            if self.loader.data[i+j][22] < self.pres_min:
                                self.pres_min = self.loader.data[i+j][22]

                            self.variation_pres3h = self.pres_max - self.pres_min
                        j += 1

                    if self.contPresValid >= 40:
                        if self.variation_pres3h < 6:
                            self.loader.code[i][22] = 99
                            self.lastPresValid = self.loader.code[i][22]
                        else:
                            self.loader.code[i][22] = 529
                    else:
                        l = 0
                        while l <= self.pres3h:
                            if self.loader.code[i+l][22] != 3333 and self.loader.code[i+l][22] != 552:
                                if i == 0:
                                    self.loader.code[i][22] = 59
                                else:
                                    self.loader.code[i][22] = self.lastPresValid
                            l += 1

                    self.contPresValid = 0
                    self.pres_max = 0
                    self.pres_min = 999

                if i >= totalPres3h_2:
                    self.loader.code[i][22] = self.loader.code[totalPres3h_1][22]

            # End of the routine validation: Atmospheric Pressure (mbar) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Accumulated Precipitation (mm) level 2

            if self.loader.code[i][23] != 3333 and self.loader.code[i][23] != -5555 and self.loader.code[i][23] != 552:
                if i <= totalPrec1h_1:
                    j = 0
                    while j <= self.prec1h:
                        if self.loader.code[i+j][23] != 3333 and self.loader.code[i+j][23] != 552:
                            self.contPrecValid += 1

                            if self.loader.data[i+j][23] > self.prec_max:
                                self.prec_max = self.loader.data[i+j][23]

                            if self.loader.data[i+j][23] < self.prec_min:
                                self.prec_min = self.loader.data[i+j][23]

                            self.variation_prec1h = self.prec_max - self.prec_min
                        j += 1

                    if self.contPrecValid >= 40:
                        if self.variation_prec1h < 25:
                            self.loader.code[i][23] = 99
                            self.lastPrecValid = self.loader.code[i][23]
                        else:
                            self.loader.code[i][23] = 529
                    else:
                        l = 0
                        while l <= self.prec1h:
                            if self.loader.code[i+l][23] != 3333 and self.loader.code[i+l][23] != 552:
                                if i == 0:
                                    self.loader.code[i][23] = 559
                                else:
                                    self.loader.code[i][23] = self.lastPrecValid
                            l += 1

                    self.contPrecValid = 0
                    self.prec_max = 0
                    self.prec_min = 999

                if i >= totalPrec1h_2:
                    self.loader.code[i][23] = self.loader.code[totalPrec1h_1][23]

            # End of the routine validation: Accumulated Precipitation (mm) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Wind Speed 10m (m/s) level 2

            if self.loader.code[i][24] != 3333 and self.loader.code[i][24] != -5555 and self.loader.code[i][24] != 552:
                if i <= totalWs103h_1:
                    j = 0
                    while j <= self.ws103h:
                        if self.loader.code[i+j][24] != 3333 and self.loader.code[i+j][24] != 552:
                            self.contWspdValid += 1
                            if self.loader.data[i+j][24] > self.ws10_max:
                                self.ws10_max = self.loader.data[i+j][24]

                            if self.loader.data[i+j][24] < self.ws10_min:
                                self.ws10_min = self.loader.data[i+j][24]

                            self.variation_ws103h = self.ws10_max - self.ws10_min
                        j += 1

                    if self.contWspdValid >= 40:
                        if self.variation_ws103h > 0.1:
                            self.loader.code[i][24] = 99
                            self.lastWs10Valid = self.loader.code[i][24]
                        else:
                            self.loader.code[i][24] = 529
                    else:
                        l = 0
                        while l <= self.ws103h:
                            if self.loader.code[i+l][24] != 3333 and self.loader.code[i+l][24] != 552:
                                if i == 0:
                                    self.loader.code[i][24] = 559
                                else:
                                    self.loader.code[i][24] = self.lastWs10Valid
                            l += 1

                    self.contWspdValid = 0
                    self.ws10_max = 0
                    self.ws10_min = 999

                if i >= totalWs103h_2:
                    self.loader.code[i][24] = self.loader.code[totalWs103h_1][24]

            # End of the routine validation: Wind Speed 10m (m/s) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Wind Direction 10m (°) level 2

            if self.loader.code[i][25] != 3333 and self.loader.code[i][25] != -5555 and self.loader.code[i][25] != 552:
                if i <= totalWd103h_1:
                    j = 0
                    while j <= self.wd103h:
                        if self.loader.code[i+j][25] != 3333 and self.loader.code[i+j][25] != 552:
                            self.contWdirValid += 1
                            if self.loader.data[i+j][25] > self.wd10_max:
                                self.wd10_max = self.loader.data[i+j][25]

                            if self.loader.data[i+j][25] < self.wd10_min:
                                self.wd10_min = self.loader.data[i+j][25]

                            self.variation_wd103h = self.wd10_max - self.wd10_min
                        j += 1

                    if self.contWdirValid >= 40:
                        if self.variation_wd103h > 1:
                            self.loader.code[i][25] = 99
                            self.lastWd10Valid = self.loader.code[i][25]
                        else:
                            self.loader.code[i][25] = 529
                    else:
                        l = 0
                        while l <= self.wd103h:
                            if self.loader.code[i+l][25] != 3333 and self.loader.code[i+l][25] != 552:
                                if i == 0:
                                    self.loader.code[i][25] = 559
                                else:
                                    self.loader.code[i][25] = self.lastWd10Valid
                            l += 1

                    self.contWdirValid = 0
                    self.wd10_max = 0
                    self.wd10_min = 999

                if i >= totalWd103h_2:
                    self.loader.code[i][25] = self.loader.code[totalWd103h_1][25]

            # End of the routine validation: Wind Direction 10m (°) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Direct Radiation (W/m²) level 2

            if self.loader.code[i][28] != 3333 and self.loader.code[i][28] != -5555 and self.loader.code[i][28] != -6999 and self.loader.code[i][28] != 552:
                if self.u0 > 0:
                    self.DIRECT_MX = (self.sa * 0.95 * (self.u0 ** 0.2) + 10)
                else:
                    self.DIRECT_MX = 10

                if self.loader.data[i][28] > self.DIRECT_MI and self.loader.data[i][28] < self.DIRECT_MX:
                    self.loader.code[i][28] = 99
                else:
                    self.loader.code[i][28] = 29

            # End of the routine validation: Direct Radiation (W/m²) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # Start of the routine validation: Long Wave Radiation (W/m²) level 2

            if self.loader.code[i][32] != 3333 and self.loader.code[i][32] != -5555 and self.loader.code[i][32] != -6999 and self.loader.code[i][32] != 552:
                if self.loader.data[i][32] > self.LWDN_MI and self.loader.data[i][32] < self.LWDN_MX:
                    self.loader.code[i][32] = 99
                else:
                    self.loader.code[i][32] = 29

            self.pb.update(1)

            # End of the routine validation: Long Wave Radiation (W/m²) level 2

            # ----------------------------------------------------------------------------------------------------------------------

            # End of loop level 2

    	# Start level 3

        for i in range(self.rows + 1):
            self.num = self.loader.data[i][3]
            self.div = self.num / 60
            self.dia_jul = int(self.loader.data[i][2])

            # Calculating astronomical geometry data
            self.day_angle = (2 * np.pi / 365.25 * self.dia_jul)
            self.dec = (self.d0 - self.dc1 * np.cos(self.day_angle) + self.ds1 * np.sin(self.day_angle) - self.dc2 * np.cos(2*self.day_angle) + self.ds2 * np.sin(2*self.day_angle) - self.dc3 * np.cos(3*self.day_angle) + self.ds3 * np.sin(3*self.day_angle))
            self.eqtime = (self.et0 + self.tc1 * np.cos(self.day_angle) - self.ts1 * np.sin(self.day_angle) - self.tc2 * np.cos(2*self.day_angle) - self.ts2 * np.sin(2*self.day_angle)) * 229.18
            self.tcorr = (self.eqtime + 4*(longitude-0)) / 60
            self.horacorr = self.tcorr + self.div
            self.hour_angle = (12.00 - self.horacorr) * 15
            self.e0 = self.e1 + self.e2 * np.cos(self.day_angle) + self.e3 * np.sin(self.day_angle) + self.e4 * np.cos(2*self.day_angle) + self.e5 * np.sin(2*self.day_angle)
            self.u0 = np.sin(self.dec) * np.sin(latitude * self.CDR) + np.cos(self.dec) * np.cos(latitude*self.CDR) * np.cos(self.hour_angle * self.CDR)
            self.zenith_angle = (np.arccos(self.u0)) * 180 / np.pi
            self.sa = 1368 * self.e0

            # Variables used to validate radiation Global and Diffuse - level 3
            difSw = 0
            sumSw = 0
            divSw = 0

            # Variables used to validate radiation Direct - level 3
            direct_h = None
            direct_n = None
            direct_p = None

            # Variables used to validate radiation long wave - level 3
            sigma = 5.76E-8
            temp = None
            temp_a = None
            temp_b = None

            # Variables used in the comparison of global radiation with par and lux - level 3
            lux_global = None
            par_global = None
            lux_par = None
            par_lux = None

            mat_desvio = np.zeros(4)
            mat_limite = np.zeros(4)
            mat_lppl = None

            # Variables used to validate meteorological data - level 3
            totalTemp12h_1 = self.rows - self.temp12h
            totalTemp12h_2 = self.rows - self.temp12h + 1

            totalPrec24h_1 = self.rows - self.prec24h
            totalPrec24h_2 = self.rows - self.prec24h + 1

            totalWs1012h_1 = self.rows - self.ws1012h
            totalWs1012h_2 = self.rows - self.ws1012h + 1

            totalWd1018h_1 = self.rows - self.wd1018h
            totalWd1018h_2 = self.rows - self.wd1018h + 1

            # Start of the routine validation: Comparison of global radiation with par and lux level 3
            if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552 and self.loader.code[i][4] != 29:
                if self.loader.code[i][12] != 3333 and self.loader.code[i][12] != -5555 and self.loader.code[i][12] != -6999 and self.loader.code[i][12] != 552 and self.loader.code[i][12] != 29:
                    if self.loader.code[i][16] != 3333 and self.loader.code[i][16] != -5555 and self.loader.code[i][16] != -6999 and self.loader.code[i][16] != 552 and self.loader.code[i][16] != 29:
                        if self.zenith_angle < 90:
                            lux_global = 0.115 * self.loader.data[i][4]
                            par_global = 2.07 * self.loader.data[i][4]

                            # There are some dependency with photosynthetic photon flux and sometimes 18 is not a better number.
                         	# This version (3.5) these terms were recalculated by Prof. Enio.
                            lux_par = self.loader.data[i][12] / 20.83
                            par_lux = 20.83 * self.loader.data[i][16]

                            if self.loader.data[i][12] == 0:
                                self.loader.data[i][12] = 0.001

                            if self.loader.data[i][16] == 0:
                                self.loader.data[i][16] = 0.001


                            # LUX - LUX < -GLO
                            mat_desvio[0] = (np.abs(self.loader.data[i][16] - lux_global) / self.loader.data[i][16]) * 100
                            # LUX - LUX<-PAR
                            mat_desvio[2] = (np.abs(self.loader.data[i][16] - lux_par) / self.loader.data[i][16]) * 100
                            # PAR - PAR < -GLO
                            mat_desvio[1] = (np.abs(self.loader.data[i][12] - par_global) / self.loader.data[i][12]) * 100
                            # PAR - PAR < -LUX
                            mat_desvio[3] = (np.abs(self.loader.data[i][12] - par_lux) / self.loader.data[i][12]) * 100

                            if self.zenith_angle < 80:
                                # LUX<-GLO
                                if mat_desvio[0] < 9.5:         # Padrao 0
                                    mat_limite[0] = 0
                                elif mat_desvio[0] < 33.5:      # Padrao 1
                                    mat_limite[0] = 1
                                else:                           # Padrao 2
                                    mat_limite[0] = 2

                                # PAR<-GLO
                                if mat_desvio[1] < 12:          # Padrao 0
                                    mat_limite[1] = 0
                                elif mat_desvio[1] < 34:        # Padrao 1
                                    mat_limite[1] = 1
                                else:                           # Padrao 2
                                    mat_limite[1] = 2

                                # LUX<-PAR
                                if mat_desvio[2] < 7.25:        # Padrao 0
                                    mat_limite[2] = 0
                                elif mat_desvio[2] < 15.5:      # Padrao 1
                                    mat_limite[2] = 1
                                else:                           # Padrao 2
                                    mat_limite[2] = 2

                                # PAR<-LUX
                                if mat_desvio[3] < 6.75:        # Padrao 0
                                    mat_limite[3] = 0
                                elif mat_desvio[3] < 13.5:      # Padrao 1
                                    mat_limite[3] = 1
                                else:                           # Padrao 2
                                    mat_limite[3] = 2

                            elif self.zenith_angle <= 88:
                                # LUX<-GLO
                                if mat_desvio[0] < 16.5:        # Padrao 0
                                    mat_limite[0] = 0
                                elif mat_desvio[1] < 65:        # Padrao 1 # Deveria ser 0?
                                    mat_limite[0] = 1
                                else:                           # Padrao 2
                                    mat_limite[0] = 2

                                # PAR<-GLO
                                if mat_desvio[1] < 17:          # Padrao 0
                                    mat_limite[1] = 0
                                elif mat_desvio[1] < 66.5:      # Padrao 1
                                    mat_limite[1] = 1
                                else:                           # Padrao 2
                                    mat_limite[1] = 2

                                # LUX<-PAR
                                if mat_desvio[2] < 11.75:       # Padrao 0
                                    mat_limite[2] = 0
                                elif mat_desvio[2] < 23.5:      # Padrao 1
                                    mat_limite[2] = 1
                                else:                           # Padrao 2
                                    mat_limite[2] = 2

                                # PAR<-LUX
                                if mat_desvio[3] < 10.5:        # Padrao 0
                                    mat_limite[3] = 0
                                elif mat_desvio[3] < 19:        # Padrao 1
                                    mat_limite[3] = 1
                                else: 						    # Padrao 2
                                    mat_limite[3] = 2

                            elif self.zenith_angle > 80 and self.zenith_angle <= 90:
                                # LUX<-GLO
                                if mat_desvio[0] < 45.5:        # Padrao 0
                                    mat_limite[0] = 0
                                elif mat_desvio[0] < 100:       # Padrao 1
                                    mat_limite[0] = 1
                                else:                           # Padrao 2
                                    mat_limite[0] = 2

                                # PAR<-GLO
                                if mat_desvio[1] < 51.25:       # Padrao 0
                                    mat_limite[1] = 0
                                elif mat_desvio[1] < 99.25:     # Padrao 1
                                    mat_limite[1] = 1
                                else:                           # Padrao 2
                                    mat_limite[1] = 2

                                # LUX<-PAR
                                if mat_desvio[2] < 17.75:       # Padrao 0
                                    mat_limite[2] = 0
                                elif mat_desvio[2] < 43.5:      # Padrao 1
                                    mat_limite[2] = 1
                                else:                           # Padrao 2
                                    mat_limite[2] = 2

                                # PAR<-LUX
                                if mat_desvio[3] < 15.5:        # Padrao 0
                                    mat_limite[3] = 0
                                elif mat_desvio[3] < 30.5:      # Padrao 1
                                    mat_limite[3] = 1
                                else:                           # Padrao 2
                                    mat_limite[3] = 2

                            if mat_limite[2] >= mat_limite[3]:
                                mat_lppl = mat_limite[2]
                            else:
                                mat_lppl = mat_limite[3]

                            # Diminuir comparações a seguir

                            if ((mat_limite[1] == 0) and (mat_lppl == 0) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 0) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 0) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 0) and (mat_lppl == 1) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 1) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 1) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 2) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 0) and (mat_lppl == 2) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 0) and (mat_lppl == 2) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 1) and (mat_lppl == 0) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 1) and (mat_lppl == 0) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 1) and (mat_lppl == 0) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 1) and (mat_lppl == 1) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 1) and (mat_lppl == 1) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 1) and (mat_lppl == 1) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 1) and (mat_lppl == 2) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 1) and (mat_lppl == 2) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 1) and (mat_lppl == 2) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 0) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 0) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 2) and (mat_lppl == 0) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 999


                            if ((mat_limite[1] == 2) and (mat_lppl == 1) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 1) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 1) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 2) and (mat_limite[0] == 0)):
                                self.loader.code[i][16] = 999
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 2) and (mat_limite[0] == 1)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299


                            if ((mat_limite[1] == 2) and (mat_lppl == 2) and (mat_limite[0] == 2)):
                                self.loader.code[i][16] = 299
                                self.loader.code[i][12] = 299

                        else:
                            if self.loader.code[i][16] == 99:
                                self.loader.code[i][16] = 599

                            if self.loader.code[i][12] == 99:
                                self.loader.code[i][12] = 599

                    else:
                        if self.loader.code[i][16] == 99:
                            self.loader.code[i][16] = 599

                        if self.loader.code[i][16] == 29:
                            self.loader.code[i][16] = 529

                        if self.loader.code[i][12] == 99:
                            self.loader.code[i][12] = 599

                else:
                    if self.loader.code[i][12] == 99:
                        self.loader.code[i][12] = 599

                    if self.loader.code[i][12] == 29:
                        self.loader.code[i][12] = 529

                    if self.loader.code[i][16] == 99:
                        self.loader.code[i][16] = 599

            else:
                if self.loader.code[i][16] == 99:
                    self.loader.code[i][16] = 599

                if self.loader.code[i][16] == 29:
                    self.loader.code[i][16] = 529

                if self.loader.code[i][12] == 99:
                    self.loader.code[i][12] = 599

                if self.loader.code[i][12] == 29:
                    self.loader.code[i][12] = 529

            # End of the routine validation: Comparison of global radiation with par and lux level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Global Radiation (W/m²) level 3

            if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552 and self.loader.code[i][4] != 29:
                if self.loader.code[i][8] != 3333 and self.loader.code[i][8] != -5555 and self.loader.code[i][8] != -6999 and self.loader.code[i][8] != 552 and self.loader.code[i][8] != 29 and self.loader.code[i][28] != 3333 and self.loader.code[i][28] != -5555 and self.loader.code[i][28] != -6999 and self.loader.code[i][28] != 552 and self.loader.code[i][28] != 29:
                    if self.loader.data[i][4] >= 50:
                        if self.zenith_angle >= 75:
                            if self.loader.data[i][8] / self.loader.data[i][4] < 1.10:
                                self.loader.code[i][4] = 999
                            else:
                                self.loader.code[i][4] = 299
                        else:
                            if self.loader.data[i][8] / self.loader.data[i][4] < 1.05:
                                self.loader.code[i][4] = 999
                            else:
                                self.loader.code[i][4] = 299
                    else:
                        if self.loader.data[i][4] < 50:
                            if self.loader.data[i][8] - self.loader.data[i][4] < 15:
                                self.loader.code[i][4] = 999
                            else:
                                self.loader.code[i][4] = 299
                        else:
                            self.loader.code[i][4] = 599

                    # sumSw = self.loader.data[i][8] + (self.loader.data[i][28] * self.u0)
                    #
                    # # ////////////////////// TEST BSRN LEVEL 3 ////////////////////////
                    # if sumSw > 50:
                    #     if self.zenith_angle < 75:
                    #         if divSw > 0.90 and divSw < 1.10:
                    #             self.loader.code[i][4] = 999
                    #         else:
                    #             self.loader.code[i][4] = 299
                    #
                    #     if self.zenith_angle > 75 and self.zenith_angle < 93:
                    #         if divSw > 0.85 and divSw < 1.15:
                    #             self.loader.code[i][4] = 999
                    #         else:
                    #             self.loader.code[i][4] = 299
                    # else:
                    #     self.loader.code[i][4] = 599

                    # ////////////////////// TEST BSRN LEVEL 3 ////////////////////////

                # ////////////////////// Se a DIFUSA e DIRETA for RUIM - VERIFICA PAR E LUX
                else:
                    if self.loader.code[i][12] != 529 and self.loader.code[i][12] != 299 and self.loader.code[i][12] != 552 and self.loader.code[i][12] != 29 and self.loader.code[i][16] != 529 and self.loader.code[i][16] != 299 and self.loader.code[i][16] != 552 and self.loader.code[i][16] != 29:
                        self.loader.code[i][4] = 999
                    else:
                        self.loader.code[i][4] = 599
            else:
                if self.loader.code[i][4] == 29:
                    self.loader.code[i][4] = 529

            # End of the routine validation: Global Radiation (W/m²) level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Diffuse Radiation (W/m²) level 3

            if self.loader.code[i][8] != 3333 and self.loader.code[i][8] != -5555 and self.loader.code[i][8] != -6999 and self.loader.code[i][8] != 552 and self.loader.code[i][8] != 29:
                if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552 and self.loader.code[i][4] != 529:
                    if self.loader.data[i][4] > 50:
                        difSw = self.loader.data[i][8] / self.loader.data[i][4]
                        if self.zenith_angle < 75:
                            if difSw < 1.05:
                                self.loader.code[i][8] = 999
                            else:
                                self.loader.code[i][8] = 299

                        if self.zenith_angle > 75 and self.zenith_angle < 93:
                            if difSw < 1.10:
                                self.loader.code[i][8] = 999
                            else:
                                self.loader.code[i][8] = 299

                    else:
                        self.loader.code[i][8] = 599
                else:
                    if self.loader.code[i][8] == 99:
                        self.loader.code[i][8] = 599
            else:
                if self.loader.code[i][8] == 29:
                    self.loader.code[i][8] = 529

            # End of the routine validation: Diffuse Radiation (W/m²) level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Air Temperature (°C) level 3

            if self.loader.code[i][20] != 3333 and self.loader.code[i][20] != -5555 and self.loader.code[i][20] != 552 and self.loader.code[i][20] != 529:
                if i <= totalTemp12h_1:
                    j = 0
                    while j <= self.temp12h:
                        if self.loader.code[i+j][20] != 3333 and self.loader.code[i+j][20] != 552 and self.loader.code[i+j][20] != 529:
                            self.contTempValid += 1
                            if self.loader.data[i+j][20] > self.temp_max:
                                self.temp_max = self.loader.data[i+j][20]
                            if self.loader.data[i+j][20] < self.temp_min:
                                self.temp_min = self.loader.data[i+j][20]
                            self.variation_temp12h = self.temp_max - self.temp_min
                        j += 1

                    if self.contTempValid >= 40:
                        if self.variation_temp12h > 0.5:
                            self.loader.code[i][20] = 999
                            self.lastTempValid = self.loader.code[i][20]
                        else:
                            self.loader.code[i][20] = 299
                    else:
                        l = 0
                        while l <= self.temp12h:
                            if self.loader.code[i+l][20] != 3333 and self.loader.code[i+l][20] != 552 and self.loader.code[i+l][20] != 529:
                                if i == 0:
                                    self.loader.code[i][20] = 559
                                else:
                                    self.loader.code[i][20] = self.lastTempValid
                            l += 1

                        self.contTempValid = 0
                        self.temp_max = 0
                        self.temp_min = 999
                if i >= totalTemp12h_2:
                    self.loader.code[i][20] = self.loader.code[totalTemp12h_1][20]

            # End of the routine validation: Air Temperature (°C) level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Accumulated Precipitation (mm) level 3

            if self.loader.code[i][23] != 3333 and self.loader.code[i][23] != -5555 and self.loader.code[i][23] != 552 and self.loader.code[i][23] != 529:
                if i <= totalPrec24h_1:
                    j = 0
                    while j <= self.prec24h:
                        if self.loader.code[i+j][23] != 3333 and self.loader.code[i+j][23] != 552 and self.loader.code[i+j][23] != 529:
                            self.contPrecValid += 1
                            if self.loader.data[i+j][23] > self.prec_max:
                                self.prec_max = self.loader.data[i+j][23]
                            if self.loader.data[i+j][23] < self.prec_min:
                                self.prec_min = self.loader.data[i+j][23]
                            self.variation_prec24h = self.temp_max - self.prec_min #prec_max
                        j += 1

                    if self.contPrecValid >= 40:
                        if self.variation_prec24h < 100:
                            self.loader.code[i][23] = 999
                            self.lastPrecValid = self.loader.code[i][23]
                        else:
                            self.loader.code[i][23] = 299
                    else:
                        l = 0
                        while l <= self.prec24h:
                            if self.loader.code[i+l][23] != 3333 and self.loader.code[i+l][23] != 552 and self.loader.code[i+l][23] != 529:
                                if i == 0:
                                    self.loader.code[i][23] = 559
                                else:
                                    self.loader.code[i][23] = self.lastPrecValid
                            l += 1

                        self.contPrecValid = 0
                        self.prec_max = 0
                        self.prec_min = 999

                if i >= totalPrec24h_2:
                    self.loader.code[i][23] = self.loader.code[totalPrec24h_1][23]

            # End of the routine validation: Accumulated Precipitation (mm) level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Wind Speed 10m (m/s) level 3

            if self.loader.code[i][24] != 3333 and self.loader.code[i][24] != -5555 and self.loader.code[i][24] != 552 and self.loader.code[i][24] != 529:
                if i <= totalWs1012h_1:
                    j = 0
                    while j <= self.ws1012h:
                        if self.loader.code[i+j][24] != 3333 and self.loader.code[i+j][24] != 552 and self.loader.code[i+j][24] != 529:
                            self.contWspdValid += 1
                            if self.loader.data[i+j][24] > self.ws10_max:
                                self.ws10_max = self.loader.data[i+j][24]
                            if self.loader.data[i+j][24] < self.ws10_min:
                                self.ws10_min = self.loader.data[i+j][24]
                            self.variation_ws1012h = self.ws10_max - self.ws10_min
                        j += 1

                    if self.contWspdValid >= 40:
                        if self.variation_ws1012h > 0.5:
                            self.loader.code[i][24] = 999
                            self.lastWs10Valid = self.loader.code[i][24]
                        else:
                            self.loader.code[i][24] = 299
                    else:
                        l = 0
                        while l <= self.ws1012h:
                            if self.loader.code[i+l][24] != 3333 and self.loader.code[i+l][24] != 552 and self.loader.code[i+l][24] != 529:
                                if i == 0:
                                    self.loader.code[i][24] = 559
                                else:
                                    self.loader.code[i][24] = self.lastWs10Valid
                            l += 1
                        self.contWspdValid = 0
                        self.ws10_max = 0
                        self.ws10_min = 999

                if i >= totalWs1012h_2:
                    self.loader.code[i][24] = self.loader.code[totalWs1012h_1][24]

            # End of the routine validation: Wind Speed 10m (m/s) level 3

         	# ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Wind Direction 10m (°) level 3

            if self.loader.code[i][25] != 3333 and self.loader.code[i][25] != -5555 and self.loader.code[i][25] != 552 and self.loader.code[i][25] != 529:
                if i <= totalWd1018h_1:
                    j = 0
                    while j <= self.wd1018h:
                        if self.loader.code[i+j][25] != 3333 and self.loader.code[i+j][25] != 552 and self.loader.code[i+j][25] != 529:
                            self.contWdirValid += 1
                            if self.loader.data[i+j][25] > self.wd10_max:
                                self.wd10_max = self.loader.data[i+j][25]
                            if self.loader.data[i+j][25] < self.wd10_min:
                                self.wd10_min = self.loader.data[i+j][25]
                            self.variation_wd1018h = self.wd10_max - self.wd10_min
                        j += 1

                    if self.contWdirValid >= 40:
                        if self.variation_wd1018h > 10:
                            self.loader.code[i][25] = 999
                            self.lastWd10Valid = self.loader.code[i][25]
                        else:
                            self.loader.code[i][25] = 299
                    else:
                        l = 0
                        while l <= self.wd1018h:
                            if self.loader.code[i+l][25] != 3333 and self.loader.code[i+l][25] != 552 and self.loader.code[i+l][25] != 529:
                                if i == 0:
                                    self.loader.code[i][25] = 559
                                else:
                                    self.loader.code[i][25] = self.lastWd10Valid
                            l += 1
                        self.contWdirValid = 0
                        self.wd10_max = 0
                        self.wd10_min = 999

                if i >= totalWd1018h_2:
                    self.loader.code[i][25] = self.loader.code[totalWd1018h_1][25]

            # End of the routine validation: Wind Direction 10m (°) level 3

         	# ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Direct Radiation (W/m²) level 3

            if self.loader.code[i][28] != 3333 and self.loader.code[i][28] != -5555 and self.loader.code[i][28] != -6999 and self.loader.code[i][28] != 552 and self.loader.code[i][28] != 29:
                if self.loader.code[i][8] != 3333 and self.loader.code[i][8] != -5555 and self.loader.code[i][8] != -6999 and self.loader.code[i][8] != 552 and self.loader.code[i][8] != 529:
                    if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552 and self.loader.code[i][4] != 529:
                        direct_h = self.loader.data[i][4] - self.loader.data[i][8]
                        direct_n = (self.loader.data[i][28] * self.u0) - 50
                        direct_p = (self.loader.data[i][28] * self.u0) + 50

                        if direct_n <= direct_h and direct_h <= direct_p:
                            self.loader.code[i][28] = 999
                        else:
                            self.loader.code[i][28] = 299

                    else:
                        if self.loader.code[i][28] == 99:
                            self.loader.code[i][28] = 599

                else:
                    if self.loader.code[i][28] == 99:
                        self.loader.code[i][28] = 599

            else:
                if self.loader.code[i][28] == 29:
                    self.loader.code[i][28] = 529

            # End of the routine validation: Direct Radiation (W/m²) level 3

            # ----------------------------------------------------------------------------------------------------------------------

         	# Start of the routine validation: Long Wave Radiation (W/m²) level 3

            if self.loader.code[i][32] != 3333 and self.loader.code[i][32] != -5555 and self.loader.code[i][32] != -6999 and self.loader.code[i][32] != 552 and self.loader.code[i][32] != 29:
                if self.loader.code[i][20] != 3333 and self.loader.code[i][20] != -5555 and self.loader.code[i][20] != 552 and self.loader.code[i][20] != 529:
                    temp =  self.loader.data[i][20] + 273.15
                    temp_a = 0.4 * sigma * (temp ** 4)
                    temp_b = sigma * (temp ** 4) + 25

                    if temp_a < self.loader.data[i][32] and self.loader.data[i][32] < temp_b:
                        self.loader.code[i][32] = 999
                    else:
                        self.loader.code[i][32] = 299

                else:
                    if self.loader.code[i][32] == 99:
                        self.loader.code[i][32] = 599

            else:
                if self.loader.code[i][32] == 29:
                    self.loader.code[i][32] = 529

            self.pb.update(1)

            # End of the routine validation: Long Wave Radiation (W/m²) level 3

            # ----------------------------------------------------------------------------------------------------------------------

            # End of loop level 3

        # Start level 4
        # Define vertical ozone layer thickness value (cm)
        # Iqbal average table (5.3.2)
        if latitude >= -10:
            L = 0.24
        elif latitude < -10 and latitude >= -20:
            L = 0.25
        elif latitude < -20 and latitude >= -30:
            L = 0.28
        elif latitude < -30 and latitude >= -40:
            L = 0.30

        # Start level 4

        np.seterr(all='ignore')

        for i in range(self.rows + 1):
            self.num = self.loader.data[i][3]
            self.div = self.num / 60
            self.dia_jul = int(self.loader.data[i][2])

            # Calculating astronomical geometry data
            self.day_angle = (2 * np.pi / 365.25 * self.dia_jul)
            self.dec = (self.d0 - self.dc1 * np.cos(self.day_angle) + self.ds1 * np.sin(
                self.day_angle) - self.dc2 * np.cos(2 * self.day_angle) + self.ds2 * np.sin(
                2 * self.day_angle) - self.dc3 * np.cos(3 * self.day_angle) + self.ds3 * np.sin(3 * self.day_angle))
            self.eqtime = (self.et0 + self.tc1 * np.cos(self.day_angle) - self.ts1 * np.sin(
                self.day_angle) - self.tc2 * np.cos(2 * self.day_angle) - self.ts2 * np.sin(
                2 * self.day_angle)) * 229.18
            self.tcorr = (self.eqtime + 4 * (longitude - 0)) / 60
            self.horacorr = self.tcorr + self.div
            self.hour_angle = (12.00 - self.horacorr) * 15
            self.e0 = self.e1 + self.e2 * np.cos(self.day_angle) + self.e3 * np.sin(
                self.day_angle) + self.e4 * np.cos(2 * self.day_angle) + self.e5 * np.sin(2 * self.day_angle)
            self.u0 = np.sin(self.dec) * np.sin(latitude * self.CDR) + np.cos(self.dec) * np.cos(
                latitude * self.CDR) * np.cos(self.hour_angle * self.CDR)
            self.zenith_angle = (np.arccos(self.u0)) * 180 / np.pi
            self.sa = 1368 * self.e0

            if self.loader.code[i][22] == 99 and self.loader.code[i][20] == 999 and self.loader.code[i][21] == 9:

                # Relative optical mass applied
                Mr = 1 / (np.cos(self.zenith_angle))

                # Relative optical mass
                Ma = Mr * (self.loader.data[i][22] / 1013.25)

                # Ozone relative optical path length
                U3 = L * Mr

                # Water vapor
                Ps = np.exp(26.23 - (5416 / self.loader.data[i][20] + 273.15))

                # Precipitable water in terms of relative humidity
                Pw = 0.493 * (self.loader.data[i][21] / 100) * (Ps / (self.loader.data[i][20] + 273.15))

                # Pressure-corrected relative optical path length of precipitable water
                U1 = Pw * Mr

                # Transmittance by Rayleigh scattering

                Tr = np.exp(-0.0903*(Ma**0.84)*(1.0 + Ma - (Ma**1.01)))

                # Transmittance by ozone
                To = 1-(0.1611*U3*((1.0+139.48*U3)**(-0.3035))-0.002715*U3*((1.0+0.44*U3+0.0003*(U3**2))**(-1)))

                # Transmittance by uniformely mixed gases
                Tg = np.exp(-0.0127*Ma**0.26)

                # Transmittance by water vapor
                Tw = 1-2.4959*U1*((((1.0+79.034*U1)**0.6828)+(6.385*U1))**(-1))

                # Aerosol optical thickness - Kah(0.38)=0.087 and Kah(0.5)=0.069
                Ka = (0.2758*0.087) + (0.35*0.069)

                # Aerosol transmittance
                Ta = np.exp(-Ka**0.0873*(1.0+Ka-(Ka**0.07088))*(Ma**0.9108))

                # Ecentricy correction factor of the earth's orbit
                Eo = 1+(0.033*np.cos(((2*np.pi*self.dia_jul)/365)))

                # Direct normal irradiance
                Irn = Eo*0.9751*self.Isc*Tr*To*Tg*Tw*Ta

                # Extraterrestrial irradiance on a horizontal surface
                Io = Eo*self.Isc*np.cos(self.zenith_angle)

                # Total beam irradiance on a horizontal surface
                Ib = Irn*np.cos(self.zenith_angle)

                # Transmittance of direct radiation due to aerosol absortance
                Taa = 1-(1-self.Wo)*(1-Ma+(Ma**1.06)*(1-Ta))

                # Ration between Ta/Taa
                Tas = Ta/Taa

                # Reyleigh-scattered diffuse irradiance
                Idr = Eo*0.79*self.Isc*(np.cos(self.zenith_angle))*To*Tg*Tw*Taa*0.5*((1-Tr)/(1-Ma+(Ma**1.02)))

                # Aerosol-scattered diffuse irradiance
                Ida = Eo*0.79*self.Isc*(np.cos(self.zenith_angle))*To*Tg*Tw*Taa*(self.Fc*(1-Tas))/(1-Ma+(Ma**1.02))

                # Albedo for cloudless sky
                Pa = 0.0685+(1-self.Fc)*(1-Tas)

                # Ground albedo
                Pg = 0.2

                # Diffuse irradiance produced by multiple reflections between ground and atmosphere
                Idm = (Irn*(np.cos(self.zenith_angle))+Idr+Ida)*Pg*Pa/(1-Pg*Pa)

                # Total diffuse irradiance on a horizontal surface
                Idiff = Idr+Ida+Idm

                # Total global irradiance on a horizontal surface
                self.Iglob = Ib + Idiff

                self.porc = (self.loader.data[i][4] * 100) / self.Iglob

                # Validation for global irradiance
                if self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999 and self.loader.code[i][4] != 552 and self.loader.code[i][4] != 529 and self.loader.code[i][4] != 299:
                    if self.loader.data[i][4]:
                        if self.Iglob > 1367 or Idiff <= 0:
                            self.loader.code[i][4] += 2000
                        else:
                            porc_10 = self.Iglob * 0.1
                            if self.loader.data[i][4] <= (self.Iglob + porc_10):
                                self.loader.code[i][4] += 9000
                            else:
                                self.loader.code[i][4] += 2000
                elif self.loader.code[i][4] == 552 or self.loader.code[i][4] == 529 or self.loader.code[i][4] == 299:
                    self.loader.code[i][4] += 5000
            elif self.loader.code[i][4] != 3333 and self.loader.code[i][4] != -5555 and self.loader.code[i][4] != -6999:
                self.loader.code[i][4] += 5000

            # Write global irradiance
            self.loader.clearSky[i][0] = self.Iglob
            self.loader.clearSky[i][1] = self.loader.data[i][4]
            self.loader.clearSky[i][2] = self.porc
            self.Iglob = None
            self.porc = None

            # Sum count

            self.pb.update(1)
            self.cont += 1

        self.pb.close()
        return self.loader.code, self.loader.clearSky

