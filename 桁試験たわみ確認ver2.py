#ライブラリのインポート
import pandas as pd
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

#対象のcsvファイルをインポート
data = pd.read_csv("for_deflection_check.csv" , encoding="shift-jis")

#各種データのインポート
x = data['位置'].tolist()
n = int(x[-1]/10)
dx = 10/1000
ei = data['曲げ剛性'].tolist()
dihedral = data['初期上反角'].tolist()
f = data['荷重分布'].tolist()
xl = data['桁端部位置'].tolist()
d = data['内径'].tolist()
D = data['外径'].tolist()
xl = int(xl[0]/10)
print(x[-1])

#初期値の代入
phi = np.zeros(n)
z = np.zeros(n)
y = np.zeros(n)
m = np.zeros(n)
I = np.zeros(n)
E = np.zeros(n)
deflection = 0
delta = 0
for i in range(0,n):
  I[i] = math.pi*((D[i]/1000)**4 - (d[i]/1000)**4)/64
  E[i] = ei[i]/I[i]


#モーメント・たわみ角・たわみ量の反復計算
for i in range(100):
    m = np.zeros(n)
    for k in range(1,n):
        for j in range(k,n):
            m[k] = m[k] + (f[j]*math.cos(phi[j]-phi[j-1]))*(x[j]-x[k])/1000

    phi = np.zeros(n)
    for p in range (1,n):
        phi[p] = phi[p-1] + 0.5*(m[p]/ei[p] + m[p-1]/ei[p-1])*dx +(dihedral[p] - dihedral[p-1])* math.pi / 180.0

    for h in range(1,n):
        z[h] = z[h - 1] + 1.11 * math.sin(phi[h]) * math.cos(2*phi[h]) * dx
        x[h] = x[h] - math.sin(phi[h]) * math.sin(2*phi[h]) * dx

    print(z[n - 1]*1000)
    if (abs(z[n - 1] - deflection) < 0.00000000000000001):
      break
    deflection = z[n - 1]

#桁長手方向圧縮方向の
for i in range(0,n):
  delta += + i*10 - x[i]

#モーメント・たわみ角・たわみ量の反復計算
print('翼端部最大たわみ量(ウィングレット含む)は' + str(deflection*1000) + 'mmです')
print('桁端部最大たわみ量(Eclatだと6番桁端部)は' + str(z[xl]*1000) + 'mmです')
print('桁長手方向圧縮量は' + str(delta) + 'mmです')