import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from scipy import interpolate


# Mendefinisikan parameter yang diketahui
to=0         
v=4                 
x=np.array((20, 50, 40, 10))            
y=np.array((10, 25, 50, 40))            
n=len(x)


M=np.array((40,30))       # Solusi Model (Epicenter)


# Menghitung t dari data stasiun dengan x,y epicenter 40,30
t_dat = np.ones((n))

for i in range (0,n):      
    t_dat[i] = (np.sqrt((x[i]-40)**2+(y[i]-30)**2))/v


# Menambahkan noise random dengan mean 0, standar deviasi 2, dan x=0.01 
noise = np.random.normal(0,2,t_dat.shape)

for i in range (0,n):
    t_dat[i] = t_dat[i]+noise[i]*0.01


# Mendefinisikan grid untuk nilai error
grid_x = []
grid_y = []

for i in range (0,61,2):
    grid_x.append(i)
    grid_y.append(i)

grid_x=np.array(grid_x)
grid_y=np.array(grid_y)
g=len(grid_x)


# Menghitung nilai error untuk setiap grid
t_cal = np.ones((n))
E = np.zeros((g,g))

for i in range (0,g):
    for j in range (0,g):
        for k in range (0,n):
            t_cal[k] = (np.sqrt((x[k]-grid_x[i])**2+(y[k]-grid_y[j])**2))/v
            E[(i,j)] = E[(i,j)] + np.sqrt(((t_cal[k]-t_dat[k])**2)/n)
                
    
# Melakukan plot grafis 
fig = pl.subplots(figsize=(8, 4))

X, Y = np.mgrid[0:60:31j, 0:60:31j]
rbf = interpolate.Rbf(X.ravel(), Y.ravel(), E.ravel(), smooth=0.000001)

X2, Y2 = np.mgrid[0:60:60j, 0:60:60j]
c3 = pl.contourf(X2, Y2, rbf(X2, Y2),25, cmap='coolwarm')

cbar = pl.colorbar(c3)       
cbar.set_label('Error (s)', rotation=270, labelpad=15, y=0.5)

plt.plot(x,y,'vk', markersize=10, label='Stasiun')
for i in range (n):
    plt.text(x[i]-1.5,y[i]+2,'St'+ str(i+1))

plt.xlabel('Easting')       
plt.ylabel('Northing')
plt.title('Plot Epicenter', fontsize=20)

# Plot epicenter
plt.plot(M[0],M[1],'*r', markersize=10, label='Error Minimum Global \n(Epicenter)')

plt.legend(bbox_to_anchor=(1.2, 0.15), loc='upper left')
plt.tight_layout()

plt.show()
