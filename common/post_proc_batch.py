import os
import sys
import matplotlib.pyplot as plt

### Constants
bigSep = "\n====================== "
sep = "---------------------- "
r = [0.0, 0.5]
v = [0.5, 0.0]
b = [0.5, 0.0]
colors = []
grad = len(sys.argv) - 1
for i in range(grad):
	c = (i/float(grad))
	colors.append((r[0]*c+r[1]*(1-c), v[0]*c+v[1]*(1-c), b[0]*c+b[1]*(1-c)))
markers = ["$\MVTwo$", "$\MVOne$", "$\MVZero$", "d", "*", "s", "v", "o"]
#markers = ["$\mathbf{H}$", "$\mathbf{G}$", "$\mathbf{F}$", "$\mathbf{E}$", "$\mathbf{D}$", "$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$"]
markevery = 5
mew = 0.3
ms = 7.0
d_ad = 0
save_fig_dir = "/home/rmonthil/Documents/post_proc/"

### Setting plt options
plt.rc('text', usetex=True)

### Getting names
name_list = sys.argv[1]
name_list = name_list.split("_")
name_case = name_list[0]
name_param = name_list[1] 
for n in name_list[2:-1]:
	name_param += "_{" + n + "}"
name_value = name_list[-1]

### import measures functions
execfile("params_post_proc.py")
execfile("common/simulationPyRunners.py")
execfile("common/measures.py")

def read_ids(dr):
	print(sep + "Reading ids.")
	f = open(dr + '/.ids','r')
	ids = eval(f.read())
	f.close()
	return ids

def read_data(dr):
	print(sep + "Loading data.")
	time = []
	data = {
		"profiles":[],
		"shields":[]
		}
	for f in os.listdir(dr+"/data"):
		print("Loading file: "+dr+"/data/" + f)
		O.load(dr+"/data/" + f)
		time.append(O.time)
		### Updating quantities in order to measure them after.
		pyRuns.updateQuantities()
		### Getting data here.
		# Add calls to measurements to add data 
		data["profiles"].append(getProfiles())
		data["shields"].append(pF.shields)
		### End
	return time, data

def sort_data(time, data):
	print(sep + "Sorting data.")
	for key in data:
		stime, data[key] = zip(*sorted(zip(time, data[key])))
	return stime, data

def post_process(dr):
	m = markers.pop()
	c = colors.pop()
	
	# Update name_value
	name_value = dr.split("_")[-1]

	ids = read_ids(dr)
	time, data = read_data(dr)
	time, data = sort_data(time, data)

	# Useful constants
	n_time = len(time) - 1
	profilesT = data["profiles"]
	if pPP.mean_over_time_enable:
		i_deb = 0
		while time[i_deb] < pPP.mean_begin_time:
			i_deb += 1
		profiles = [profilesT[i_deb][0][:], profilesT[i_deb][1][:], profilesT[i_deb][2][:]]
		i = i_deb + 1
		while i < n_time + 1 and time[i] < pPP.mean_end_time:
			for j in range(len(profiles)):
				for k in range(len(profiles[j])):
					profiles[j][k] += profilesT[i][j][k]
			i += 1
		profiles = [[z/(i - i_deb) for z in profiles[0]], [phi/(i - i_deb) for phi in profiles[1]], [vx/(i - i_deb) for vx in profiles[2]]]
	else :
		profiles = profilesT[n_time]
	
	z_star = [z/d_ad for z in profiles[0]]
	phi = profiles[1]
	vx = profiles[2]
	
	dz = z_star[1] - z_star[0]
	qsT = []
	for i in range(n_time + 1):
		p = profilesT[i]
		tmp_phi = p[1]
		tmp_vx = p[2]
		qs = 0
		for j in range(len(z_star)):
			qs += tmp_phi[j] * tmp_vx[j] * dz 
		qsT.append(qs)
	
	### Ploting figures
	print(sep + "Ploting data.")
	# Phi plot
	ax_phi.plot(phi, z_star, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
	# Vx plot
	ax_vx.plot(vx, z_star, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
	# Qs plot
	ax_qs.plot(time, qsT, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
	# Shields plot
	ax_sh.plot(time, data["shields"], color=c, marker=m, markevery=markevery, markeredgewidth=mew, markerfacecolor=c, markersize=ms, label=r"$"+name_param+"="+name_value+"$")

### Creating figures
# Phi profile
fig_phi = plt.figure()
ax_phi = plt.gca()
plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $\phi$ profile for different $" + name_param + "$.")
plt.xlabel(r"$\phi$")
plt.ylabel(r"$z/"+pPP.d_ad_type+"$")
# Vx profile
fig_vx = plt.figure()
ax_vx = plt.gca()
plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $V^p_x$ profile for different $" + name_param + "$.")
plt.xlabel(r"$V^p_x$")
plt.ylabel(r"$z/"+pPP.d_ad_type+"$")
# Qs over time
fig_qs = plt.figure()
ax_qs = plt.gca()
plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of $Q_s$ over time for different $" + name_param + "$.")
plt.xlabel(r"t (s)")
plt.ylabel("$Q_s$")
# Shields over time
fig_sh = plt.figure()
ax_sh = plt.gca()
plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of $\theta$ over time for different $" + name_param + "$.")
plt.xlabel(r"t (s)")
plt.ylabel(r"$\theta$")

for dr in sys.argv[1:]:
	print(bigSep + dr)
	execfile(dr+"/params.py")
	if pPP.d_ad_type == "d_min":
		d_ad = pS.d_min
		d_ad_type = r"d_{min}"
	elif pPP.d_ad_type == "d_max":
		d_ad = pS.d_max
		d_ad_type = r"d_{max}"
	elif pPP.d_ad_type == "d":
		d_ad = pP.d
	post_process(dr)

#### Creating rectangular patch to show averaging
if pPP.mean_over_time_enable:
	rect = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
	ax_qs.add_patch(rect)
	rect2 = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
	ax_sh.add_patch(rect2)

## Adding legends
ax_phi.legend()
ax_vx.legend()
ax_qs.legend()
ax_sh.legend()

### Saving figures
fig_phi.savefig(save_fig_dir+name_case+"_"+name_param+"_"+name_value+"_"+"phi.pdf")
fig_vx.savefig(save_fig_dir+name_case+"_"+name_param+"_"+name_value+"_"+"vx.pdf")
fig_qs.savefig(save_fig_dir+name_case+"_"+name_param+"_"+name_value+"_"+"qs.pdf")
fig_sh.savefig(save_fig_dir+name_case+"_"+name_param+"_"+name_value+"_"+"shields.pdf")

### Showing figures
plt.show()
