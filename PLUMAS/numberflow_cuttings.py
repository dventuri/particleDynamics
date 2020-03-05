"""
Created on Wed Jun 26 09:51:05 2019

PLUMAS project.
Calculates cuttings flow rate according to drilling profiles.
Considering only Non-aqueous fluid (NAF) drilling phase, with riser,
pre-centrifuge.
Using information from 2 sources:
[1] DIAS, Gerônimo Joaquim. "Modelagem tridimensional do lançamento de
rejeitos das atividades de exploração e produção de petróleo em águas
profundas." Master's thesis. Universidade Federal do Rio de Janeiro, 2005.
[2] PIVEL, M. A. G.; FREITAS, C. M. D. S.; COMBA, J. L. D. Modeling the
discharge of cuttings and drilling fluids in a deep-water environment.
"Deep-Sea Research II", 56, 12-21, 2009.
"""
import numpy as np
import matplotlib.pyplot as plt
# plt.style.use('default')

#Total volume of cuttings (input)
# total_volume = 815 #bbl (barrels)
total_volume = 642 #bbl (barrels) (from Pivel)
total_volume *= 0.1589873 #convert to m³

#Read and convert drilling data - time and depth
time, depth = np.loadtxt('./drilling_data.csv',
                         delimiter=',', skiprows=1, unpack=True)

time *= 60 # convert to seconds

#Check drilling profile
fig, ax = plt.subplots()
ax.plot(time/3600, depth, '-o', ms=15)
ax.set(xlabel='Time (h)', ylabel='Depth (m)')
ax.grid()

xs = [7.2,13,19,50,75,85,105,122]
ys = [-1900,-2200,-2450,-2450,-2550,-2650,-2700,-2850]
texts = ['Step 1','Step 2','Step 3','X','Step 4',' Step 5','X','Step 6']
for x,y,text in zip(xs,ys,texts):
    ax.text(x,y,text,fontsize=15,color='r')

plt.show()
# fig.savefig('PLUMAS/steps.png', dpi=500)

#Define 6 drilling steps (horizontal ones are neglected)
step_begin = [0,1,2,4,5,7]

#Interpolate total volume to drilling step volume
step_volume = np.zeros(6)
for i in range(6):
    stb = step_begin[i]
    step_volume[i] = (depth[stb+1]-depth[stb])/(depth[-1]-depth[0])
step_volume *= total_volume

#Step volume flow rate (of cuttings)
flow_rate = np.zeros(6)
for i in range(6):
    stb = step_begin[i]
    flow_rate[i] = step_volume[i]/(time[stb+1]-depth[stb])

#Convert to mass flow rate
mflow_rate = flow_rate*2011 #kg/s

#Read and convert particle data - size and fraction
# radius, mass_fraction = np.loadtxt('./particle_data.csv',
#                                    delimiter=',', skiprows=1, unpack=True)
radius, volume_fraction = np.loadtxt('./particle_data_Pivel.csv',
                                   delimiter=',', skiprows=1, unpack=True)

diameter = radius*2/100 #convert to meters

#Calculate "number flow" of cuttings - number of particles per second
number = np.zeros((len(step_begin),len(diameter)))
for i in range(len(step_begin)):
    for j in range(len(diameter)):
        # number[i,j] =  mflow_rate[i]*mass_fraction[j] #Use for mass fraction
        # number[i,j] /= (2011*np.pi/6*diameter[j]**3)
        number[i,j] =  flow_rate[i]*volume_fraction[j] #Use for volume fraction
        number[i,j] /= (np.pi/6*diameter[j]**3)

#Save data
# np.savetxt('./numbers.csv', np.concatenate((diameter.reshape(1,8),number)).T,
#            delimiter=',', comments='',
#            header='Diameter (m), Step 1, Step 2, Step 3, Step 4, Step 5, Step 6',)
np.savetxt('./numbers_Pivel.csv', np.concatenate((diameter.reshape(1,8),number)).T,
           delimiter=',', comments='',
           header='Diameter (m), Step 1 (np/s), Step 2 (np/s), Step 3 (np/s), Step 4 (np/s), Step 5 (np/s), Step 6 (np/s)',)

#Save mass flow rate for each step
np.savetxt('./mass_flow_rate.csv', np.concatenate(((np.arange(1,7,dtype='int16')).reshape(1,6),mflow_rate.reshape(1,6))).T,
           delimiter=',', comments='', fmt=['%i', '%f'],
           header='Step number,Mass flow rate',)
