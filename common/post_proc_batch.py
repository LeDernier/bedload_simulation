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
batch_colors = []
grad = len(sys.argv) - 1
for i in range(grad):
	c = (i/float(grad))
	colors.append((r[0]*c+r[1]*(1-c), v[0]*c+v[1]*(1-c), b[0]*c+b[1]*(1-c)))
	batch_colors.append((r[0]*c+r[1]*(1-c), v[0]*c+v[1]*(1-c), b[0]*c+b[1]*(1-c)))
markers = ["$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
batch_markers = ["$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
#markers = ["$\mathbf{H}$", "$\mathbf{G}$", "$\mathbf{F}$", "$\mathbf{E}$", "$\mathbf{D}$", "$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$"]
me = 0.005 
mew = 0.3
ms = 7.0
d_ad = 0
save_fig_dir = pPP.save_fig_dir 

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
		"shields":[],
		"rots":[]
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
		data["rots"].append(getOrientationHist())
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
	profiles = []
	profilesT = data["profiles"]
	rots = []
	rotsT = data["rots"]
	# Averaging
	if pPP.mean_over_time_enable:
		i_deb = 0
		while time[i_deb] < pPP.mean_begin_time:
			i_deb += 1
		# Dealing with profiles
		profiles = [profilesT[i_deb][0][:], profilesT[i_deb][1][:], profilesT[i_deb][2][:], profilesT[i_deb][3][:]]
		i = i_deb + 1
		while i < n_time + 1 and time[i] < pPP.mean_end_time:
			for j in range(len(profiles)):
				for k in range(len(profiles[j])):
					profiles[j][k] += profilesT[i][j][k]
			i += 1
		profiles = [[z/(i - i_deb) for z in profiles[0]], [phi/(i - i_deb) for phi in profiles[1]], [vx/(i - i_deb) for vx in profiles[2]], [vxf/(i - i_deb) for vxf in profiles[3]]]
		# Dealing with rots
		rots = [rotsT[i_deb][0][:], rotsT[i_deb][1][:], rotsT[i_deb][2][:], rotsT[i_deb][3][:]]
		i = i_deb + 1
		while i < n_time + 1 and time[i] < pPP.mean_end_time:
			for j in range(len(rots)):
				for k in range(len(rots[j])):
					rots[j][k] += rotsT[i][j][k]
			i += 1
		rots = [[rot/(i - i_deb) for rot in rots[0]], [rot/(i - i_deb) for rot in rots[1]], [rot/(i - i_deb) for rot in rots[2]], [rot/(i - i_deb) for rot in rots[3]]]
	else :
		profiles = profilesT[n_time]
		rots = rotsT[n_time]
	
	d_eff = 0 
	i = 0
	roty = rots[2]
	for a in rots[0]:
		d = sin(a) * pS.d_tot + cos(a) * pS.d_max
		d_eff += roty[i] * d
		i += 1
	print("INFO : d_eff/d_max = ", d_eff/pS.d_max)

	
	z_star = [z/d_ad for z in profiles[0]]
	phi = profiles[1]
	vx = [vx/(sqrt(abs(pM.g[2] * d_ad))) for vx in profiles[2]]
	vxf = [vf/(sqrt(abs(pM.g[2] * d_ad))) for vf in profiles[3]]
	
	dz = z_star[1] - z_star[0]
	# Computation of qs
	qsT = []
	for i in range(n_time + 1):
		p = profilesT[i]
		tmp_phi = p[1]
		tmp_vx = p[2]
		qs = 0
		for j in range(len(z_star)):
			qs += tmp_phi[j] * tmp_vx[j] * dz 
		qsT.append(qs)
	# Computation of qf
	qfT = []
	for i in range(n_time + 1):
		p = profilesT[i]
		tmp_phi = p[1]
		tmp_vf = p[3]
		qf = 0
		for j in range(len(z_star)):
			qf += (1.0 - tmp_phi[j]) * tmp_vf[j] * dz
		qfT.append(qf)

	# Averaging
	qs_mean = 0
	qf_mean = 0
	sh_mean = 0
	if pPP.mean_over_time_enable:
		i_deb = 0
		while time[i_deb] < pPP.mean_begin_time:
			i_deb += 1
		i = i_deb
		while i < n_time + 1 and time[i] < pPP.mean_end_time:
			qs_mean += qsT[i]
			qf_mean += qfT[i]
			sh_mean += data["shields"][i]
			i += 1
		qs_mean /= (i - i_deb)
		qf_mean /= (i - i_deb)
		sh_mean /= (i - i_deb)
	else :
		qs_mean = qsT[n_time]
		qf_mean = qfT[n_time]
		sh_mean = data["shields"][n_time]

	### Storing 2D data
	batch_val = eval(pPP.batch_plot_param)
	if batch_val in batch_data:
		batch_data[batch_val]["qs"].append(qs_mean)
		batch_data[batch_val]["qf"].append(qf_mean)
		batch_data[batch_val]["sh"].append(sh_mean)
	else:
		batch_data[batch_val] = {
				"qs":[qs_mean],
				"qf":[qf_mean],
				"sh":[sh_mean]
				}
	
	if not pPP.batch_plot_enable:
		### Ploting figures
		print(sep + "Ploting data.")
		# Setting markeverys
		markevery = int(max(1.0, me * len(z_star)))
		markeveryH = int(max(1.0, me * len(rots[0])))
		markeveryT = int(max(1.0, me * len(time)))
		# Phi plot
		axs["phi"].plot(phi, z_star, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Vx plot
		axs["vx"].plot(vx, z_star, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Vxf plot
		axs["vxf"].plot(vxf, z_star, color=c, marker=m, markevery=markevery, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Rotx plot
		axs["rotx"].plot(rots[0], rots[1], color=c, marker=m, markevery=markeveryH, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Roty plot
		axs["roty"].plot(rots[0], rots[2], color=c, marker=m, markevery=markeveryH, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Rotz plot
		axs["rotz"].plot(rots[0], rots[3], color=c, marker=m, markevery=markeveryH, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Qs plot
		axs["qs"].plot(time, qsT, color=c, marker=m, markevery=markeveryT, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Qf plot
		axs["qf"].plot(time, qfT, color=c, marker=m, markevery=markeveryT, markerfacecolor=c, markeredgewidth=mew, markersize=ms, label=r"$"+name_param+"="+name_value+"$")
		# Shields plot
		axs["sh"].plot(time, data["shields"], color=c, marker=m, markevery=markeveryT, markeredgewidth=mew, markerfacecolor=c, markersize=ms, label=r"$"+name_param+"="+name_value+"$")

if not pPP.batch_plot_enable:
	### Creating figures
	figs = {}
	axs = {}
	# Phi profile
	figs["phi"] = plt.figure()
	axs["phi"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $\phi$ profile for different $" + name_param + "$.")
	plt.xlabel(r"$\phi$")
	plt.ylabel(r"$z/"+pPP.d_ad_name+"$")
	# Vx profile
	figs["vx"] = plt.figure()
	axs["vx"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final ${V^f_x}^*=\frac{V^p_x}{\sqrt{g"+pPP.d_ad_name+"}}$ profile for different $" + name_param + "$.")
	plt.xlabel(r"${V^p_x}^*$")
	plt.ylabel(r"$z/"+pPP.d_ad_name+"$")
	# Vxf profile
	figs["vxf"] = plt.figure()
	axs["vxf"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } evolution of the final ${V^f_x}^*=\frac{V^f_x}{\sqrt{g"+pPP.d_ad_name+"}}$ profile for different $" + name_param + "$.")
	plt.xlabel(r"${V^f_x}^*$")
	plt.ylabel(r"$z/"+pPP.d_ad_name+"$")
	# Rotx profile
	figs["rotx"] = plt.figure()
	axs["rotx"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $rot_x$ profile for different $" + name_param + "$.")
	plt.xlabel(r"$rot_x$")
	plt.ylabel(r"$P$")
	# Roty profile
	figs["roty"] = plt.figure()
	axs["roty"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $rot_y$ profile for different $" + name_param + "$.")
	plt.xlabel(r"$rot_y$")
	plt.ylabel(r"$P$")
	# Rotz profile
	figs["rotz"] = plt.figure()
	axs["rotz"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the final $rot_z$ profile for different $" + name_param + "$.")
	plt.xlabel(r"$rot_z$")
	plt.ylabel(r"$P$")
	# Qs over time
	figs["qs"] = plt.figure()
	axs["qs"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of $Q_s$ over time for different $" + name_param + "$.")
	plt.xlabel(r"t (s)")
	plt.ylabel("$Q^*_s$")
	# Qf over time
	figs["qf"] = plt.figure()
	axs["qf"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of $Q_f$ over time for different $" + name_param + "$.")
	plt.xlabel(r"t (s)")
	plt.ylabel("$Q^*_f$")
	# Shields over time
	figs["sh"] = plt.figure()
	axs["sh"] = plt.gca()
	plt.title(r"\textbf{" + name_case.capitalize() +  r" : } Evolution of $\theta$ over time for different $" + name_param + "$.")
	plt.xlabel(r"t (s)")
	plt.ylabel(r"$\theta$")

# Declaring batch data storage
batch_data = {}

# Processing 1D data
for dr in sys.argv[1:]:
	print(bigSep + dr)
	execfile(dr+"/params.py")
	d_ad = eval(pPP.d_ad)
	post_process(dr)

if pPP.batch_plot_enable:
	### Qs(shields)
	plt.figure()
	plt.title(r"\begin{center}"+
			r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the solid transport compared to the shields number \\ for different $" + pPP.batch_param_name + r"$."
			+r"\end{center}"
			)
	plt.xlabel(r"$\theta$")
	plt.ylabel(r"$Q_s$")
	# Plotting
	for key in batch_data:
		batch_m = batch_markers.pop()
		batch_c = batch_colors.pop()
		d = batch_data[key]
		markeveryS = int(max(1.0, me * len(d["sh"])))
		plt.plot(d["sh"], d["qs"], color=batch_c, marker=batch_m, markevery=markeveryS, markeredgewidth=mew, markerfacecolor=batch_c, markersize=ms, label=r"$"+pPP.batch_param_name+"="+str(key)+"$")
	plt.legend(fancybox=True, framealpha=0.5)
	if pPP.save_figs:
		plt.savefig(save_fig_dir+name_case+"_"+name_param+"_"+"qs(shields)"+".pdf")
	### Qs(Qf)
	plt.figure()
	plt.title(r"\begin{center}"+
			r"\textbf{" + name_case.capitalize() +  r" : } Evolution of the solid transport compared to the fluid flow \\ for different $" + pPP.batch_param_name + r"$."
			+r"\end{center}"
			)
	plt.xlabel(r"$\theta$")
	plt.ylabel(r"$Q_s$")
	# Plotting
	for key in batch_data:
		batch_m = batch_markers.pop()
		batch_c = batch_colors.pop()
		d = batch_data[key]
		markeveryS = int(max(1.0, me * len(d["qf"])))
		plt.plot(d["qf"], d["qs"], color=batch_c, marker=batch_m, markevery=markeveryS, markeredgewidth=mew, markerfacecolor=batch_c, markersize=ms, label=r"$"+pPP.batch_param_name+"="+str(key)+"$")
	plt.legend(fancybox=True, framealpha=0.5)
	if pPP.save_figs:
		plt.savefig(save_fig_dir+name_case+"_"+name_param+"_"+"qs(qf)"+".pdf")
else:
	#### Creating rectangular patch to show averaging
	if pPP.mean_over_time_enable:
		rect = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
		axs["qs"].add_patch(rect)
		rect2 = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
		axs["sh"].add_patch(rect2)
		rect3 = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
		axs["qf"].add_patch(rect3)
	
	## Adding legends
	for key in axs:
		axs[key].legend(fancybox=True, framealpha=0.5)

	## Converting xlabel with radian writing
	axs["rotx"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["rotx"].get_xticks()])
	axs["roty"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["roty"].get_xticks()])
	axs["rotz"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["rotz"].get_xticks()])
	
	### Saving figures
	if pPP.save_figs:
		for key in figs:
			figs[key].savefig(save_fig_dir+name_case+"_"+name_param+"_"+key+".pdf")

### Showing figures
plt.show()
