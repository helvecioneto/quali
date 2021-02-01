import numpy as np
import datetime

class Loader:

    # Init function, setting parameters to the respective attributes (None if not passed)
    def __init__(self, rawData=None, numberOfColumns=None, numberOfRows=None):
        self.rawData = np.array(rawData)
        self.numberOfColumns = numberOfColumns
        self.numberOfRows = numberOfRows
        self.temp = np.array([])
        self.data = np.array([])
        self.limits = np.array([])
        self.code = np.array([])
        self.clearSky = np.array([])

        self.line = None

        # Object basic variables and constants
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
        self.ts2 = 004.00890

        self.u0 = None
        self.zenith_angle = None
        self.day_angle = None
        self.dec = None
        self.eqtime = None
        self.tcorr = None
        self.hour_angle = None

        self.CDR = np.pi / 180
        self.num = None
        self.dia_jul = None
        self.horacorr = None
        self.div = None

        self.cont_gl1n = 0
        self.cont_gl2n = 0
        self.cont_gl3n = 0
        self.cont_gl4n = 0
        self.cont_glna = 0
        self.cont_glv = 0

        self.cont_di1n = 0
        self.cont_di2n = 0
        self.cont_di3n = 0
        self.cont_dina = 0
        self.cont_div = 0

        self.cont_df1n = 0
        self.cont_df2n = 0
        self.cont_df3n = 0
        self.cont_dfna = 0
        self.cont_dfv = 0

        self.cont_lw1n = 0
        self.cont_lw2n = 0
        self.cont_lw3n = 0
        self.cont_lwna = 0
        self.cont_lwv = 0

        self.cont_pa1n = 0
        self.cont_pa2n = 0
        self.cont_pa3n = 0
        self.cont_pana = 0
        self.cont_pav = 0

        self.cont_lx1n = 0
        self.cont_lx2n = 0
        self.cont_lx3n = 0
        self.cont_lxna = 0
        self.cont_lxv = 0

        self.cont_tp1n = 0
        self.cont_tp2n = 0
        self.cont_tp3n = 0
        self.cont_tpna = 0
        self.cont_tpv = 0

        self.cont_hu1n = 0
        self.cont_huna = 0
        self.cont_huv = 0

        self.cont_ps1n = 0
        self.cont_ps2n = 0
        self.cont_psna = 0
        self.cont_psv = 0

        self.cont_pc1n = 0
        self.cont_pc2n = 0
        self.cont_pc3n = 0
        self.cont_pcna = 0
        self.cont_pcv = 0

        self.cont_ws1n = 0
        self.cont_ws2n = 0
        self.cont_ws3n = 0
        self.cont_wsna = 0
        self.cont_wsv = 0

        self.cont_wd1n = 0
        self.cont_wd2n = 0
        self.cont_wd3n = 0
        self.cont_wdna = 0
        self.cont_wdv = 0

        self.cont_vgl = 0
        self.cont_nagl = 0
        self.cont_vdi = 0
        self.cont_nadi = 0
        self.cont_vdf = 0
        self.cont_nadf = 0
        self.cont_vlw = 0
        self.cont_nalw = 0
        self.cont_vpa = 0
        self.cont_napa = 0
        self.cont_vlx = 0
        self.cont_nalx = 0

        self.flag_gl = 0
        self.flag_di = 0
        self.flag_df = 0
        self.flag_lw = 0
        self.flag_pa = 0
        self.flag_lx = 0
        self.flag_tp = 0
        self.flag_hu = 0
        self.flag_ps = 0
        self.flag_pc = 0
        self.flag_ws = 0
        self.flag_wd = 0

        self.med_gl1n = None
        self.med_gl2n = None
        self.med_gl3n = None
        self.med_gl4n = None
        self.med_glna = None
        self.med_glv = None

        self.med_di1n = None
        self.med_di2n = None
        self.med_di3n = None
        self.med_dina = None
        self.med_div = None

        self.med_df1n = None
        self.med_df2n = None
        self.med_df3n = None
        self.med_dfna = None
        self.med_dfv = None

        self.med_lw1n = None
        self.med_lw2n = None
        self.med_lw3n = None
        self.med_lwna = None
        self.med_lwv = None

        self.med_pa1n = None
        self.med_pa2n = None
        self.med_pa3n = None
        self.med_pana = None
        self.med_pav = None

        self.med_lx1n = None
        self.med_lx2n = None
        self.med_lx3n = None
        self.med_lxna = None
        self.med_lxv = None

        self.med_tp1n = None
        self.med_tp2n = None
        self.med_tp3n = None
        self.med_tpna = None
        self.med_tpv = None

        self.med_hu1n = None
        self.med_huna = None
        self.med_huv = None

        self.med_ps1n = None
        self.med_ps2n = None
        self.med_psna = None
        self.med_psv = None

        self.med_pc1n = None
        self.med_pc2n = None
        self.med_pc3n = None
        self.med_pcna = None
        self.med_pcv = None

        self.med_ws1n = None
        self.med_ws2n = None
        self.med_ws3n = None
        self.med_wsna = None
        self.med_wsv = None

        self.med_wd1n = None
        self.med_wd2n = None
        self.med_wd3n = None
        self.med_wdna = None
        self.med_wdv = None

    # Função criada mas não utilizada
    def extractLines(self, input, output, id):
        try:
            bfIn = open(input, 'r')
            try:
                bfOut = open(output, 'w')
                for line in bfIn:
                    if line[0:3] != id:
                        bfOut.write(line)
                        bfOut.write('\n')
                bfOut.close()
            except IOError:
                raise IOError
            finally:
                bfIn.close()
        except IOError:
            raise IOError

    def read(self, input):
        try:
            bfIn = open(input, 'r')
            newArray = []
            for line in bfIn:
                token = line.split(',')
                if self.numberOfColumns is None or self.numberOfColumns == 0:
                    self.numberOfColumns = len(token)
                lines = np.array(token, dtype=float)
                newArray.append(lines)
            self.rawData = np.array(newArray)
            if self.rawData is not None:
                self.numberOfRows = self.rawData.shape[0]
            bfIn.close()
        except IOError:
            raise IOError("Erro durante a leitura do arquivo: ", input)
        except ValueError:
            raise ValueError("Arquivo com problema de formatação: ", input)

    # Método de arredondamento diferente do Java
    # Diminuir função
    def writeData(self, output, dataArray, clearSkyArray, id, month):
        try:
            bfOut = open(output, 'w')
            for i in range(len(dataArray)):
                # Header
                bfOut.write(f"{id};")
                bfOut.write(f"{dataArray[i][1]:.0f};")
                bfOut.write(f"{dataArray[i][2]:.0f};")
                bfOut.write(f"{dataArray[i][3]:.0f};")
                day = datetime.datetime.strptime((str(int(float(dataArray[i][2])))), '%j').date().day
                dt = datetime.datetime(int(dataArray[i][1]), int(month), day, int(dataArray[i][3]/60), int(dataArray[i][3])%60)
                bfOut.write(f"{dt};")

                # Print Global Radiation AVG 60s
                if dataArray[i][4] == 3333 or dataArray[i][4] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][4] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][4] == 0:
                    bfOut.write(f"{dataArray[i][4]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][4]:5.3f};")

                # Print Direct Radiation AVG 60s
                if dataArray[i][28] == 3333 or dataArray[i][28] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][28] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][28] == 0:
                    bfOut.write(f"{dataArray[i][28]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][28]:5.3f};")

                # Print Diffuse Radiation AVG 60s
                if dataArray[i][8] == 3333 or dataArray[i][8] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][8] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][8] == 0:
                    bfOut.write(f"{dataArray[i][8]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][8]:5.3f};")

                # Print LongWave Radiation AVG 60s
                if dataArray[i][32] == 3333 or dataArray[i][32] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][32] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][32] == 0:
                    bfOut.write(f"{dataArray[i][32]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][32]:.1f};")

                # Print Par Radiation AVG 60s
                if dataArray[i][12] == 3333 or dataArray[i][12] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][12] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][12] == 0:
                    bfOut.write(f"{dataArray[i][12]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][12]:5.3f};")

                # Print Lux Radiation AVG 60s
                if dataArray[i][16] == 3333 or dataArray[i][16] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][16] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][16] == 0:
                    bfOut.write(f"{dataArray[i][16]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][16]:5.3f};")

                # Print Air Temperature AVG 60s
                if dataArray[i][20] == 3333 or dataArray[i][20] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][20] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][20] == 0:
                    bfOut.write(f"{dataArray[i][20]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][20]:5.2f};")

                # Print Relative Humidity AVG 60s
                if dataArray[i][21] == 3333 or dataArray[i][21] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][21] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][21] == 0:
                    bfOut.write(f"{dataArray[i][21]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][21]:5.2f};")

                # Print Atmospheric Pressure AVG 60s
                if dataArray[i][22] == 3333 or dataArray[i][22] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][22] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][22] == 0:
                    bfOut.write(f"{dataArray[i][22]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][22]:5.2f};")

                # Print Accumulated Precipitation AVG 60s
                if dataArray[i][23] == 3333 or dataArray[i][23] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][23] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][23] == 0:
                    bfOut.write(f"{dataArray[i][23]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][23]:.1f};")

                # Print Wind Speed AVG 60s
                if dataArray[i][24] == 3333 or dataArray[i][24] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][24] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][24] == 0:
                    bfOut.write(f"{dataArray[i][24]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][24]:5.3f};")

                # Print Wind Direction AVG 60s
                if dataArray[i][25] == 3333 or dataArray[i][25] == -6999:
                    bfOut.write("N/A;")
                elif dataArray[i][25] == -5555:
                    bfOut.write("N/S;")
                elif dataArray[i][25] == 0:
                    bfOut.write(f"{dataArray[i][25]:.0f};")
                else:
                    bfOut.write(f"{dataArray[i][25]:.1f};")

                bfOut.write("\n")

            bfOut.close()
        except IOError:
            raise IOError("Erro durante a escrita do arquivo: ", output)

    # Diminuir função
    def writeCode(self, output, dataArray, codeArray, id, month):
        try:
            bfOut = open(output, 'w')
            for i in range(len(dataArray)):
                # Header
                bfOut.write(f"{id};")
                bfOut.write(f"{dataArray[i][1]:.0f};")
                bfOut.write(f"{dataArray[i][2]:.0f};")
                bfOut.write(f"{dataArray[i][3]:.0f};")
                day = datetime.datetime.strptime((str(int(float(dataArray[i][2])))), '%j').date().day
                dt = datetime.datetime(int(dataArray[i][1]), int(month), day, int(dataArray[i][3]/60), int(dataArray[i][3])%60)
                bfOut.write(f"{dt};")

                # Global Radiation
                if codeArray[i][4] == 3333 or codeArray[i][4] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][4] == -5555:
                    bfOut.write("N/S;")
                else:
                    bfOut.write(f"{codeArray[i][4]:.0f};")

                # Direct Radiation
                if codeArray[i][28] == 999:
                    bfOut.write(f"{codeArray[i][28]:04.0f};")
                elif codeArray[i][28] == 599:
                    bfOut.write(f"{codeArray[i][28]:04.0f};")
                elif codeArray[i][28] == 529:
                    bfOut.write(f"{codeArray[i][28]:04.0f};")
                elif codeArray[i][28] == 299:
                    bfOut.write(f"{codeArray[i][28]:04.0f};")
                elif codeArray[i][28] == 552:
                    bfOut.write(f"{codeArray[i][28]:04.0f};")
                elif codeArray[i][28] == 3333 or codeArray[i][28] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][28] == -5555:
                    bfOut.write("N/S;")

                # Diffuse Radiation
                if codeArray[i][8] == 999:
                    bfOut.write(f"{codeArray[i][8]:04.0f};")
                elif codeArray[i][8] == 599:
                    bfOut.write(f"{codeArray[i][8]:04.0f};")
                elif codeArray[i][8] == 529:
                    bfOut.write(f"{codeArray[i][8]:04.0f};")
                elif codeArray[i][8] == 299:
                    bfOut.write(f"{codeArray[i][8]:04.0f};")
                elif codeArray[i][8] == 552:
                    bfOut.write(f"{codeArray[i][8]:04.0f};")
                elif codeArray[i][8] == 3333 or codeArray[i][8] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][8] == -5555:
                    bfOut.write("N/S;")

                # Long-Wave
                if codeArray[i][32] == 999:
                    bfOut.write(f"{codeArray[i][32]:04.0f};")
                elif codeArray[i][32] == 599:
                    bfOut.write(f"{codeArray[i][32]:04.0f};")
                elif codeArray[i][32] == 529:
                    bfOut.write(f"{codeArray[i][32]:04.0f};")
                elif codeArray[i][32] == 299:
                    bfOut.write(f"{codeArray[i][32]:04.0f};")
                elif codeArray[i][32] == 552:
                    bfOut.write(f"{codeArray[i][32]:04.0f};")
                elif codeArray[i][32] == 3333 or codeArray[i][32] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][32] == -5555:
                    bfOut.write("N/S;")

                # Par
                if codeArray[i][12] == 999:
                    bfOut.write(f"{codeArray[i][12]:04.0f};")
                elif codeArray[i][12] == 599:
                    bfOut.write(f"{codeArray[i][12]:04.0f};")
                elif codeArray[i][12] == 529:
                    bfOut.write(f"{codeArray[i][12]:04.0f};")
                elif codeArray[i][12] == 299:
                    bfOut.write(f"{codeArray[i][12]:04.0f};")
                elif codeArray[i][12] == 552:
                    bfOut.write(f"{codeArray[i][12]:04.0f};")
                elif codeArray[i][12] == 3333 or codeArray[i][12] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][12] == -5555:
                    bfOut.write("N/S;")

                # Lux
                if codeArray[i][16] == 999:
                    bfOut.write(f"{codeArray[i][16]:04.0f};")
                elif codeArray[i][16] == 599:
                    bfOut.write(f"{codeArray[i][16]:04.0f};")
                elif codeArray[i][16] == 529:
                    bfOut.write(f"{codeArray[i][16]:04.0f};")
                elif codeArray[i][16] == 299:
                    bfOut.write(f"{codeArray[i][16]:04.0f};")
                elif codeArray[i][16] == 552:
                    bfOut.write(f"{codeArray[i][16]:04.0f};")
                elif codeArray[i][16] == 3333 or codeArray[i][16] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][16] == -5555:
                    bfOut.write("N/S;")

                # Temperature
                if codeArray[i][20] == 999:
                    bfOut.write(f"{codeArray[i][20]:04.0f};")
                elif codeArray[i][20] == 559:
                    bfOut.write(f"{codeArray[i][20]:04.0f};")
                elif codeArray[i][20] == 529:
                    bfOut.write(f"{codeArray[i][20]:04.0f};")
                elif codeArray[i][20] == 299:
                    bfOut.write(f"{codeArray[i][20]:04.0f};")
                elif codeArray[i][20] == 552:
                    bfOut.write(f"{codeArray[i][20]:04.0f};")
                elif codeArray[i][20] == 3333:
                    bfOut.write("N/A;")
                elif codeArray[i][20] == -5555:
                    bfOut.write("N/S;")

                # Humidity
                if codeArray[i][21] == 9:
                    bfOut.write(f"{codeArray[i][21]:04.0f};")
                elif codeArray[i][21] == 552:
                    bfOut.write(f"{codeArray[i][21]:04.0f};")
                elif codeArray[i][21] == 3333:
                    bfOut.write("N/A;")
                elif codeArray[i][21] == -5555:
                    bfOut.write("N/S;")

                # Pressure
                if codeArray[i][22] == 99:
                    bfOut.write(f"{codeArray[i][22]:04.0f};")
                elif codeArray[i][22] == 559:
                    bfOut.write(f"{codeArray[i][22]:04.0f};")
                elif codeArray[i][22] == 529:
                    bfOut.write(f"{codeArray[i][22]:04.0f};")
                elif codeArray[i][22] == 299:
                    bfOut.write(f"{codeArray[i][22]:04.0f};")
                elif codeArray[i][22] == 552:
                    bfOut.write(f"{codeArray[i][22]:04.0f};")
                elif codeArray[i][22] == 3333:
                    bfOut.write("N/A;")
                elif codeArray[i][22] == -5555:
                    bfOut.write("N/S;")

                # Precipitation
                if codeArray[i][23] == 999:
                    bfOut.write(f"{codeArray[i][23]:04.0f};")
                elif codeArray[i][23] == 559:
                    bfOut.write(f"{codeArray[i][23]:04.0f};")
                elif codeArray[i][23] == 529:
                    bfOut.write(f"{codeArray[i][23]:04.0f};")
                elif codeArray[i][23] == 299:
                    bfOut.write(f"{codeArray[i][23]:04.0f};")
                elif codeArray[i][23] == 552:
                    bfOut.write(f"{codeArray[i][23]:04.0f};")
                elif codeArray[i][23] == 3333:
                    bfOut.write("N/A;")
                elif codeArray[i][23] == -5555:
                    bfOut.write("N/S;")

                # Speed
                if codeArray[i][24] == 999:
                    bfOut.write(f"{codeArray[i][24]:04.0f};")
                elif codeArray[i][24] == 559:
                    bfOut.write(f"{codeArray[i][24]:04.0f};")
                elif codeArray[i][24] == 529:
                    bfOut.write(f"{codeArray[i][24]:04.0f};")
                elif codeArray[i][24] == 299:
                    bfOut.write(f"{codeArray[i][24]:04.0f};")
                elif codeArray[i][24] == 552:
                    bfOut.write(f"{codeArray[i][24]:04.0f};")
                elif codeArray[i][24] == 3333:
                    bfOut.write("N/A;")
                elif codeArray[i][24] == -5555:
                    bfOut.write("N/S;")

                # Direction
                if codeArray[i][25] == 999:
                    bfOut.write(f"{codeArray[i][25]:04.0f}")
                elif codeArray[i][25] == 559:
                    bfOut.write(f"{codeArray[i][25]:04.0f}")
                elif codeArray[i][25] == 529:
                    bfOut.write(f"{codeArray[i][25]:04.0f}")
                elif codeArray[i][25] == 299:
                    bfOut.write(f"{codeArray[i][25]:04.0f}")
                elif codeArray[i][25] == 552:
                    bfOut.write(f"{codeArray[i][25]:04.0f}")
                elif codeArray[i][25] == 3333:
                    bfOut.write("N/A")
                elif codeArray[i][25] == -5555:
                    bfOut.write("N/S")

                bfOut.write("\n")

            bfOut.close()
        except IOError:
            raise IOError("Erro durante a escrita do arquivo: ", output)

    def writeClearSky(self, output, dataArray, codeArray, clearSkyArray, id, month):
        try:
            bfOut = open(output, 'w')
            for i in range(len(clearSkyArray)):
                bfOut.write(f"{id};")
                bfOut.write(f"{dataArray[i][1]:.0f};")
                bfOut.write(f"{dataArray[i][2]:.0f};")
                bfOut.write(f"{dataArray[i][3]:.0f};")
                day = datetime.datetime.strptime((str(int(float(dataArray[i][2])))), '%j').date().day
                dt = datetime.datetime(int(dataArray[i][1]), int(month), day, int(dataArray[i][3]/60), int(dataArray[i][3])%60)
                bfOut.write(f"{dt};")

                if codeArray[i][4] == 3333 or codeArray[i][4] == -6999:
                    bfOut.write("N/A;")
                elif codeArray[i][4] == -5555:
                    bfOut.write("N/S;")
                else:
                    bfOut.write(f"{codeArray[i][4]:.0f};")

                if np.isnan(clearSkyArray[i][0]) or clearSkyArray[i][0] > 1367 or clearSkyArray[i][0] < -1367:
                    bfOut.write("N/A;")
                else:
                    bfOut.write(f"{clearSkyArray[i][0]:5.3f};")

                bfOut.write(f"{clearSkyArray[i][1]:5.3f};")

                if np.isnan(clearSkyArray[i][2]):
                    bfOut.write("N/A")
                else:
                    bfOut.write(f"{clearSkyArray[i][2]:5.3f}")
                bfOut.write("\n")
            bfOut.close()
        except IOError:
            raise IOError("Erro durante a escrita do arquivo: ", output)



    # Diminuir função
    def writeReportData(self, output, station, year, month, id, codeArray, latitude, longitude):
        try:
            bfOut = open(output, 'w')
            for i in range(len(codeArray)):
                # Tirar cálculos repetidos em FOR
                self.num = self.data[i][3]
                self.div = self.num / 60
                self.dia_jul = int(self.data[i][2])

                self.day_angle = (2 * np.pi) / (365.25 * self.dia_jul)
                self.dec = (self.d0 - self.dc1 * np.cos(self.day_angle) + self.ds1 * np.sin(self.day_angle) - self.dc2 * np.cos(2 * self.day_angle) + self.ds2 * np.sin(2 * self.day_angle) - self.dc3 * np.cos(3 * self.day_angle) + self.ds3 * np.sin(3 * self.day_angle))

                self.eqtime = (self.et0 + self.tc1 * np.cos(self.day_angle) - self.ts1 * np.sin(self.day_angle) - self.tc2 * np.cos(2 * self.day_angle) - self.ts2 * np.sin(2 * self.day_angle)) * 229.18

                self.tcorr = (self.eqtime + 4 * (longitude - 0)) / 60

                self.horacorr = self.tcorr + self.div

                self.hour_angle = (12.00 - self.horacorr) * 15

                self.u0 = np.sin(self.dec) * np.sin(latitude * self.CDR) + np.cos(self.dec) * np.cos(latitude * self.CDR) * np.cos(self.hour_angle * self.CDR)

                self.zenith_angle = (np.arccos(self.u0)) * 180 / np.pi

                # ------------------ Código em Java não trata caso zenith_angle == 90 ---------------
                # colocar <= 90, discutir depois
                if self.zenith_angle < 90:

                    # Global Radiation
                    if codeArray[i][4] == 9999 or codeArray[i][4] == 9599:
                        self.cont_glv += 1
                    elif codeArray[i][4] == 5599:
                        self.cont_glv += 1
                    elif codeArray[i][4] == 5999:
                        self.cont_glv += 1
                    elif codeArray[i][4] == 5552:
                        self.cont_gl1n += 1
                    elif codeArray[i][4] == 5529:
                        self.cont_gl2n += 1
                    elif codeArray[i][4] == 5299:
                        self.cont_gl3n += 1
                    elif codeArray[i][4] == 2999 or codeArray[i][4] == 2599:
                        self.cont_gl4n += 1
                    elif codeArray[i][4] == -5555:
                        self.flag_gl = 1
                    elif codeArray[i][4] == 3333 or codeArray[i][4] == -6999:
                        self.cont_glna += 1

                    # Direct Radiation
                    if codeArray[i][28] == 999:
                        self.cont_div += 1
                    elif codeArray[i][28] == 599:
                        self.cont_div += 1
                    elif codeArray[i][28] == 552:
                        self.cont_di1n += 1
                    elif codeArray[i][28] == 529:
                        self.cont_di2n += 1
                    elif codeArray[i][28] == 299:
                        self.cont_di3n += 1
                    elif codeArray[i][28] == -5555:
                        self.flag_di = 1
                    elif codeArray[i][28] == 3333 or codeArray[i][28] == -6999:
                        self.cont_dina += 1

                    # Diffuse Radiation
                    if codeArray[i][8] == 999:
                        self.cont_dfv += 1
                    elif codeArray[i][8] == 599:
                        self.cont_dfv += 1
                    elif codeArray[i][8] == 552:
                        self.cont_df1n += 1
                    elif codeArray[i][8] == 529:
                        self.cont_df2n += 1
                    elif codeArray[i][8] == 299:
                        self.cont_df3n += 1
                    elif codeArray[i][8] == -5555:
                        self.flag_df = 1
                    elif codeArray[i][8] == 3333 or codeArray[i][8] == -6999:
                        self.cont_dfna += 1

                    # Long Wave
                    if codeArray[i][32] == 999:
                        self.cont_lwv += 1
                    elif codeArray[i][32] == 599:
                        self.cont_lwv += 1
                    elif codeArray[i][32] == 552:
                        self.cont_lw1n += 1
                    elif codeArray[i][32] == 529:
                        self.cont_lw2n += 1
                    elif codeArray[i][32] == 299:
                        self.cont_lw3n += 1
                    elif codeArray[i][32] == -5555:
                        self.flag_lw = 1
                    elif codeArray[i][32] == 3333 or codeArray[i][32] == -6999:
                        self.cont_lwna += 1

                    # Par
                    if codeArray[i][12] == 999:
                        self.cont_pav += 1
                    elif codeArray[i][12] == 599:
                        self.cont_pav += 1
                    elif codeArray[i][12] == 552:
                        self.cont_pa1n += 1
                    elif codeArray[i][12] == 529:
                        self.cont_pa2n += 1
                    elif codeArray[i][12] == 299:
                        self.cont_pa3n += 1
                    elif codeArray[i][32] == -5555:
                        self.flag_pa = 1
                    elif codeArray[i][12] == 3333 or codeArray[i][12] == -6999:
                        self.cont_pana += 1

                    # Lux
                    if codeArray[i][16] == 999:
                        self.cont_lxv += 1
                    elif codeArray[i][16] == 599:
                        self.cont_lxv += 1
                    elif codeArray[i][16] == 552:
                        self.cont_lx1n += 1
                    elif codeArray[i][16] == 529:
                        self.cont_lx2n += 1
                    elif codeArray[i][16] == 299:
                        self.cont_lx3n += 1
                    elif codeArray[i][16] == -5555:
                        self.flag_lx = 1
                    elif codeArray[i][16] == 3333 or codeArray[i][16] == -6999:
                        self.cont_lxna += 1

                if self.zenith_angle > 90:

                    # Global Radiation
                    if codeArray[i][4] == 3333 or codeArray[i][4] == -6999:
                        self.cont_nagl += 1

                    if codeArray[i][4] != 3333 and codeArray[i][4] != -6999:
                        self.cont_vgl += 1

                    # Direct Radiation
                    if codeArray[i][28] == 3333 or codeArray[i][28] == -6999:
                        self.cont_nadi += 1

                    if codeArray[i][28] != 3333 and codeArray[i][28] != -6999:
                        self.cont_vdi += 1

                    # Diffuse Radiation
                    if codeArray[i][8] == 3333 or codeArray[i][8] == -6999:
                        self.cont_nadf += 1

                    if codeArray[i][8] != 3333 and codeArray[i][8] != -6999:
                        self.cont_vdf += 1

                    # Long Wave
                    if codeArray[i][32] == 3333 or codeArray[i][32] == -6999:
                        self.cont_nalw += 1

                    if codeArray[i][32] != 3333 and codeArray[i][32] != -6999:
                        self.cont_vlw += 1

                    # Par
                    if codeArray[i][12] == 3333 or codeArray[i][12] == -6999:
                        self.cont_napa += 1

                    if codeArray[i][12] != 3333 and codeArray[i][12] != -6999:
                        self.cont_vpa += 1

                    # Lux
                    if codeArray[i][16] == 3333 or codeArray[i][16] == -6999:
                        self.cont_nalx += 1

                    if codeArray[i][16] != 3333 and codeArray[i][16] != -6999:
                        self.cont_vlx += 1

                # Air Temperature
                if codeArray[i][20] == 999:
                    self.cont_tpv += 1
                elif codeArray[i][20] == 559:
                    self.cont_tpv += 1
                elif codeArray[i][20] == 552:
                    self.cont_tp1n += 1
                elif codeArray[i][20] == 529:
                    self.cont_tp2n += 1
                elif codeArray[i][20] == 299:
                    self.cont_tp3n += 1
                elif codeArray[i][20] == -5555:
                    self.flag_tp = 1
                elif codeArray[i][20] == 3333:
                    self.cont_tpna += 1

                # Relative Humidity
                if codeArray[i][21] == 9:
                    self.cont_huv += 1
                elif codeArray[i][21] == 552:
                    self.cont_hu1n += 1
                elif codeArray[i][21] == -5555:
                    self.flag_hu = 1
                elif codeArray[i][21] == 3333:
                    self.cont_huna += 1

                # Atmospheric Pressure
                if codeArray[i][22] == 99:
                    self.cont_psv += 1
                elif codeArray[i][22] == 559:
                    self.cont_psv += 1
                elif codeArray[i][22] == 552:
                    self.cont_ps1n += 1
                elif codeArray[i][22] == 529:
                    self.cont_ps2n += 1
                elif codeArray[i][22] == -5555:
                    self.flag_ps = 1
                elif codeArray[i][22] == 3333:
                    self.cont_psna += 1

                # Accumulated Precipitation
                if codeArray[i][23] == 999:
                    self.cont_pcv += 1
                elif codeArray[i][23] == 559:
                    self.cont_pcv += 1
                elif codeArray[i][23] == 552:
                    self.cont_pc1n += 1
                elif codeArray[i][23] == 529:
                    self.cont_pc2n += 1
                elif codeArray[i][23] == 299:
                    self.cont_pc3n += 1
                elif codeArray[i][23] == -5555:
                    self.flag_pc = 1
                elif codeArray[i][23] == 3333:
                    self.cont_pcna += 1

                # Wind Speed
                if codeArray[i][24] == 999:
                    self.cont_wsv += 1
                elif codeArray[i][24] == 559:
                    self.cont_wsv += 1
                elif codeArray[i][24] == 552:
                    self.cont_ws1n += 1
                elif codeArray[i][24] == 529:
                    self.cont_ws2n += 1
                elif codeArray[i][24] == 299:
                    self.cont_ws3n += 1
                elif codeArray[i][24] == -5555:
                    self.flag_ws = 1
                elif codeArray[i][24] == 3333:
                    self.cont_wsna += 1

                # Wind Direction
                if codeArray[i][25] == 999:
                    self.cont_wdv += 1
                elif codeArray[i][25] == 559:
                    self.cont_wdv += 1
                elif codeArray[i][25] == 552:
                    self.cont_wd1n += 1
                elif codeArray[i][25] == 529:
                    self.cont_wd2n += 1
                elif codeArray[i][25] == 299:
                    self.cont_wd3n += 1
                elif codeArray[i][25] == -5555:
                    self.flag_wd = 1
                elif codeArray[i][25] == 3333:
                    self.cont_wdna += 1

            # Global Radiation Percentages
            self.med_gl1n = (self.cont_gl1n * 100) / self.numberOfRows
            self.med_gl2n = (self.cont_gl2n * 100) / self.numberOfRows
            self.med_gl3n = (self.cont_gl3n * 100) / self.numberOfRows
            self.med_gl4n = (self.cont_gl4n * 100) / self.numberOfRows
            self.med_glna = ((self.cont_glna + self.cont_nagl) * 100) / self.numberOfRows
            self.med_glv = ((self.cont_glv + self.cont_vgl) * 100) / self.numberOfRows

            # Direct Radiation Percentages
            self.med_di1n = (self.cont_di1n * 100) / self.numberOfRows
            self.med_di2n = (self.cont_di2n * 100) / self.numberOfRows
            self.med_di3n = (self.cont_di3n * 100) / self.numberOfRows
            self.med_dina = ((self.cont_dina + self.cont_nadi) * 100) / self.numberOfRows
            self.med_div = ((self.cont_div + self.cont_vdi) * 100) / self.numberOfRows

            # Diffuse Radiation Percentages
            self.med_df1n = (self.cont_df1n * 100) / self.numberOfRows
            self.med_df2n = (self.cont_df2n * 100) / self.numberOfRows
            self.med_df3n = (self.cont_df3n * 100) / self.numberOfRows
            self.med_dfna = ((self.cont_dfna + self.cont_nadf) * 100) / self.numberOfRows
            self.med_dfv = ((self.cont_dfv + self.cont_vdf) * 100) / self.numberOfRows

            # Long Wave Radiation Percentages
            self.med_lw1n = (self.cont_lw1n * 100) / self.numberOfRows
            self.med_lw2n = (self.cont_lw2n * 100) / self.numberOfRows
            self.med_lw3n = (self.cont_lw3n * 100) / self.numberOfRows
            self.med_lwna = ((self.cont_lwna + self.cont_nalw) * 100) / self.numberOfRows
            self.med_lwv = ((self.cont_lwv + self.cont_vlw) * 100) / self.numberOfRows

            # Par Radiation Percentages
            self.med_pa1n = (self.cont_pa1n * 100) / self.numberOfRows
            self.med_pa2n = (self.cont_pa2n * 100) / self.numberOfRows
            self.med_pa3n = (self.cont_pa3n * 100) / self.numberOfRows
            self.med_pana = ((self.cont_pana + self.cont_napa) * 100) / self.numberOfRows
            self.med_pav = ((self.cont_pav + self.cont_vpa) * 100) / self.numberOfRows

            # Lux Radiation Percentages
            self.med_lx1n = (self.cont_lx1n * 100) / self.numberOfRows
            self.med_lx2n = (self.cont_lx2n * 100) / self.numberOfRows
            self.med_lx3n = (self.cont_lx3n * 100) / self.numberOfRows
            self.med_lxna = ((self.cont_lxna + self.cont_nalx) * 100) / self.numberOfRows
            self.med_lxv = ((self.cont_lxv + self.cont_vlx) * 100) / self.numberOfRows

            # Air Temperature Percentages
            self.med_tp1n = (self.cont_tp1n * 100) / self.numberOfRows
            self.med_tp2n = (self.cont_tp2n * 100) / self.numberOfRows
            self.med_tp3n = (self.cont_tp3n * 100) / self.numberOfRows
            self.med_tpna = (self.cont_tpna * 100) / self.numberOfRows
            self.med_tpv = (self.cont_tpv * 100) / self.numberOfRows

            # Relative Humidity Percentages
            self.med_hu1n = (self.cont_hu1n * 100) / self.numberOfRows
            self.med_huna = (self.cont_huna * 100) / self.numberOfRows
            self.med_huv = (self.cont_huv * 100) / self.numberOfRows

            # Atmospheric Pressure Percentages
            self.med_ps1n = (self.cont_ps1n * 100) / self.numberOfRows
            self.med_ps2n = (self.cont_ps2n * 100) / self.numberOfRows
            self.med_psna = (self.cont_psna * 100) / self.numberOfRows
            self.med_psv = (self.cont_psv * 100) / self.numberOfRows

            # Accumulated Precipitation Percentages
            self.med_pc1n = (self.cont_pc1n * 100) / self.numberOfRows
            self.med_pc2n = (self.cont_pc2n * 100) / self.numberOfRows
            self.med_pc3n = (self.cont_pc3n * 100) / self.numberOfRows
            self.med_pcna = (self.cont_pcna * 100) / self.numberOfRows
            self.med_pcv = (self.cont_pcv * 100) / self.numberOfRows

            # Wind Speed Percentages
            self.med_ws1n = (self.cont_ws1n * 100) / self.numberOfRows
            self.med_ws2n = (self.cont_ws2n * 100) / self.numberOfRows
            self.med_ws3n = (self.cont_ws3n * 100) / self.numberOfRows
            self.med_wsna = (self.cont_wsna * 100) / self.numberOfRows
            self.med_wsv = (self.cont_wsv * 100) / self.numberOfRows

            # Wind Direction Percentages
            self.med_wd1n = (self.cont_wd1n * 100) / self.numberOfRows
            self.med_wd2n = (self.cont_wd2n * 100) / self.numberOfRows
            self.med_wd3n = (self.cont_wd3n * 100) / self.numberOfRows
            self.med_wdna = (self.cont_wdna * 100) / self.numberOfRows
            self.med_wdv = (self.cont_wdv * 100) / self.numberOfRows

            bfOut.write("Valores em Porcentagem dos Dados Suspeitos\n")
            bfOut.write("e ou Reprovados nos Níveis 1, 2 e 3, e Gaps N/A.\n\n\n")
            bfOut.write("Estação: {} ({} {})\n".format(station, output[0:3], id))
            bfOut.write("Data: {}-{}\n".format(month, year))
            bfOut.write("Qtde total de dados: {}\n\n".format(self.numberOfRows))

            # Printing levels of each percentage variable
            if self.flag_gl == 0:
                bfOut.write(f"Global Nível 1 = {self.med_gl1n:.2f}%\n")
                bfOut.write(f"Global Nível 2 = {self.med_gl2n:.2f}%\n")
                bfOut.write(f"Global Nível 3 = {self.med_gl3n:.2f}%\n")
                bfOut.write(f"Global Nível 4 = {self.med_gl4n:.2f}%\n")
                bfOut.write(f"Global Válido  = {self.med_glv:.2f}%\n")
                bfOut.write(f"Global N/A     = {self.med_glna:.2f}%\n\n")
            else:
                bfOut.write(f"Global Nível 1 = N/S\n")
                bfOut.write(f"Global Nível 2 = N/S\n")
                bfOut.write(f"Global Nível 3 = N/S\n")
                bfOut.write(f"Global Nível 4 = N/S\n")
                bfOut.write(f"Global Válido  = N/S\n")
                bfOut.write(f"Global N/A     = N/S\n\n")

            if self.flag_di == 0:
                bfOut.write(f"Direta Nível 1 = {self.med_di1n:.1f}%\n")
                bfOut.write(f"Direta Nível 2 = {self.med_di2n:.1f}%\n")
                bfOut.write(f"Direta Nível 3 = {self.med_di3n:.1f}%\n")
                bfOut.write(f"Direta Válido  = {self.med_div:.1f}%\n")
                bfOut.write(f"Direta N/A     = {self.med_dina:.1f}%\n\n")
            else:
                bfOut.write(f"Direta Nível 1 = N/S\n")
                bfOut.write(f"Direta Nível 2 = N/S\n")
                bfOut.write(f"Direta Nível 3 = N/S\n")
                bfOut.write(f"Direta Válido  = N/S\n")
                bfOut.write(f"Direta N/A     = N/S\n\n")

            if self.flag_df == 0:
                bfOut.write(f"Difusa Nível 1 = {self.med_df1n:.1f}%\n")
                bfOut.write(f"Difusa Nível 2 = {self.med_df2n:.1f}%\n")
                bfOut.write(f"Difusa Nível 3 = {self.med_df3n:.1f}%\n")
                bfOut.write(f"Difusa Válido  = {self.med_dfv:.1f}%\n")
                bfOut.write(f"Difusa N/A     = {self.med_dfna:.1f}%\n\n")
            else:
                bfOut.write(f"Difusa Nível 1 = N/S\n")
                bfOut.write(f"Difusa Nível 2 = N/S\n")
                bfOut.write(f"Difusa Nível 3 = N/S\n")
                bfOut.write(f"Difusa Válido  = N/S\n")
                bfOut.write(f"Difusa N/A     = N/S\n\n")

            if self.flag_lw == 0:
                bfOut.write(f"Onda Longa Nível 1 = {self.med_lw1n:.1f}%\n")
                bfOut.write(f"Onda Longa Nível 2 = {self.med_lw2n:.1f}%\n")
                bfOut.write(f"Onda Longa Nível 3 = {self.med_lw3n:.1f}%\n")
                bfOut.write(f"Onda Longa Válido  = {self.med_lwv:.1f}%\n")
                bfOut.write(f"Onda Longa N/A     = {self.med_lwna:.1f}%\n\n")
            else:
                bfOut.write(f"Onda Longa Nível 1 = N/S\n")
                bfOut.write(f"Onda Longa Nível 2 = N/S\n")
                bfOut.write(f"Onda Longa Nível 3 = N/S\n")
                bfOut.write(f"Onda Longa Válido  = N/S\n")
                bfOut.write(f"Onda Longa N/A     = N/S\n\n")

            if self.flag_pa == 0:
                bfOut.write(f"Par Nível 1 = {self.med_pa1n:.1f}%\n")
                bfOut.write(f"Par Nível 2 = {self.med_pa2n:.1f}%\n")
                bfOut.write(f"Par Nível 3 = {self.med_pa3n:.1f}%\n")
                bfOut.write(f"Par Válido  = {self.med_pav:.1f}%\n")
                bfOut.write(f"Par N/A     = {self.med_pana:.1f}%\n\n")
            else:
                bfOut.write(f"Par Nível 1 = N/S\n")
                bfOut.write(f"Par Nível 2 = N/S\n")
                bfOut.write(f"Par Nível 3 = N/S\n")
                bfOut.write(f"Par Válido  = N/S\n")
                bfOut.write(f"Par N/A     = N/S\n\n")

            if self.flag_lx == 0:
                bfOut.write(f"Lux Nível 1 = {self.med_lx1n:.1f}%\n")
                bfOut.write(f"Lux Nível 2 = {self.med_lx2n:.1f}%\n")
                bfOut.write(f"Lux Nível 3 = {self.med_lx3n:.1f}%\n")
                bfOut.write(f"Lux Válido  = {self.med_lxv:.1f}%\n")
                bfOut.write(f"Lux N/A     = {self.med_lxna:.1f}%\n\n")
            else:
                bfOut.write(f"Lux Nível 1 = N/S\n")
                bfOut.write(f"Lux Nível 2 = N/S\n")
                bfOut.write(f"Lux Nível 3 = N/S\n")
                bfOut.write(f"Lux Válido  = N/S\n")
                bfOut.write(f"Lux N/A     = N/S\n\n")

            if self.flag_tp == 0:
                bfOut.write(f"Temperatura Nível 1 = {self.med_tp1n:.1f}%\n")
                bfOut.write(f"Temperatura Nível 2 = {self.med_tp2n:.1f}%\n")
                bfOut.write(f"Temperatura Nível 3 = {self.med_tp3n:.1f}%\n")
                bfOut.write(f"Temperatura Válido  = {self.med_tpv:.1f}%\n")
                bfOut.write(f"Temperatura N/A     = {self.med_tpna:.1f}%\n\n")
            else:
                bfOut.write(f"Temperatura Nível 1 = N/S\n")
                bfOut.write(f"Temperatura Nível 2 = N/S\n")
                bfOut.write(f"Temperatura Nível 3 = N/S\n")
                bfOut.write(f"Temperatura Válido  = N/S\n")
                bfOut.write(f"Temperatura N/A     = N/S\n\n")

            if self.flag_hu == 0:
                bfOut.write(f"Umidade Nível 1 = {self.med_hu1n:.1f}%\n")
                bfOut.write(f"Umidade Válido  = {self.med_huv:.1f}%\n")
                bfOut.write(f"Umidade N/A     = {self.med_huna:.1f}%\n\n")
            else:
                bfOut.write(f"Umidade Nível 1 = N/S\n")
                bfOut.write(f"Umidade Válido  = N/S\n")
                bfOut.write(f"Umidade N/A     = N/S\n\n")

            if self.flag_ps == 0:
                bfOut.write(f"Pressão Nível 1 = {self.med_ps1n:.1f}%\n")
                bfOut.write(f"Pressão Nível 2 = {self.med_ps2n:.1f}%\n")
                bfOut.write(f"Pressão Válido  = {self.med_psv:.1f}%\n")
                bfOut.write(f"Pressão N/A     = {self.med_psna:.1f}%\n\n")
            else:
                bfOut.write(f"Pressão Nível 1 = N/S\n")
                bfOut.write(f"Pressão Nível 2 = N/S\n")
                bfOut.write(f"Pressão Válido  = N/S\n")
                bfOut.write(f"Pressão N/A     = N/S\n\n")

            if self.flag_pc == 0:
                bfOut.write(f"Precipitação Nível 1 = {self.med_pc1n:.1f}%\n")
                bfOut.write(f"Precipitação Nível 2 = {self.med_pc2n:.1f}%\n")
                bfOut.write(f"Precipitação Nível 3 = {self.med_pc3n:.1f}%\n")
                bfOut.write(f"Precipitação Válido  = {self.med_pcv:.1f}%\n")
                bfOut.write(f"Precipitação N/A     = {self.med_pcna:.1f}%\n\n")
            else:
                bfOut.write(f"Precipitação Nível 1 = N/S\n")
                bfOut.write(f"Precipitação Nível 2 = N/S\n")
                bfOut.write(f"Precipitação Nível 3 = N/S\n")
                bfOut.write(f"Precipitação Válido  = N/S\n")
                bfOut.write(f"Precipitação N/A     = N/S\n\n")

            if self.flag_ws == 0:
                bfOut.write(f"Vel. Vento Nível 1 = {self.med_ws1n:.1f}%\n")
                bfOut.write(f"Vel. Vento Nível 2 = {self.med_ws2n:.1f}%\n")
                bfOut.write(f"Vel. Vento Nível 3 = {self.med_ws3n:.1f}%\n")
                bfOut.write(f"Vel. Vento Válido  = {self.med_wsv:.1f}%\n")
                bfOut.write(f"Vel. Vento N/A     = {self.med_wsna:.1f}%\n\n")
            else:
                bfOut.write(f"Vel. Vento Nível 1 = N/S\n")
                bfOut.write(f"Vel. Vento Nível 2 = N/S\n")
                bfOut.write(f"Vel. Vento Nível 3 = N/S\n")
                bfOut.write(f"Vel. Vento Válido  = N/S\n")
                bfOut.write(f"Vel. Vento N/A     = N/S\n\n")

            if self.flag_wd == 0:
                bfOut.write(f"Dir. Vento Nível 1 = {self.med_wd1n:.1f}%\n")
                bfOut.write(f"Dir.Dir Vento Nível 2 = {self.med_wd2n:.1f}%\n")
                bfOut.write(f"Dir. Vento Nível 3 = {self.med_wd3n:.1f}%\n")
                bfOut.write(f"Dir. Vento Válido  = {self.med_wdv:.1f}%\n")
                bfOut.write(f"Dir. Vento N/A     = {self.med_wdna:.1f}%\n")
            else:
                bfOut.write(f"Dir. Vento Nível 1 = N/S\n")
                bfOut.write(f"Dir. Vento Nível 2 = N/S\n")
                bfOut.write(f"Dir. Vento Nível 3 = N/S\n")
                bfOut.write(f"Dir. Vento Válido  = N/S\n")
                bfOut.write(f"Dir. Vento N/A     = N/S\n")

            bfOut.close()

        except IOError:
            raise IOError("Erro durante a escrita do arquivo: ", output)

    # Matrix and max-min functions
    def buildsMatrixData(self, input):
        self.numberOfColumns = 0
        self.numberOfRows = 0
        self.read(input)
        self.data = np.array([])
        try:
            self.data = self.rawData
        except IndexError:
            raise IndexError("Erro ao Acessar Índice da Matriz")
        self.rawData = np.array([])

    def buildsMatrixCode(self, input):
        self.numberOfColumns = 0
        self.numberOfRows = 0
        # Verificar se é necessário read()
        self.read(input)
        self.code = np.ndarray(shape=(self.numberOfRows, self.numberOfColumns))
        self.clearSky = np.ndarray(shape=(self.numberOfRows, 3))

    def buildsMatrixLimits(self, input):
        self.numberOfColumns = 0
        self.numberOfRows = 0
        self.read(input)
        self.limits = np.array([])
        try:
            self.limits = self.rawData
        except IndexError:
            raise IndexError("Erro ao Acessar Índice da Matriz")
        self.rawData = np.array([])

    # Funções get iguais, diminuir para uma função
    # Diminuir tempo de execução de chamada (cada uma executa um read via MatrixLimits)
    # Usar variáveis estáticas em Controller.py para não executar a cada rodada
    def getTempMax(self, input, station, month):
        self.buildsMatrixLimits(input)
        temp_max = 0
        for i in range(self.numberOfRows):
            if self.limits[i][0] == station:
                temp_max = self.limits[i][month]
        return temp_max

    def getTempMin(self, input, station, month):
        self.buildsMatrixLimits(input)
        temp_min = 0
        for i in range(self.numberOfRows):
            if self.limits[i][0] == station:
                temp_min = self.limits[i][month]
        return temp_min

    def getPresMax(self, input, station):
        self.buildsMatrixLimits(input)
        pres_max = 0
        for i in range(self.numberOfRows):
            if self.limits[i][0] == station:
                pres_max = self.limits[i][1]
        return pres_max

    def getPresMin(self, input, station):
        self.buildsMatrixLimits(input)
        pres_min = 0
        for i in range(self.numberOfRows):
            if self.limits[i][0] == station:
                pres_min = self.limits[i][1]
        return pres_min

    def getPrecMax(self, input, station, month):
        self.buildsMatrixLimits(input)
        prec_max = 0
        for i in range(self.numberOfRows):
            if self.limits[i][0] == station:
                prec_max = self.limits[i][month]
        return prec_max

    # Getters
    def getCols(self):
        return self.numberOfColumns

    def getRows(self):
        return self.numberOfRows