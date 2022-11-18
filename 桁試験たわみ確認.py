#ライブラリのインポート
import pandas as pd
import numpy as np
import math


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
xl = int(xl[0]/10)

#初期値の代入
M = np.zeros(n)
for k in range(1,n):
    for j in range(k,n):
        M[k] = M[k] + (f[j]*(x[j]-x[k]))/1000 ##曲げモーメントの計算

phi = np.zeros(n)
z = np.zeros(n)
y = np.zeros(n)

#たわみ角→たわみ量→引張方向の縮む方向の計算
for i in range(1, n):
     phi[i] = phi[i - 1] + 0.5 * (M[i - 1]/ei[i-1] + M[i]/ei[i])*dx + (dihedral[i] - dihedral[i - 1]) * math.pi / 180.0
     z[i] = z[i - 1] + 1.11 * 0.5 * (math.sin(phi[i - 1]) + math.sin(phi[i])) * dx
     y[i] = y[i - 1] + 0.5 * (math.cos(phi[i - 1]) + math.cos(phi[i])) * dx
     deflection = z[n - 1]*1000
     stretching = x[-1] - y[n - 1]*1000

print('翼端部最大たわみ量(ウィングレット含む)は' + str(deflection) + 'mmです')
print('ｘ軸方向に縮んだ量は' + str(stretching) + 'mmです')
print('桁端部最大たわみ量(Eclatだと6番桁端部)は' + str(z[xl]*1000) + 'mmです')