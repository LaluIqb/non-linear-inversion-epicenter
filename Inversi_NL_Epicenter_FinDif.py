import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

# Mendefinisikan parameter yang diketahui
to=0         
v=4        
t_dat=np.array((7.1, 2.8, 5, 7.9))         
x=np.array((20, 50, 40, 10))            
y=np.array((10, 25, 50, 40))            
n=len(x)


M0=np.array((30,10))      # Initial Model


t_cal= np.ones((n))
J = np.ones((n,2))    
M=M0
l=1

while True:
    
    print('\n----------------------------------------------------')
    print('\nMelakukan iterasi',l,'\n')
    
    for j in range (0,n):
        
        # Asumsi peturbasi 5% =0.05
        pet = 0.05
        t = to+(1/v)*(np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
        dt_dx = (np.sqrt((M0[0]+(pet*M0[0])-x[j])**2+(M0[1]-y[j])**2))-(np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
        dt_dy = (np.sqrt((M0[0]-x[j])**2+(M0[1]+(pet*M0[1])-y[j])**2))-(np.sqrt((M0[0]-x[j])**2+(M0[1]-y[j])**2))
    
        J[(j,0)] = dt_dx/(v*pet*M0[0])
        J[(j,1)] = dt_dy/(v*pet*M0[1])
        t_cal[j] = t
        
    print('Matriks jacobian:')
    print(J)

    # Estimasi lokasi epicenter baru
    dM = (inv((J.T).dot(J))).dot(J.T).dot(t_dat-t_cal)    
    M_new = M0 + dM
    print('\nPrediksi lokasi epicenter (Xo, Yo):')
    print(M_new)    
    
    M=np.append(M,M_new, axis=0)
    
    # Membuat Kriteria pemberhentian estimasi berdasarkan error estimasi
    err_0 = abs(M0[0]-M_new[0])
    err_1 = abs(M0[1]-M_new[1])
    print('\nError yang didapatkan untuk estimasi Xo dan Yo adalah',err_0,'dan',err_1)

    if err_0< 0.05:     
        if err_1< 0.05: 
            print('\n\nEstimasi telah memenuhi kriteria pemberhentian iterasi!')
            break
    
    M0=M_new
    l=l+1

# Mengumpulkan hasil estimasi untuk setiap iterasi
m=int(len(M)/2)
M_plot=M.reshape(m,2)
print('\nBerikut adalah tabel estimasi lokasi Epicenter untuk tiap iterasi')
print(M_plot)

# Melakukan plot grafis
xplot=[]
yplot=[]
for i in range (0,m):
    xplot.append(M_plot[(i,0)])
    yplot.append(M_plot[(i,1)])    
    
plt.figure(figsize = (8, 5))    #ukuran plot
    
plt.plot(xplot,yplot,'o-b', label='Prediksi Epicenter')
plt.plot(x,y,'vk', markersize=10, label='Stasiun')
for i in range (n):
    plt.text(x[i]-1.5,y[i]+2,'St'+ str(i+1))

m=m-1
plt.plot(xplot[m], yplot[m], '*r', markersize=10, label='Lokasi Epicenter')

plt.axis((0,60,0,60))
plt.xlabel('Easting')
plt.ylabel('Northing')
plt.title('Plot Epicenter', fontsize=20)

plt.legend(bbox_to_anchor=(1.1, 0), loc='lower left')
plt.tight_layout()