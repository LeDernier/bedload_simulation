import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm


#-------------------#
# Constants
#-------------------#
bigSep = "\n====================== "
sep = "---------------------- "

#-------------------#
# Variables
#-------------------#
d_ad = 0

#-------------------#
# Getting names
#-------------------#
name_list = sys.argv[1]
name_list = name_list.split("_")
name_case = name_list[0]
for s in name_list[1:-2]:
	name_case += "-" + s
if len(name_list) > 2:
	name_param = name_list[-2]
	name_value = name_list[-1]
else:
	name_param = ""
	name_value = ""

#-------------------#
# Defining utils
#-------------------#
def color_gradient(grad_nb, p):
	p.colors = []
	for i in range(grad_nb):
		c = (i/float(grad_nb))
		p.colors.append((p.r[0]*c+p.r[1]*(1-c), p.v[0]*c+p.v[1]*(1-c), p.b[0]*c+p.b[1]*(1-c)))

def average(qT, t):
	""" Average qT over time.

	Parameters:
	- qT : Contains the quantity. : List of floats.
	"""
	n_time = len(t) - 1
	# Finding the first value to take into account.
	i_deb = 0
	while i_deb < len(t) and t[i_deb] < pPP.mean_begin_time:
		i_deb += 1
	if i_deb > n_time - 1:
		print('WARNING average: End of simulation before start of averaging.')
		print('WARNING average: Taking only last profile.')
		i_deb = n_time - 1
	# Initialisation
	q = qT[i_deb]
	# Averaging
	i = i_deb + 1
	while i < n_time + 1 and t[i] < pPP.mean_end_time:
		q += qT[i]
		i += 1
	q /= (i - i_deb)
	return q

def average_phi_u_profile(qT, t):
	""" Average qT profiles over time.

	Parameters:
	- qT : Contains all the profiles. : List of lists.
	qT[k][0] corresponds to z.
	qT[k][1] corresponds to phi.
	qT[k][2] corresponds to vxPart.
	qT[k][3] corresponds to vxf.
	"""
	n_time = len(t) - 1
	# Finding the first value to take into account.
	i_deb = 0
	while i_deb < len(t) and t[i_deb] < pPP.mean_begin_time:
		i_deb += 1
	if i_deb > n_time - 1:
		print('WARNING average_profile: End of simulation before start of averaging.')
		print('WARNING average_profile: Taking only last profile.')
		i_deb = n_time - 1
	# Initialisation
	q = []
	q.append(qT[i_deb][0])
	q.append([0] * len(qT[i_deb][1]))
	q.append([0] * len(qT[i_deb][2]))
	q.append([0] * len(qT[i_deb][3]))
	# Averaging
	i = i_deb
	while i < n_time + 1 and t[i] < pPP.mean_end_time:
		for k in range(len(q[1])):
			q[1][k] += qT[i][1][k]
		for k in range(len(q[2])):
			q[2][k] += qT[i][1][k] * qT[i][2][k]
		for k in range(len(q[3])):
			q[3][k] += qT[i][3][k]
		i += 1
	
	q[1] = [v/(i - i_deb) for v in q[1]]
	for k in range(len(q[2])):
		if q[1][k] > 0:
			q[2][k] /= q[1][k]
	q[2] = [v/(i - i_deb) for v in q[2]]
	
	return q

def average_profile(qT, t, n=False):
	""" Average qT profiles over time.

	Parameters:
	- qT : Contains all the profiles. : List of lists.
	qT[k][0] should correspond to the abscissa.
	- n : Enable normalise (for histograms) : bool
	"""
	n_time = len(t) - 1
	# Finding the first value to take into account.
	i_deb = 0
	while i_deb < len(t) and t[i_deb] < pPP.mean_begin_time:
		i_deb += 1
	if i_deb > n_time - 1:
		print('WARNING average_profile: End of simulation before start of averaging.')
		print('WARNING average_profile: Taking only last profile.')
		i_deb = n_time - 1
	# Initialisation
	q = []
	for l in qT[i_deb]:
		q.append(l[:])
	# Averaging
	i = i_deb + 1
	while i < n_time + 1 and t[i] < pPP.mean_end_time:
		for j in range(1, len(q)):
			for k in range(len(q[j])):
				q[j][k] += qT[i][j][k]
		i += 1
	if n:
		for j in range(1, len(q)):
			summ = sum(q[j])
			q[j] = [v/summ for v in q[j]]
	else:
		for j in range(1, len(q)):
			q[j] = [v/(i - i_deb) for v in q[j]]
	return q

def adim(q, star):
	""" non-dimensionalize the quantitie q by star.

	Parameters:
	- q : list
	- star : float
	"""
	return [a/star for a in q]

def integration(phi, y, dx):
	""" Integrate y along x ponderate by phi.

	"""
	q = 0
	for j in range(len(y)):
		q += phi[j] * y[j] * dx 
	
	return q

#-------------------#
# Import measures functions
#-------------------#
execfile("params_post_proc.py")
color_gradient(len(sys.argv) + len(pP1D.plotsExtPath) - 1, pP1D)
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
	stime = []
	data = {}
	for key in pP1D.measures:
		data[key] = []
	for f in os.listdir(dr+"/data"):
		print("Loading file: "+dr+"/data/" + f)
		### Loading data.
		O.load(dr+"/data/" + f)
		### Getting time.
		stime.append(O.time)
		### Measure data.
		for key in pP1D.measures: 
			data[key].append(eval(pP1D.measures[key]))
	return stime, data

def sort_data(stime, data):
	print(sep + "Sorting data.")
	for key in data:
		sstime, data[key] = zip(*sorted(zip(stime, data[key])))
	return sstime, data

def post_process(dr):
	# Update name_value
	name_value = dr.split("_")[-1]

	ids = read_ids(dr)
	stime, data = read_data(dr)
	stime, data = sort_data(stime, data)
	# Adding time to data
	data["time"] = stime
	# Post Processing
	for p in pP1D.post_process:
		for key in p:
			data[key] = eval(p[key])
	
	### Storing 2D data
	if pP2D.plot_enable:
		batch_val = eval(pP2D.param)
		if not (batch_val in batch_data):
			batch_data[batch_val] = {}
			for key in pP2D.measures:
				batch_data[batch_val][key] = []
		for key in pP2D.measures:
			batch_data[batch_val][key].append(eval(pP2D.measures[key]))
	
	### Ploting 1D data
	if pP1D.plot_enable:
		m = pP1D.markers.pop()
		c = pP1D.colors.pop()
		### Ploting figures
		print(sep + "Ploting data.")
		# Plots
		for key in pP1D.plots:
			errx = None
			erry = None
			if len(pP1D.plots[key]) > 2:
				if pP1D.plots[key][2][0] != "":
					errx = data[pP1D.plots[key][2][0]]
				if pP1D.plots[key][2][1] != "":
					erry = data[pP1D.plots[key][2][1]]
			for x in pP1D.plots[key][0]:
				me = int(max(1.0, pP1D.me * len(data[x])))
				for y in pP1D.plots[key][1]:
					axs[key].errorbar(data[x], data[y], xerr=errx, yerr=erry, color=c, marker=m, markevery=me,
							markerfacecolor=c, markeredgewidth=pP1D.mew, 
							markersize=pP1D.ms, label=r"$"+name_param+"="+name_value+"$")
		# PlotsT
		for key in pP1D.plotsT:
			space = pP1D.plotsT[key][2]
			for i in range(len(data["time"])):
				for x in pP1D.plotsT[key][0]:
					me = int(max(1.0, pP1D.me * len(data[x])))
					for y in pP1D.plotsT[key][1]:
						if i < 1:
							axsT[key].plot([v+i*space for v in data[x][i]], data[y], color=c, marker=m, markevery=me,
									markerfacecolor=c, markeredgewidth=pP1D.mew/len(data["time"]), 
									markersize=pP1D.ms/len(data["time"]), label=r"$"+name_param+"="+name_value+"$")
						else:
							axsT[key].plot([v+i*space for v in data[x][i]], data[y], color=c, marker=m, markevery=me,
									markerfacecolor=c, markeredgewidth=pP1D.mew/len(data["time"]), 
									markersize=pP1D.ms/len(data["time"]))
		# Orientations
		for key in pP1D.orientations:
			for xyz in pP1D.orientations[key][0]:
				X = data[xyz[0]]
				Y = data[xyz[1]]
				Z = data[xyz[2]]
				for C_name in pP1D.orientations[key][1]:
					C = data[C_name]
					for i in range(len(X)):
						norm = min(Vector3(X[i], Y[i], Z[i]).norm(), 1.0)
						axsO[key].quiver3D(X[i], Y[i], Z[i], X[i], Y[i], Z[i], 
								colors=[(0, 0, 0, norm), (0, 0, 0, norm), (0, 0, 0, norm)], 
								linewidth=2.0, length=norm)
					tmp = axsO[key].scatter3D(X, Y, Z, c=C, s=[Vector3(X[j], Y[j], Z[j]).norm()*80.0 for j in range(len(C))], cmap="Greys")
					if C_name in pPP.plots_names:
						tmp = figsO[key].colorbar(tmp)
						tmp.ax.set_ylabel(pPP.plots_names[C_name])

def plot_external_data():
	for ext_key in pP1D.plotsExtPath:
		path = pP1D.plotsExtPath[ext_key]
		# Selecting marker and color
		m = pP1D.markers.pop()
		c = pP1D.colors.pop()
		# Getting data
		data = {}
		execfile(path)
		# Plots Ext
		for key in pP1D.plotsExt:
			for x in pP1D.plotsExt[key][0]:
				me = int(max(1.0, pP1D.me * len(data[x])))
				for y in pP1D.plotsExt[key][1]:
					axs[key].plot(data[x], data[y], color=c, marker=m, markevery=me,
							markerfacecolor=c, markeredgewidth=pP1D.mew, 
							markersize=pP1D.ms, label=ext_key)
#-------------------#
# Creating 1D Figures
#-------------------#
if pP1D.plot_enable:
	# Plots 
	figs = {}
	axs = {}
	for key in pP1D.plots:
		figs[key] = plt.figure()
		axs[key] = plt.gca()
		plt.xlabel(pPP.plots_names[pP1D.plots[key][0][0]])
		plt.ylabel(pPP.plots_names[pP1D.plots[key][1][0]])
	for key in pP1D.alims:
		if pP1D.alims[key][0]:
			axs[key].set_xlim(pP1D.alims[key][0][0], pP1D.alims[key][0][1])
		if pP1D.alims[key][1]:
			axs[key].set_ylim(pP1D.alims[key][1][0], pP1D.alims[key][1][1])
	# PlotsT
	figsT = {}
	axsT = {}
	for key in pP1D.plotsT:
		figsT[key] = plt.figure()
		axsT[key] = plt.gca()
		plt.xlabel(pPP.plots_names[pP1D.plotsT[key][0][0]])
		plt.ylabel(pPP.plots_names[pP1D.plotsT[key][1][0]])
	# Orientations
	figsO = {}
	axsO = {}
	for key in pP1D.orientations:
		figsO[key] = plt.figure()
		axsO[key] = plt.gca(projection='3d')
		axsO[key].set_aspect('equal', 'box')
		axsO[key].set_xlabel("$x$")
		axsO[key].set_ylabel("$y$")
		axsO[key].set_zlabel("$z$")
		axsO[key].set_xticklabels([])
		axsO[key].set_yticklabels([])
		axsO[key].set_zticklabels([])
		axsO[key].w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
		axsO[key].w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
		axsO[key].w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
	for key in pP1D.alimsO:
		if pP1D.alimsO[key][0]:
			axsO[key].set_xlim(pP1D.alimsO[key][0][0], pP1D.alimsO[key][0][1])
		if pP1D.alimsO[key][1]:
			axsO[key].set_ylim(pP1D.alimsO[key][1][0], pP1D.alimsO[key][1][1])
		if pP1D.alimsO[key][2]:
			axsO[key].set_zlim(pP1D.alimsO[key][2][0], pP1D.alimsO[key][2][1])

# Declaring batch data storage
batch_data = {}

#-------------------#
# Post Processing 1D
#-------------------#
for dr in sys.argv[1:]:
	print(bigSep + dr)
	os.chdir(dr)
	execfile("params.py")
	os.chdir("..")
	d_ad = eval(pPP.d_ad)
	post_process(dr)

#-------------------#
# Post Processing External
#-------------------#
plot_external_data()

#-------------------#
# Post Processing 2D
#-------------------#
if pP2D.plot_enable:
	### Sorting data
	params = []
	params_val = []
	for p, v in batch_data.items():
		params.append(p)
		params_val.append(v)
	params, params_val = zip(*sorted(zip(params, params_val)))
	for key in pP2D.plots:
		plt.figure()
		plt.xlabel(pPP.plots_names[pP2D.plots[key][0][0]])
		plt.ylabel(pPP.plots_names[pP2D.plots[key][1][0]])
		if pP2D.alims[key][0]:
			plt.xlim(pP2D.alims[key][0][0], pP2D.alims[key][0][1])
		if pP2D.alims[key][1]:
			plt.ylim(pP2D.alims[key][1][0], pP2D.alims[key][1][1])
		# Plotting
		batch_markers = pP2D.markers[:]
		color_gradient(len(params), pP2D)
		for i in range(len(params)):
			p = params[i]
			v = params_val[i]
			m = batch_markers.pop()
			c = pP2D.colors.pop()
			for x in pP2D.plots[key][0]:
				me = int(max(1.0, pP2D.me * len(v[x])))
				for y in pP2D.plots[key][1]:
					plt.plot(v[x], v[y], color=c, marker=m, markevery=me, markeredgewidth=pP2D.mew, markerfacecolor=c, markersize=pP2D.ms, label=r"$"+pP2D.param_name+"="+str(p)+"$")
					plt.legend(fancybox=True, framealpha=0.5, loc=0)
					if pPP.save_figs:
						plt.savefig(pPP.save_fig_dir+name_case+"_"+pP2D.param_name+"_"+key+".pdf", bbox_inches="tight")
	
	##### Creating rectangular patch to show averaging
	#if pPP.mean_over_time_enable:
	#	rect = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
	#	axs["qs"].add_patch(rect)
	#	rect2 = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
	#	axs["sh"].add_patch(rect2)
	#	rect3 = plt.Rectangle((pPP.mean_begin_time, 0.0), pPP.mean_end_time - pPP.mean_begin_time, 1000, facecolor='w', edgecolor='k', hatch='/', alpha=0.3)
	#	axs["qf"].add_patch(rect3)

if pP1D.plot_enable:
	## Adding legends
	for key in axs:
		axs[key].legend(fancybox=True, framealpha=0.5, loc=0)
	for key in axsT:
		axsT[key].legend(fancybox=True, framealpha=0.5, loc=0)

	### Converting xlabel with radian writing
	#axs["rotx"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["rotx"].get_xticks()])
	#axs["roty"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["roty"].get_xticks()])
	#axs["rotz"].set_xticklabels([r"$" + format(r/np.pi, ".2g")+ r"\pi$" for r in axs["rotz"].get_xticks()])
	
	### Saving figures
	if pPP.save_figs:
		for key in figs:
			figs[key].savefig(pPP.save_fig_dir+name_case+"_"+name_param+"_"+key+".pdf", bbox_inches="tight")
		for key in figsT:
			figsT[key].savefig(pPP.save_fig_dir+name_case+"_"+name_param+"_"+key+"T.pdf", bbox_inches="tight")
		for key in figsO:
			for i in range(4):
				axsO[key].view_init(i * 90.0 / 3.0, -90.0)
				figsO[key].savefig(pPP.save_fig_dir+name_case+"_"+name_param+"_"+key+str(i)+".pdf", bbox_inches="tight")

### Showing figures
if pPP.show_figs:
	plt.show()
