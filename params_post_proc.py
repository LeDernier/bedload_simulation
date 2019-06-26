#-------------------#
# Setting latex
#-------------------#
plt.rc('text', usetex=True)
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
	save_fig_dir = "/home/rmonthil/Documents/post_proc/"
	save_figs = True
	#-------------------#
	# Adimensionalisation
	#-------------------#
	d_ad = "pP.dvs"
	d_ad_name = "d_{vs}"
	#-------------------#
	# Mean operation 
	#-------------------#
	mean_begin_time = 200.0
	mean_end_time = 1000.0
	#-------------------#
	# Plot visuals
	#-------------------#
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	markers = ["$\mathbf{H}$", "$\mathbf{G}$", "$\mathbf{F}$", "$\mathbf{E}$", "$\mathbf{D}$", "$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
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
			"sh":r"$\theta$",
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			"A":r"$A = \frac{L}{S}$",
			"dvsL":r"$\frac{d_{vs}}{L}$",
			"dvsS":r"$\frac{d_{vs}}{S}$",
			}

# 1D plot parameters
class pP1D:
	plot_enable = False
	#-------------------#
	# Measures
	#-------------------#
	measures = {
			#"profiles":"getProfiles()",
			#"shields":"getShields()",
			#"rots":"getEulerHist()",
			"A":"pP.A",
			"dvsL":"pP.dvs/pP.L",
			"dvsS":"pP.dvs/pP.S",
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
			# Averaging
			#"mean_rots":"average_profile(data['rots'], data['time'], True)",
			},
			{
			# Adimentionalisation.
			},
			{
			# Flows
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
#			"vx":[[], [4, 18]],
#			"qsx":[[], [4, 18]],
#			"phi":[[], [4, 18]],
#			"qs":[[], []],
			}
	plots = {
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
			#"ori":[["mean_vx"], ["z"]],
			}

class pP2D:
	plot_enable = True
	# Plot param
	param = "pF.init_shields"
	param_name = r"\theta"
	# Measuring 2D data in the 1D data
	measures = {
			"A":"average(data['A'], data['time'])",
			"dvsS":"average(data['dvsS'], data['time'])",
			"dvsL":"average(data['dvsL'], data['time'])",
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
	alims = {
			"dvsS(A)":[[], []],
			"dvsL(A)":[[], []],
			}
	plots = {
			"dvsS(A)":[["A"], ["dvsS"]],
			"dvsL(A)":[["A"], ["dvsL"]],
			}
