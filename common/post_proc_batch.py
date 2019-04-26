import os
import sys
import matplotlib.pyplot as plt

### Constants
bigSep = "======================="
sep = "---------------------- "

### import measures functions
execfile("common/measures.py")

def read_ids(dr):
	print(sep + "Reading ids.")
	f = open(dr + '/\.ids','r')
	ids=eval(f.read())
	f.close()
	return ids

def read_data(dr):
	print(sep + "Loading data.")
	time = []
	data = {
		"profiles":[],
		}
	for f in os.listdir("data"):
		print("Loading file: "+dr+"/data/" + f)
		O.load(dr+"/data/" + f)
		time.append(O.time)
		### Getting data here.
		# Add calls to measurements to add data 
		data["profiles"].append(getProfiles())
		### End
	return time, data

def sort_data(time, data):
	print(sep + "Sorting data.")
	for key in data:
		stime, data[key] = zip(*sorted(zip(time, data[key])))
	return stime, data

def post_process(dr):
	ids = read_ids(dr)
	time, data = read_data(dr)
	time, data = sort_data(time, data)

	# Useful constants
	n_time = len(time) - 1
	profiles = data["profiles"]
	z_star = [(z - pM.z_ground)/pP.d for z in profiles[0]]
	phi = profiles[1]
	vx = profiles[2]
	
	dz = profiles[0][0][1] - profiles[0][0][0]
	qsT = []
	for i in range(endT):
		p = profiles[i]
		tmp_phi = p[1]
		tmp_vx = p[2]
		qs = 0
		for j in range(len(zs)):
			qs += tmp_phi[j] * tmp_vx[j] * dz 
		qsT.append(qs)

	### Ploting figures
	print(sep + "Ploting data.")
	# Phi plot
	fig_phi.plot(phi, z_star, '->', label=dr)
	# Vx plot
	fig_vx.plot(vx, z_star, '->', label=dr)
	# Qs plot
	fig_qs.plot(time, qsT, '->', label=dr)

### Creating figures
# Phi profile
fig_phi = plt.figure()
plt.title(r"Evolution of the final \phi profile for different parameters.")
plt.xlabel(r"\phi")
plt.ylabel("z/d")
plt.legend()
# Vx profile
fig_vx = plt.figure()
plt.title(r"Evolution of the final V^p_x profile for different parameters.")
plt.xlabel(r"V^p_x")
plt.ylabel("z/d")
plt.legend()
# Qs over time
fig_qs = plt.figure()
plt.title(r"Evolution of Q_s over time for different parameters.")
plt.xlabel(r"V^p_x")
plt.ylabel("z/d")
plt.legend()

for dr in sys.argv[1:]:
	print(bigSep + dr)
	post_process(dr)

### Showing figures
plt.show()
