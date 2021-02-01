import calendar
import numpy as np

np.seterr(over='ignore')

def corrected_hour(year, latitude, longitude, altitude, turbidity):
    # Ls A LONGITUDE PADRAO PARA O BRASIL É DE -45. SE QUISER USAR UTC, Ls = 0
    Ls = 0

    # SERA CALCULADO SE O ANO É BISSEXTO E QUANTAS HORAS E MINUTOS EXISTEM EM UM ANO
    days_year = 366 if calendar.isleap(year) else 365
    days = np.arange(1, days_year+1)
    hour_year = days_year*24

    # QUANTOS MINUTOS E HORAS EXISTEM EM UM ANO
    hours = []
    for i in range(days_year):
        for k in range(24):
            hours.append(k+1)

    # FAZENDO O CABECARIO PARA A COLUNA DO ANO
    year_hours = []
    for i in range(days_year):
        for k in range(24):
            year_hours.append(year)

    # AJUSTE DO DIA JULIANO PARA O ANO EM QUESTAO EM MINUTOS OU HORAS
    day_jul_hours = []
    for i in range(days_year):
        for k in range(24):
            day_jul_hours.append(days[i])

    # CALCULO DOS MESES COM BASE NO DIA JULIANO PARA CADA HORA
    month_hour = []
    for i in range(day_jul_hours[-1]*24):
        if days_year == 366:
            if day_jul_hours[i] <= 31:
                month_hour.append(1)
            elif day_jul_hours[i] > 31 and day_jul_hours[i] <= 60:
                month_hour.append(2)
            elif day_jul_hours[i] > 60 and day_jul_hours[i] <= 91:
                month_hour.append(3)
            elif day_jul_hours[i] > 91 and day_jul_hours[i] <= 121:
                month_hour.append(4)
            elif day_jul_hours[i] > 121 and day_jul_hours[i] <= 152:
                month_hour.append(5)
            elif day_jul_hours[i] > 152 and day_jul_hours[i] <= 182:
                month_hour.append(6)
            elif day_jul_hours[i] > 182 and day_jul_hours[i] <= 213:
                month_hour.append(7)
            elif day_jul_hours[i] > 213 and day_jul_hours[i] <= 244:
                month_hour.append(8)
            elif day_jul_hours[i] > 244 and day_jul_hours[i] <= 274:
                month_hour.append(9)
            elif day_jul_hours[i] > 274 and day_jul_hours[i] <= 305:
                month_hour.append(10)
            elif day_jul_hours[i] > 305 and day_jul_hours[i] <= 335:
                month_hour.append(11)
            elif day_jul_hours[i] > 335 and day_jul_hours[i] <= 366:
                month_hour.append(12)
        else:
            if day_jul_hours[i] <= 31:
                month_hour.append(1)
            elif day_jul_hours[i] > 31 and day_jul_hours[i] <= 59:
                month_hour.append(2)
            elif day_jul_hours[i] > 59 and day_jul_hours[i] <= 90:
                month_hour.append(3)
            elif day_jul_hours[i] > 90 and day_jul_hours[i] <= 120:
                month_hour.append(4)
            elif day_jul_hours[i] > 120 and day_jul_hours[i] <= 151:
                month_hour.append(5)
            elif day_jul_hours[i] > 151 and day_jul_hours[i] <= 181:
                month_hour.append(6)
            elif day_jul_hours[i] > 181 and day_jul_hours[i] <= 212:
                month_hour.append(7)
            elif day_jul_hours[i] > 212 and day_jul_hours[i] <= 243:
                month_hour.append(8)
            elif day_jul_hours[i] > 243 and day_jul_hours[i] <= 273:
                month_hour.append(9)
            elif day_jul_hours[i] > 273 and day_jul_hours[i] <= 304:
                month_hour.append(10)
            elif day_jul_hours[i] > 304 and day_jul_hours[i] <= 334:
                month_hour.append(11)
            elif day_jul_hours[i] > 334 and day_jul_hours[i] <= 365:
                month_hour.append(12)

    # CALCULO DOS DIAS COM BASE NOS MESES PARA CADA MINUTO E HORA
    day_hour = []
    for i in range(day_jul_hours[-1]*24):
        if days_year == 366:
            if month_hour[i] == 1:
                day_hour.append(day_jul_hours[i])
            elif month_hour[i] == 2:
                day_hour.append(day_jul_hours[i] - 31)
            elif month_hour[i] == 3:
                day_hour.append(day_jul_hours[i] - 60)
            elif month_hour[i] == 4:
                day_hour.append(day_jul_hours[i] - 91)
            elif month_hour[i] == 5:
                day_hour.append(day_jul_hours[i] - 121)
            elif month_hour[i] == 6:
                day_hour.append(day_jul_hours[i] - 152)
            elif month_hour[i] == 7:
                day_hour.append(day_jul_hours[i] - 182)
            elif month_hour[i] == 8:
                day_hour.append(day_jul_hours[i] - 213)
            elif month_hour[i] == 9:
                day_hour.append(day_jul_hours[i] - 244)
            elif month_hour[i] == 10:
                day_hour.append(day_jul_hours[i] - 274)
            elif month_hour[i] == 11:
                day_hour.append(day_jul_hours[i] - 305)
            elif month_hour[i] == 12:
                day_hour.append(day_jul_hours[i] - 335)
        else:
            if month_hour[i] == 1:
                day_hour.append(day_jul_hours[i])
            elif month_hour[i] == 2:
                day_hour.append(day_jul_hours[i] - 31)
            elif month_hour[i] == 3:
                day_hour.append(day_jul_hours[i] - 59)
            elif month_hour[i] == 4:
                day_hour.append(day_jul_hours[i] - 90)
            elif month_hour[i] == 5:
                day_hour.append(day_jul_hours[i] - 120)
            elif month_hour[i] == 6:
                day_hour.append(day_jul_hours[i] - 151)
            elif month_hour[i] == 7:
                day_hour.append(day_jul_hours[i] - 181)
            elif month_hour[i] == 8:
                day_hour.append(day_jul_hours[i] - 212)
            elif month_hour[i] == 9:
                day_hour.append(day_jul_hours[i] - 243)
            elif month_hour[i] == 10:
                day_hour.append(day_jul_hours[i] - 273)
            elif month_hour[i] == 11:
                day_hour.append(day_jul_hours[i] - 304)
            elif month_hour[i] == 12:
                day_hour.append(day_jul_hours[i] - 334)

    # CALCULO DO LINK TURBIDITY PARA CADA MESES DO ANO EM MINUTO
    link_turbidity_hour = []
    for i in range(day_jul_hours[-1]*24):
        if month_hour[i] == 1:
            link_turbidity_hour.append(turbidity['January.tif']/20)
        elif month_hour[i] == 2:
            link_turbidity_hour.append(turbidity['February.tif']/20)
        elif month_hour[i] == 3:
            link_turbidity_hour.append(turbidity['March.tif']/20)
        elif month_hour[i] == 4:
            link_turbidity_hour.append(turbidity['April.tif']/20)
        elif month_hour[i] == 5:
            link_turbidity_hour.append(turbidity['May.tif']/20)
        elif month_hour[i] == 6:
            link_turbidity_hour.append(turbidity['June.tif']/20)
        elif month_hour[i] == 7:
            link_turbidity_hour.append(turbidity['July.tif']/20)
        elif month_hour[i] == 8:
            link_turbidity_hour.append(turbidity['August.tif']/20)
        elif month_hour[i] == 9:
            link_turbidity_hour.append(turbidity['September.tif']/20)
        elif month_hour[i] == 10:
            link_turbidity_hour.append(turbidity['October.tif']/20)
        elif month_hour[i] == 11:
            link_turbidity_hour.append(turbidity['November.tif']/20)
        elif month_hour[i] == 12:
            link_turbidity_hour.append(turbidity['December.tif']/20)

    # LACO PARA SER EFETUADO OS CALCULOS DO CLEAR SKY USANDO O METODO DE DUMORTIER
    clear_sky_hour = []
    for i in range(day_jul_hours[-1]*24):
        # CALCULO DA DECLINACAO SOLAR EM RADS
        day_angle = (0.017201916*day_jul_hours[i])

        dec = (0.006918 - 0.399912 * np.cos(day_angle) + 0.070257 * np.sin(day_angle) - 0.006758 * np.cos(2* day_angle) + 0.000907 * np.sin(2* day_angle) - 0.002697 * np.cos(3* day_angle) + 0.001480 * np.sin(3* day_angle))

        # CALCULO DA EQUACAO DO TEMPO EM HORA
        eqtime = (0.000075 + 0.001868 * np.cos(day_angle) - 0.032077 * np.sin(day_angle) - 0.014615 * np.cos(2* day_angle) - 0.040849 * np.sin(2* day_angle))*(3.82)
        # CALCULO DO TEMPO TOTAL TRANSCORRIDO OU HORA SOLAR EM MINUTO
        tcorr = (hours[i] + ((longitude - Ls)/15) + eqtime)
        # CALCULO DO ANGULO HORARIO EM GRAU
        hour_angle = (12.00 - tcorr)* 15
        # CALCULO DA DISTÂNCIA MÉDIA TERRA-SOL PARA CADA DIA JULIANO
        e0 = 1.00011 + 0.034221 * np.cos(day_angle) + 0.00128 * np.sin(day_angle) + 0.000719 * np.cos(2 * day_angle) + 0.000077 * np.sin(2 * day_angle)
        # CALCULO DO ÂNGULO ZÊNITAL, COSENO DO ANGULO ZENITAL E DO ANGULO DE ELEVAÇÃO
        u0 = ((np.sin(dec) * np.sin(latitude*np.pi/180)) + (np.cos(dec) * np.cos(latitude*np.pi/180) * np.cos(hour_angle*np.pi/180)))
        zenit_angle = (np.arccos(u0))*180/np.pi
        elevation_angle = (90 - zenit_angle)
        # CALCULO DA RADIAÇÃO SOLAR NO TOPO DA ATMOSFERA EM (W/m2)
        TOA = 1367 * e0 * u0
        if TOA < 0:
            TOA = 0
        # CALCULO DA RELATIVE OPTICAL AIR MASS (M)
        delta_elevation_angle = ((0.061359 * (180/np.pi)) * (((0.1594 + ((1.1230) * (np.pi/180) * (elevation_angle))) + (0.065656 * ((np.pi/180)**2) * (elevation_angle**2))) / ((1 + (28.9344 * (np.pi/180) * elevation_angle)) + (277.3971 * ((np.pi/180)**2) * (elevation_angle**2)))))
        true_elevation_angle = elevation_angle + delta_elevation_angle

        M = np.real((np.exp((-altitude)/8434.5))/(np.sin(true_elevation_angle*(np.pi/180))+(0.50572*((6.07995 + np.array(true_elevation_angle, dtype=np.complex))**(-1.6364)))))

        # CALCULO DO Aer: IS THE OPTICAL THICKNESS OF RAYLEIGH
        if M <= 20:
            Aer = ((1)/(6.6296 + 1.7513*(M) - 0.1202*(M**2) + 0.0065*(M**3) - 0.00013*(M**4)))
        elif M > 20:
            Aer = ((1)/(10.4 + (0.718*(M))))
        else:
            Aer = 0
        # CALCULO DA COMPOMENTE DIRETA DA RADIAÇÂO SOLAR
        Ees = 1367 * e0 * np.sin(elevation_angle*(np.pi/180)) * np.exp(-0.8662 * link_turbidity_hour[i] * M * Aer)

        if Ees < 0:
            Ees = 0
        # CALCULO DA COMPOMENTE DIFUSSA DA RADIAÇÃO SOLAR
        Eed = 1367 * e0 *  (0.0065 + (-0.045 + (0.0646 * link_turbidity_hour[i] * np.sin(elevation_angle*(np.pi/180)) - (-0.014 + (0.0327 * link_turbidity_hour[i] * (np.sin(elevation_angle*(np.pi/180)) * (np.sin(elevation_angle*(np.pi/180)))))))))

        if Eed < 0:
            Eed = 0
        # CALCULO DA RADIAÇÃO SOLAR GLOBAL
        IRg = Ees + Eed

        # SALVANDO O CLEAR_SKY PARA CADA MINUTO DO ANO
        data_array = [year_hours[i], month_hour[i], day_hour[i], day_jul_hours[i], hours[i], TOA, Ees, Eed, IRg]
        clear_sky_hour.append(data_array)
    return clear_sky_hour
