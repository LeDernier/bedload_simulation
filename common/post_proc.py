import os
import matplotlib.pyplot as plt

### Constants
sep = "---------------------- "

### import measures functions
execfile("../common/measures.py")

### Reading framework ids
print(sep + "Reading ids.")
f = open('.ids','r')
ids=eval(f.read())
f.close()

### Reading data
print(sep + "Loading data.")
time = []
#tetraPosZ = []
max_z = []
profiles = []
for f in os.listdir("data"):
	print("Loading file: data/" + f)
	O.load("data/" + f)
	time.append(O.time)
#	tetraPosZ.append(getObjPos(ids["tetra"])[2])
	max_z.append((getMaxZ()-pM.z_ground)/pP.d)
	profiles.append(getProfiles())

### Sorting data
print(sep + "Sorting data.")
#stime, tetraPosZ = zip(*sorted(zip(time, tetraPosZ)))
stime, max_z = zip(*sorted(zip(time, max_z)))
stime, profiles = zip(*sorted(zip(time, profiles)))

### Processing parameters from data :
profilesIt = []
it = int(math.ceil(len(stime) / nbProfiles) - 1)
for i in range(nbProfiles+1):
	profilesIt.append(i * it)

### Ploting data
print(sep + "Ploting data.")

## Plot tetra position
#plt.figure()
#plt.title(r"Evolution of the tetra's position $\frac{z}{d_tetra}$.")
#plt.xlabel("Time (s)")
#plt.ylabel("Position (m)")
#me = max(len(stime)/100,1)
#plt.plot(stime, [(z-z_ground)/d_tetra for z in tetraPosZ], '->', markevery=me, label="tetra") # markevery is just used to show less markers
#plt.plot(stime, max_z, '-<', markevery=me, label=r"max") # markevery is just used to show less markers
#plt.plot(stime, [0 for t in stime], '-o', markevery=me, label=r"ground") # markevery is just used to show less markers
#plt.legend()

## Plot v
plt.figure()
plt.title(r"Evolution of the $V_x$ profile over time.")
plt.xlabel(r"$V_x$ (.)")
plt.ylabel("z/d (m)")


for i in profilesIt: 
	p = profiles[i]
	zs = p[0]
	v_x = p[2]
	me = max(len(zs)/100,1)
	plt.plot(v_x, zs, '->', markevery=me, label="t="+str(stime[i])) # markevery is just used to show less markers
plt.legend()

## Plot phi
plt.figure()
plt.title(r"Evolution of the $\phi_x$ profile over time.")
plt.xlabel(r"$\phi_x$ (m/s)")
plt.ylabel("z/d (m)")

for i in profilesIt:
	p = profiles[i]
	zs = p[0]
	phi = p[1]
	me = max(len(zs)/100,1)
	plt.plot(phi, zs, '->', markevery=me, label="t="+str(stime[i])) # markevery is just used to show less markers
plt.legend()

## Plot 
plt.figure()
plt.title(r"Evolution of $Q_s$ over time.")
plt.xlabel(r"$Time$ (s)")
plt.ylabel(r"$Q_s$ ($m^2s^{-1}$)")

dz = profiles[0][0][1] - profiles[0][0][0]
qsT = []
for i in range(len(stime)):
	p = profiles[i]
	zs = p[0]
	phi = p[1]
	v_x = p[2]
	qs = 0
	for j in range(len(zs)):
		qs += phi[j] * v_x[j] * dz 
	qsT.append(qs)

me = max(len(zs)/100,1)
plt.plot(stime, qsT, '->', markevery=me) # markevery is just used to show less markers
plt.legend()

## Show all figures
plt.show()
