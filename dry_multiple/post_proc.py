import matplotlib.pyplot as plt

execfile("params.py")

def parseVector3(s):
	vect = s.split("Vector3(")[1].split(")")[0].split("\n")[0].split(",")
	for i in range(3):
		vect[i] = float(vect[i])
	return vect

plt.figure()
plt.title(r"Evolution of the tetra's position $\frac{z}{d_tetra}$. Comparison for different particles length.")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")

ds = [1.0*d_tetra, 1.5*d_tetra, 2.0*d_tetra, 4.0*d_tetra, 8.0*d_tetra]

for i in range(len(ds)):
	d = ds[i]
	m = i % 12

	time = []
	with open("data/"+str(d)+"_"+"time.dat","r") as f:
		for line in f:
			time.append(float(line))
	
	meanVelX = []
	with open("data/"+str(d)+"_"+"mean_vel.dat","r") as f:
		for line in f:
			vect = parseVector3(line)
			meanVelX.append(vect[0])
	
	tetraPosZ = []
	with open("data/"+str(d)+"_"+"tetra_pos.dat","r") as f:
		for line in f:
			vect = parseVector3(line)
			tetraPosZ.append(vect[2])
	
	maxPosZ = []
	with open("data/"+str(d)+"_"+"max_z.dat", "r") as f:
		for line in f:
			maxPosZ.append(float(line))
	
	plt.plot(time, [z/d_tetra for z in tetraPosZ], '-o', markevery=100, label=r"$\frac{d}{d_{tetra}}$ = "+str(d/d_tetra)) # markevery is just used to show less markers

plt.legend()
plt.show()
