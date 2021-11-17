import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

# Mendefinisikan parameter yang diketahui
to=0         
vp=4        
t_dat=np.array((7.1, 2.8, 5, 7.9))         
x=np.array((20, 50, 40, 10))            
y=np.array((10, 25, 50, 40))            
n=len(x)


M0=np.array((30,10))      # posisi tebakan awal(estimasi model awal)


t_cal= np.ones((n))
dt_dx = np.ones((n))
dt_dy = np.ones((n))
J = np.ones((n,2))    
M=M0


while True:
    
    for j in range (0,n):
        
        t = to+(1/vp)*(np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
        dt_dx = ((M0[0]-x[j]))/(vp*np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
        dt_dy = ((M0[1]-y[j]))/(vp*np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
    
        J[(j,0)] = dt_dx
        J[(j,1)] = dt_dy
        t_cal[j] = t
        
    print(J)
    dM = (inv((J.T).dot(J))).dot(J.T).dot(t_dat-t_cal)
    print(dM)
    M_new = M0 + dM
    print(M_new)    
    
    M=np.append(M,M_new, axis=0)
    
    err_0 = abs(M0[0]-M_new[0])
    print(err_0)
    err_1 = abs(M0[1]-M_new[1])
    print(err_1)

    if err_0< 0.05:
        if err_1< 0.05: 
            break
    
    M0=M_new

    

m=int(len(M)/2)
M_plot=M.reshape(m,2)
print(M_plot)

xplot=[]
yplot=[]
for i in range (0,m):
    xplot.append(M_plot[(i,0)])
    yplot.append(M_plot[(i,1)])    
    
plt.plot(xplot,yplot,'o-b', label='Prediksi Epicenter')
plt.plot(x,y,'vk', markersize=10, label='Stasiun')
m=m-1
plt.plot(xplot[m], yplot[m], '*r', markersize=10, label='Lokasi Epicenter')
plt.show()


