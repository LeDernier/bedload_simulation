import os
import matplotlib.pyplot as plt

execfile("params.py")

### Constants
sep = "---------------------- "
n_z = 1000
begz = int(z_ground * n_z / h)
endz = begz+n_z/8

### import measures functions
execfile("../common_test/measures.py")

### Reading framework ids
print(sep + "Reading ids.")
f = open('.ids','r')
ids=eval(f.read())
f.close()

### Reading data
print(sep + "Loading data.")
time = []
tetraPosZ = []
max_z = []
profiles = []
for f in os.listdir("data"):
	print("Loading file: data/" + f)
	O.load("data/" + f)
	time.append(O.time)
	tetraPosZ.append(getObjPos(ids["tetra"])[2])
	max_z.append((getMaxZ()-z_ground)/d_tetra)
	profiles.append(getProfiles())

### Sorting data
print(sep + "Sorting data.")
stime, tetraPosZ = zip(*sorted(zip(time, tetraPosZ)))
stime, max_z = zip(*sorted(zip(time, max_z)))
stime, profiles = zip(*sorted(zip(time, profiles)))

### Ploting data
print(sep + "Ploting data.")

## Plot tetra position
plt.figure()
plt.title(r"Evolution of the tetra's position $\frac{z}{d_tetra}$.")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
me = max(len(stime)/100,1)
plt.plot(stime, [(z-z_ground)/d_tetra for z in tetraPosZ], '->', markevery=me, label="tetra") # markevery is just used to show less markers
plt.plot(stime, max_z, '-<', markevery=me, label=r"max") # markevery is just used to show less markers
plt.plot(stime, [0 for t in stime], '-o', markevery=me, label=r"ground") # markevery is just used to show less markers
plt.legend()
plt.show()

## Plot v
plt.figure()
plt.title(r"Evolution of the $V_x$ profile over time.")
plt.xlabel(r"$V_x$ (m/s)")
plt.ylabel("z/d (m)")

for i in range(begt, endt):
	p = profiles[i]
	zs = p[0]
	v_x = p[2]
	me = max(len(zs)/100,1)
	plt.plot(v_x[begz:endz], [(z-z_ground)/d for z in zs[begz:endz]], '->', markevery=me, label="t="+str(stime[i])) # markevery is just used to show less markers

plt.legend()
plt.show()

## Plot phi
plt.figure()
plt.title(r"Evolution of the $V_x$ profile over time.")
plt.xlabel(r"$V_x$ (m/s)")
plt.ylabel("z/d (m)")

for i in range(begt, endt):
	p = profiles[i]
	zs = p[0]
	phi = p[1]
	me = max(len(zs)/100,1)
	plt.plot(phi[begz:endz], [(z-z_ground)/d for z in zs[begz:endz]], '->', markevery=me, label="t="+str(stime[i])) # markevery is just used to show less markers

plt.legend()
plt.show()
