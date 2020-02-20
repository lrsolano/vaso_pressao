import numpy as np
from scipy import interpolate

#Tensões para o aço a285c
__temp1 =np.array([0,150,200,260,300,325,350,375,400,425,450,475])
__tensao1 = np.array([108,108,108,108,106,104,101,97,88.9,74.4,62.2,45.6])
__f = interpolate.interp1d(__temp1, __tensao1,kind="cubic")
__xnew = np.arange(0, (__temp1[-1]+1), 1)
a285c = __f(__xnew)

#Tensões para o aço a515-60
__tensao02 = np.array([117.8,117.8,117.8,117.8,114.3,111.5,108.0,103.2,88.9,74.4,62.2,45.6,32.3,22.0])
__temp02 =  np.array([0,150,200,260,300,325,350,375,400,425,450,475,500,525])
__f2 = interpolate.interp1d(__temp02,__tensao02,kind='cubic')
__xnew2 = np.arange(0,(__temp02[-1]+1),1)
a51560 = __f2(__xnew2)

#Tensões para o aço a516-60
__tensao03 = np.array([117.8,117.8,117.8,117.8,114.3,111.5,108.0,103.2,88.9,74.4,62.2,45.6,32.3,22.0])
__temp03 =  np.array([0,150,200,260,300,325,350,375,400,425,450,475,500,525])
__f3 = interpolate.interp1d(__temp03,__tensao03,kind='cubic')
__xnew3 = np.arange(0,(__temp03[-1]+1),1)
a51660 = __f3(__xnew3)

#Valores das constantes Kg(K9) e Kf(K6) 
__theta = np.array([120,135,150,165])
__k = np.array([0.204,0.231,0.259,0.288])
k_interpo = interpolate.interp1d(__theta,__k,kind='cubic')
__k2 = np.array([0.0528,0.0413,0.0316,0.0238])
k2_interpo = interpolate.interp1d(__theta,__k2,kind='cubic')

#Definir a espessura tabelada
def espessura(espessura):
    padrao = [6.30,8.00,9.50,12.50,16.0,19.0,22.40,25.40,28.50,32.50,35.0,37.50,44.50,50.0,57.0,70.0,75.0,89.0,100.0]
    for a in range(len(padrao)):
        if padrao[a] == espessura:
            return padrao[a]
        elif padrao[a] <= espessura and padrao[a+1] >= espessura:
            return padrao[a+1]
    if espessura < padrao[0]:
        return padrao[0]
    if espessura > padrao[-1]:
        return padrao[-1]
        