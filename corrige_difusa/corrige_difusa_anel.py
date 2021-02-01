import numpy as np
import csv
import sys
import os
from datetime import datetime

compare_data = {}
obsdata = []

stations = {
    'BAB': [-01.9311, -59.4197],
    'BJL': [-13.2335, -43.3760],
    'BRB': [-15.6008, -47.7131],
    'CPA': [-22.6896, -45.0062],
    'CAI': [-06.4669, -37.0847],
    'CGR': [-20.4383, -54.5383],
    'CHP': [-27.0800, -52.6144],
    'CBA': [-15.5553, -56.0700],
    'CTB': [-25.4954, -49.3312],
    'FLN': [-27.6017, -48.5178],
    'JOI': [-26.2525, -48.8578],
    'LEB': [-26.9886, -50.7150],
    'MCL': [-16.6864, -43.8688],
    'NAT': [-05.8367, -35.2064],
    'ORN': [-22.9486, -49.8942],
    'PMA': [-10.1778, -48.3619],
    'PTR': [-09.0689, -40.3197],
    'RLM': [-11.5817, -61.7736],
    'SLZ': [-02.5933, -44.2122],
    'SMS': [-29.4428, -53.8231],
    'SBR': [-29.0956, -49.8133],
    'TMA': [-05.3829, -36.8191],
    'TLG': [-20.7507, -51.6642],
    'UBE': [-19.9980, -47.9000],
}

# Matriz de correcao F conforme Tabela 5.2 do manual do anel KZ-CM 121
F = [
    [1.10, 1.11, 1.12, 1.12, 1.13, 1.13, 1.14, 1.14, 1.14],
    [1.11, 1.11, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.14],
    [1.11, 1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.14],
    [1.11, 1.12, 1.12, 1.13, 1.13, 1.14, 1.14, 1.14, 1.14],
    [1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.14, 1.14],
    [1.12, 1.12, 1.13, 1.13, 1.13, 1.14, 1.14, 1.13, 1.13],
    [1.12, 1.13, 1.13, 1.13, 1.13, 1.14, 1.13, 1.13, 1.13],
    [1.12, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.12],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.12, 1.12],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.12, 1.12],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.13, 1.12, 1.12, 1.11],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.12, 1.12, 1.11, 1.11],
    [1.13, 1.13, 1.13, 1.13, 1.13, 1.12, 1.12, 1.11, 1.10],
    [1.13, 1.13, 1.13, 1.13, 1.12, 1.12, 1.11, 1.11, 1.10],
    [1.13, 1.13, 1.13, 1.13, 1.12, 1.11, 1.11, 1.10, 1.09],
    [1.13, 1.13, 1.13, 1.12, 1.12, 1.11, 1.10, 1.10, 1.09],
    [1.13, 1.13, 1.12, 1.12, 1.11, 1.11, 1.10, 1.09, 1.08],
    [1.13, 1.13, 1.12, 1.12, 1.11, 1.10, 1.09, 1.09, 1.08],
    [1.13, 1.12, 1.12, 1.11, 1.11, 1.10, 1.09, 1.08, 1.08],
    [1.13, 1.12, 1.12, 1.11, 1.10, 1.09, 1.09, 1.08, 1.07],
    [1.12, 1.12, 1.11, 1.11, 1.10, 1.09, 1.08, 1.07, 1.07],
    [1.12, 1.12, 1.11, 1.10, 1.09, 1.08, 1.08, 1.07, 1.06],
    [1.12, 1.11, 1.11, 1.10, 1.09, 1.08, 1.07, 1.06, 1.05],
    [1.12, 1.11, 1.10, 1.09, 1.08, 1.08, 1.07, 1.06, 1.05],
]

def corrige_difusa_anel(path, lat, dx):
    name = os.path.basename(path)
    station_name = name[:3]

    if station_name in compare_data:
        station = compare_data[station_name]

        # Carrega dados das estações
        with open(os.path.abspath(path), 'r') as datafile:
            read_data = csv.reader(datafile, delimiter=',')
            for data in read_data:
                obsdata.append(data)

        codefile_w = open((os.path.abspath(path)), 'w')
        write_code = csv.writer(codefile_w, delimiter=';')

        # Vetores de indices latitude e declinacao
        declindex = np.array([-24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
        latindex = np.array([5, 0, -5, -10, -15, -20, -25, -30, -35])

        year = obsdata[0][1]
        month = name[5:-4]
        for data in obsdata:
            day = data[2]
            date = datetime.strptime(day+'-'+month+'-'+year, '%j-%m-%Y').date()
            if station[0] <= date <= station[1]:
                # Calcula declinação solar
                decl = -23.45*np.cos(2*np.pi*(int(day)+10)/365)
                # Calcula indice da latitude
                jlat = min(abs(latindex - lat))
                # Calcula indice da longitude
                idecl = min(abs(decl - declindex))
                # Corrige difusa
                k = F[int(round(idecl))][int(round(jlat))]
                data[dx] = '%.3f'%(k * float(data[dx]))
                write_code.writerow(data)



with open('estacoes_anel.csv', 'r') as datafile:
    read_data = csv.reader(datafile, delimiter=',')
    for data in read_data:
        compare_data[data[0]] = [datetime.strptime(data[1],'%d-%m-%Y').date(), datetime.strptime(data[2],'%d-%m-%Y').date()]

if len(sys.argv) == 1:
    print('Necessário especificar o(s) arquivo(s) .dat ao chamar o código')
else:
    path = './' + sys.argv[1]
    name = os.path.basename(path)
    corrige_difusa_anel(path, stations[name[:3]][0], 8)

























