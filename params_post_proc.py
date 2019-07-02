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
			}
	# Plot params
	name_case = "shape"
	param = "pP.A"
	name_param = "A"

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Variable Utils
	#-------------------#
	z_av_min = "pM.hs*0.1"
	z_av_max = "pM.hs*0.5"
	#-------------------#
	# Post Processing
	#-------------------#
	post_process = [
			{
			# Exporting profiles
			"phi":"[l[1] for l in data['profiles']]",
			"vx":"[adim(l[2], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['profiles']]",
			"vfx":"[adim(l[3], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad)) for l in data['profiles']]",
			# Averaging
			"mean_profiles":"average_phi_u_profile(data['profiles'], data['time'])",
			},
			{
			# Adimentionalisation.
			"z":"[z/d_ad for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			"mean_vx":"adim(data['mean_profiles'][2], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad))", 
			"mean_vfx":"adim(data['mean_profiles'][3], sqrt((pP.rho/pF.rho - 1.0) * -pM.g[2] * d_ad))",
			},
			{
			# Flows
			"mean_qsx":"[data['mean_phi'][i] * data['mean_vx'][i] for i in range(len(data['mean_phi']))]",
			"qs":"[integration(data['phi'][i], data['vx'][i], pF.dz) for i in range(len(data['profiles']))]",
			"qf":"[integration([1.0 - p for p in data['phi'][i]], data['vfx'][i], pF.dz) for i in range(len(data['profiles']))]",
			"mean_z_phi":"[np.mean(data['phi'][i][int("+z_av_min+"/pF.dz):int("+z_av_max+"/pF.dz)]) for i in range(len(data['profiles']))]",
			"var_z_phi":"[sqrt(np.var(data['phi'][i][int("+z_av_min+"/pF.dz):int("+z_av_max+"/pF.dz)])) for i in range(len(data['profiles']))]",
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
			"vx":[["mean_vx"], ["z"]],
			"qsx":[["mean_qsx"], ["z"]],
			"vfx":[["mean_vfx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			"qs":[["time"], ["qs"]],
			"qf":[["time"], ["qf"]],
			"sh":[["time"], ["shields"]],
			"mean_z_phi":[["time"], ["mean_z_phi"]],
			"var_z_phi":[["time"], ["var_z_phi"]],
			}
	plotsT = {
#			"vx":[["vx"], ["z"], 20.0],
#			"vfx":[["vfx"], ["z"], 20.0],
			}
	plotsExtPath = {
			}
	plotsExt = {
			}
	alimsO = {
			}
	orientations = {
			}
	patchs = {
			"qs":{"pos":"(pPP.mean_begin_time, 0.0)", "w":"pPP.mean_end_time - pPP.mean_begin_time", "h":"10"},
			"phi":{"pos":"(0.0, "+z_av_min+"/d_ad)", "w":"1.0", "h":"("+z_av_max+"-"+z_av_min+")/d_ad"},
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
