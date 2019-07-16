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
			"vfx":r"${U^f_x}^* = \frac{U^p_x}{\sqrt{(\rho_s/\rho_f - 1) g "+d_ad_name+"}}$",
			"mean_qsx":r"$\bar{Q_s}^*$",
			"qs":r"${Q_s}^*$",
			"qf":r"${Q_f}^*$",
			"shields":r"$\theta$",
			"sh":r"$\theta$",
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			"lt":r"$\lambda$",
			}
	# Plot params
	name_case = "valid-self"
	param = "pF.turbulence_model_type"
	name_param = "model"

# 1D plot parameters
class pP1D:
	plot_enable = False
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
			# Adimensionalisation
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
			}
	plots = {
			}
	plotsT = {
			}
	plotsExtPath = {
			}
	plotsExt = {
			}
	alimsO = {
			}
	orientations = {
			}

class pP2D:
	plot_enable = True
	# Measuring 2D data in the 1D data
	measures = {
			"qs":"average(data['qs'], data['time'])",
			"lt":"computeTransportLayerThickness(data['mean_qsx'], pF.dz)",
			#"qf":"average(data['qf'], data['time'])",
			"sh":"average(data['shields'], data['time'])",
			}
	post_process = [
			{
			},
			]
	add = [
			{
			#"sh":"bdata[bdata.keys()[0]]['sh']",
			#"theta3/2":"[s**(3.0/2.0) for s in badata['sh']]"
			},
			]
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
			"qs(sh)":[[], []],
			"lt(sh)":[[], []],
			}
	plots = {
			"lt(sh)":[["sh"], ["lt"]],
			"qs(sh)":[["sh"], ["qs"]],
			}
	loglogs = {
			"qs(sh)":[["sh"], ["qs"]],
			}
	plot_adds = {
			#"qs(sh)":[["sh"], ["theta3/2"], [r"$\theta^{\frac{3}{2}}$"]],
			}
	plotsExtPath = {
			}
	plotsExt = {
			}
	loglogsExt = {
			}
