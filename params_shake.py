#-------------------#
# Setting latex
#-------------------#
#plt.rc('text', usetex=True)
#-------------------#
# Setting Font
#-------------------#
font = {'family' : 'normal',
#        'weight' : 'bold',
        'size'   : 18}
plt.rc('font', **font)

# Basic plot parameters
class pPP:
	#-------------------#
	# Plot Names
	#-------------------#
	show_figs = False
	#-------------------#
	# Saving figures
	#-------------------#
	save_fig_dir = "./post_proc/"
	save_figs = True
	#-------------------#
	# Adimensionalisation
	#-------------------#
	d_ad = "pP.dvs"
	d_ad_name = "d_{vs}"
	#-------------------#
	# Mean operation 
	#-------------------#
	mean_begin_time = 50.0
	mean_end_time = 300.0
	#-------------------#
	# Plot visuals
	#-------------------#
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	markers = ["$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
	me = 0.05 
	mew = 0.3
	ms = 7.0
	#-------------------#
	# Plot Names
	#-------------------#
	plots_names = {
			"mean_phi":r"$\bar{\phi}$",
			"mean_vx":r"$\bar{U^p_x}$",
			"vx":r"${U^p_x}^* = \frac{U^p_x}{\sqrt{(\rho_s/\rho_f - 1) g"+d_ad_name+"}}$",
			"mean_vfx":r"$\bar{U^f_x}^* = \frac{\bar{U^p_x}}{(\rho_s/\rho_f - 1) \sqrt{g"+d_ad_name+"}}$",
			"vfx":r"${U^f_x}^* = \frac{U^p_x}{(\rho_s/\rho_f - 1) \sqrt{g"+d_ad_name+"}}$",
			"mean_qsx":r"$\bar{Q_s}$",
			"qs":r"${Q_s}$",
			"qf":r"${Q_f}^*$",
			"shields":r"$\theta$",
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			}

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Measures
	#-------------------#
	measures = {
			"profiles":"getProfiles()",
			#"shields":"getShields()",
			#"rots":"getEulerHist()",
			}
	#-------------------#
	# Post Processing
	#-------------------#
	# Time is dealt seperately but data['time'] can be accessed from here.
	# Dictionaries are not sorted so it is an array of dictionaries.
	# An element of the array can use all the previous elements results. 
	post_process = [
			{
			# Exporting profiles
			"phi":"[l[1] for l in data['profiles']]",
			#"vx":"[adim(l[2], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['profiles']]",
			#"vfx":"[adim(l[3], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['profiles']]",
			# Averaging
			"mean_profiles":"average_phi_u_profile(data['profiles'], data['time'])",
			#"mean_rots":"average_profile(data['rots'], data['time'], True)",
			},
			{
			# Adimentionalisation.
			"z":"[z/d_ad for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			#"mean_vx":"adim(data['mean_profiles'][2], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad))", 
			#"mean_vfx":"adim(data['mean_profiles'][3], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad))",
			},
			{
			# Flows
			#"mean_qsx":"[data['mean_phi'][i] * data['mean_vx'][i] for i in range(len(data['mean_phi']))]",
			#"qs":"[integration(data['phi'][i], data['vx'][i], pF.dz) for i in range(len(data['profiles']))]",
			#"qf":"[integration([1.0 - p for p in data['phi'][i]], data['vfx'][i], pF.dz) for i in range(len(data['profiles']))]",
			"mean_z_phi":"[np.mean(data['phi'][i][int(pM.hs/pF.dz*0.25):int(pM.hs/pF.dz*0.75)]) for i in range(len(data['profiles']))]",
			"var_z_phi":"[sqrt(np.var(data['phi'][i][int(pM.hs/pF.dz*0.25):int(pM.hs/pF.dz*0.75)])) for i in range(len(data['profiles']))]",
			}
			]
	#-------------------#
	# Plot Visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	colors = []
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	alims = {
			"phi":[[], []],
			"mean_z_phi":[[], [0.4, 0.65]],
			"var_z_phi":[[], [0.0, 0.02]],
			}
	plots = {
			#"vx":[["mean_vx"], ["z"]],
			#"qsx":[["mean_qsx"], ["z"]],
			#"vfx":[["mean_vfx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			#"qs":[["time"], ["qs"]],
			#"qf":[["time"], ["qf"]],
			#"sh":[["time"], ["shields"]],
			"mean_z_phi":[["time"], ["mean_z_phi"]],
			"var_z_phi":[["time"], ["var_z_phi"]],
			}
	plotsT = {
#			"vx":[["vx"], ["z"], 20.0],
#			"vfx":[["vfx"], ["z"], 20.0],
			}
	plotsExtPath = {
#			"Numerical data,\nMaurin et al. 2016":"num-data/DATAr2d6s2_Maurinetal2016.py"
			}
	plotsExt = {
#			"vx":[["vx"], ["z"]],
#			"phi":[["phi"], ["z"]],
#			"qsx":[["qsx"], ["z"]],
			}

	alimsO = {
			
			}
	orientations = {
			"ori":[["mean_vx"], ["z"]],
			}

class pP2D:
	plot_enable = False
	# Plot param
	param = "pP.A"
	param_name = "A"
	# Measuring 2D data in the 1D data
	measures = {
			"qs":"average(data['qs'], data['time'])",
			"qf":"average(data['qf'], data['time'])",
			"sh":"average(data['shields'], data['time'])",
			}
	#-------------------#
	# Plot visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	colors = []
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	plots = {
			"qs(qf)":[["qf"], ["qs"]],
			"qs(sh)":[["sh"], ["qs"]],
			}
