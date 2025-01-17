import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from sample_dehnendf import get_samples_with_z
from galpy.util.bovy_conversion import time_in_Gyr

norbits = 1000
t = np.linspace(0, 1/time_in_Gyr(vo=220., ro=8.), 1000)

orbits = get_samples_with_z(n=norbits, integration_steps=1000)
Rs = np.stack([o.R(t) for o in orbits], axis=1)
zs = np.stack([o.z(t) for o in orbits], axis=1)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set(xlim=(0,2), ylim=(-0.2, 0.2), xlabel='$R/R_0$', ylabel='$z/R_0$')
scatter = ax.scatter(Rs[0], zs[0], s=5)

def animate(i):
    scatter.set_offsets(np.c_[Rs[i], zs[i]])
    ax.set(title='t = {:.2f}'.format(t[i]))
    
anim = animation.FuncAnimation(fig, animate, interval=33, frames=len(Rs)-1)
plt.draw()
plt.show()

if not os.path.exists('animations'):
    os.mkdir('animations')

anim.save('animations/{}_samples.gif'.format(norbits), writer='imagemagick')
