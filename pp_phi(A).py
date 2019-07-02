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
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			"A":r"$A$",
			}
	# Plot param
	name_case = "phi(A)"
	param = "pP.kind"
	name_param = ""

# 1D plot parameters
class pP1D:
	plot_enable = False
	#-------------------#
	# Post Processing
	#-------------------#
	post_process = [
			{
			# Exporting profiles
			"phi":"[l[1] for l in data['profiles']]",
			"mean_profiles":"average_phi_u_profile(data['profiles'], data['time'])",
			},
			{
			# Adimentionalisation.
			"z":"[z/d_ad for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			},
			{
			# Flows
			"mean_z_phi":"[np.mean(data['phi'][i][int(pM.hs/pF.dz*0.25):int(pM.hs/pF.dz*0.75)]) for i in range(len(data['profiles']))]",
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
			"mean_z_phi":"average(data['mean_z_phi'], data['time'])",
			"A":"average(data['A'], data['time'])",
			}
	post_process = [
			{
			"A_ext":"np.linspace(1.0, 3.0, 100)",
			},
			{
			"fit":"np.polynomial.polynomial.polyval(bdata[bval]['A_ext'], np.polynomial.polynomial.polyfit(bdata[bval]['A'], bdata[bval]['mean_z_phi'], 1))"
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
			"phi_max(A)":[[], []],
			}
	plots = {
			"phi_max(A)":[["A", "A_ext"], ["mean_z_phi", "fit"], ["simulations", "fit"]],
			}
