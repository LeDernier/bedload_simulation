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
	show_figs = True
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
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"dirocc":r"Probability",
			"mtheta":r"$\theta (rad)$",
			"mphi":r"$\phi (rad)$",
			}
	# Plot params
	name_case = "ori"
	param = "pP.A"
	name_param = "A"

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Post Processing
	#-------------------#
	rot_i = "-1"
	#rot_i = "0"
	post_process = [
			{
			"dirocc":"data['dirs']["+rot_i+"][3]",
			"dirx":"data['dirs']["+rot_i+"][0]",
			"diry":"data['dirs']["+rot_i+"][1]",
			"dirz":"data['dirs']["+rot_i+"][2]",
			"mdirc":"data['mdirs']["+rot_i+"][3]",
			"mdirx":"data['mdirs']["+rot_i+"][0]",
			"mdiry":"data['mdirs']["+rot_i+"][1]",
			"mdirz":"data['mdirs']["+rot_i+"][2]",
			"z":"[z/d_ad for z in data['ori']["+rot_i+"][0]]",
			"mtheta":"data['ori']["+rot_i+"][1]",
			"vtheta":"[t/2.0 for t in data['ori']["+rot_i+"][2]]",
			"mphi":"data['ori']["+rot_i+"][3]",
			"vphi":"[p/2.0 for p in data['ori']["+rot_i+"][4]]",
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
			"mtheta":[[0.0, pi], []],
			"mphi":[[-pi/2.0, pi/2.0], []],
			}
	plots = {
			"mtheta":[["mtheta"], ["z"], ["vtheta", ""]],
			"mphi":[["mphi"], ["z"], ["vphi", ""]],
			}
	plotsT = {
			}
	plotsExtPath = {
			}
	plotsExt = {
			}
	alimsO = {
			"dirs":[[-0.5, 1.5], [-1.0, 1.0], [-1.0, 1.0]],
			"mdirs":[[-0.5, 1.5], [-1.0, 1.0], [-1.0, 1.0]],
			}
	orientations = {
			"dirs":[[["dirx", "diry", "dirz"]], ["dirocc"]],
			"mdirs":[[["mdirx","mdiry","mdirz"]], ["mdirc"]],
			}

class pP2D:
	plot_enable = False
	# Measuring 2D data in the 1D data
	measures = {
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
			}
