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
	me = 0.01 
	mew = 0.3
	ms = 5.0
	#-------------------#
	# Plot Names
	#-------------------#
	plots_names = {
			"mean_phi":r"$\bar{\phi}$",
			"mean_vx":r"$\bar{U^p_x}^* = \frac{\bar{U^p_x}}{\sqrt{(\rho_s/\rho_f - 1) g "+d_ad_name+"}}$",
			"vx":r"${U^p_x}^* = \frac{U^p_x}{\sqrt{(\rho_s/\rho_f - 1) g"+d_ad_name+"}}$",
			"mean_vfx":r"$\bar{U^f_x}^* = \frac{\bar{U^f_x}}{\sqrt{(\rho_s/\rho_f - 1) g "+d_ad_name+"}}$",
			"vfx":r"${U^f_x}^* = \frac{U^f_x}{\sqrt{(\rho_s/\rho_f - 1) g "+d_ad_name+"}}$",
			"mean_qsx":r"$\bar{Q_s}^*$",
			"qs":r"${Q_s}^*$",
			"qf":r"${Q_f}^*$",
			"shields":r"$\theta$",
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			"lm":r"${l_{m}}^* = \frac{l_{m}}{"+d_ad_name+"}$",
			#"lm":r"$l_{m} (m)$",
			"mean_lm":r"${\bar{l_{m}}}^* = \frac{\bar{l_{m}}}{"+d_ad_name+"}$",
			#"mean_lm":r"$\bar{l_{m}} (m)$",
			"ReS":r"$\tau'}$",
			"mean_ReS":r"$\bar{\tau'}$",
			}
	# Plot params
	name_case = "valid-self-A1-s0.4"
	param = "pF.turbulence_model_type"
	name_param = "model"

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Variable Utils
	#-------------------#
	z_av_min = "pM.hs*0.1"
	z_av_max = "pM.hs*0.4"
	#-------------------#
	# Post Processing
	#-------------------#
	post_process = [
			{
			# Adimentionalisation.
			"z":"[i * pF.dz/d_ad for i in range(pN.n_z)]",
			"vx":"[adim(l, sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['vx']]",
			"vfx":"[adim(l, sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['vfx']]",
			"lm":"[adim(l, d_ad) for l in data['lm']]",
			},
			{
			# Averaging.
			"mean_phi":"average_profile(data['phi'], data['time'])",
			"mean_vx":"ponderate_average_profile(data['phi'], data['vx'], data['time'])", 
			"mean_vfx":"average_profile(data['vfx'], data['time'])",
			"mean_lm":"average_profile(data['lm'], data['time'])",
			"mean_ReS":"average_profile(data['ReS'], data['time'])",
			},
			{
			# Flows
			"mean_qsx":"[data['mean_phi'][i] * data['mean_vx'][i] for i in range(len(data['mean_phi']))]",
			"qs":"[integration(data['phi'][i], data['vx'][i], pF.dz/d_ad) for i in range(len(data['time']))]",
			"qf":"[integration([1.0 - p for p in data['phi'][i]], data['vfx'][i], pF.dz/d_ad) for i in range(len(data['time']))]",
			"mean_z_phi":"[np.mean(data['phi'][i][int("+z_av_min+"/pF.dz):int("+z_av_max+"/pF.dz)]) for i in range(len(data['time']))]",
			"var_z_phi":"[sqrt(np.var(data['phi'][i][int("+z_av_min+"/pF.dz):int("+z_av_max+"/pF.dz)])) for i in range(len(data['time']))]",
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
			#"lm":[[0,0.004], [9,13]],
			"lm_phi":[[], [0.0, 1.0]],
			}
	plots = {
			"vx":[["mean_vx"], ["z"]],
			"qsx":[["mean_qsx"], ["z"]],
			"vfx":[["mean_vfx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			"qs":[["time"], ["qs"]],
			"qf":[["time"], ["qf"]],
			"sh":[["time"], ["shields"]],
			"lm":[["mean_lm"], ["z"]],
			"lm_phi":[["mean_phi"], ["mean_lm"]],
			"ReS":[["mean_ReS"], ["z"]],
			"mean_z_phi":[["time"], ["mean_z_phi"]],
			#"var_z_phi":[["time"], ["var_z_phi"]],
			}
	plotsT = {
#			"vx":[["vx"], ["z"], 20.0],
#			"vfx":[["vfx"], ["z"], 20.0],
			}
	plotsExtPath = {
			"Experimental data: 14,\nNi et al. 2014":"./capart-data/lm.csv"
			}
	plotsExt = {
			"lm_phi":[["phi"], ["lm"]],
			}
	alimsO = {
			}
	orientations = {
			}
	patchs = {
			#"qs":{"pos":"(pPP.mean_begin_time, -500)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"1000"},
			#"qf":{"pos":"(pPP.mean_begin_time, -500)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"1000"},
			#"mean_z_phi":{"pos":"(pPP.mean_begin_time, -500)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"1000"},
			#"var_z_phi":{"pos":"(pPP.mean_begin_time, -500)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"1000"},
			#"sh":{"pos":"(pPP.mean_begin_time, 0.0)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"1000"},
			#"phi":{"pos":"(-500, "+z_av_min+"/d_ad)", "w":"1000", "h":"("+z_av_max+"-"+z_av_min+")/d_ad"},
			#"vx":{"pos":"(-500, "+z_av_min+"/d_ad)", "w":"1000", "h":"("+z_av_max+"-"+z_av_min+")/d_ad"},
			#"qsx":{"pos":"(-500, "+z_av_min+"/d_ad)", "w":"1000", "h":"("+z_av_max+"-"+z_av_min+")/d_ad"},
			}

class pP2D:
	plot_enable = False
	# Measuring 2D data in the 1D data
	measures = {
			}
	post_process = []
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
			}
