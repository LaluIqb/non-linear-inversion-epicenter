import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import matplotlib.tri as tri


# Mendefinisikan parameter yang diketahui
to=0         
v=4        
t_dat=np.array((7.1, 2.8, 5, 7.9))         
x=np.array((20, 50, 40, 10))            
y=np.array((10, 25, 50, 40))            
n=len(x)


# Menambahkan noise random dengan mean 0, standar deviasi 2, dan x=0.01 
noise = np.random.normal(0,2,t_dat.shape)

for i in range (0,n):
    t_dat[i] = t_dat[i]+noise[i]*0.01

# Mendefinisikan grid untuk nilai error
grid_x = np.random.uniform(0, 60, 50)
grid_y = np.random.uniform(0, 60, 50)
g=len(grid_x)


# Menghitung nilai error untuk setiap grid
t_cal = np.ones((n))
E = np.zeros((g))
E_total = np.zeros((g))

for i in range (0,g):
    for j in range (0,n):
        t_cal[j] = (np.sqrt((x[j]-grid_x[i])**2+(y[j]-grid_y[i])**2))/v
        E[(i)] = E[(i)] + np.sqrt(((t_cal[j]-t_dat[j])**2)/n)
                
    
# Melakukan plot grafis 
fig = pl.subplots(figsize=(8, 4))

xi = np.linspace(0, 60, 100)
yi = np.linspace(0, 60, 100)

triang = tri.Triangulation(grid_x, grid_y)
interpolator = tri.LinearTriInterpolator(triang, E)
Xi, Yi = np.meshgrid(xi, yi)
zi = interpolator(Xi, Yi)

c3 = plt.contourf(xi, yi, zi,35, levels=14, cmap="coolwarm")

plt.plot(grid_x,grid_y,'.k', label='Sampel')

cbar = pl.colorbar(c3)       
cbar.set_label('Error (s)', rotation=270, labelpad=15, y=0.5)

plt.plot(x,y,'vk', markersize=10, label='Stasiun')
for i in range (n):
    plt.text(x[i]-1.5,y[i]+2,'St'+ str(i+1))

plt.xlabel('Easting')       
plt.ylabel('Northing')
plt.title('Plot Epicenter', fontsize=20)

# Plot manual
plt.plot(40,30,'*r', markersize=10, label='Error Minimum Global \n(Epicenter)')

plt.legend(bbox_to_anchor=(1.2, 0.15), loc='upper left')
plt.tight_layout()

plt.show()
