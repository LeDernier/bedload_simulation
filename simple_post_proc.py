#!/usr/bin/python

#-------------------#
# Import
#-------------------#
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

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
	# Color gradient 
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	# Marker characteristics 
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
			"z":r"$z^* =  \frac{z}{"+d_ad_name+"}$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			}

def color_gradient(grad_nb):
	pPP.colors = []
	for i in range(grad_nb):
		c = (i/float(grad_nb))
		pPP.colors.append((pPP.r[0]*c+pPP.r[1]*(1-c), pPP.v[0]*c+pPP.v[1]*(1-c), pPP.b[0]*c+pPP.b[1]*(1-c)))


#-------------------#
# Data
#-------------------#

m_A =       np.array([1.0,   1.4,   1.8,   2.2,   2.6,   3.0])
m_alpha =   np.array([0.375, 0.445, 0.545, 0.595, 0.595, 0.595])
m_mu =      np.tan(m_alpha)
alpha_A = poly.Polynomial(poly.polyfit(m_A, m_alpha, 3))
mu_A = poly.Polynomial(poly.polyfit(m_A, m_mu, 3))

#-------------------#
# Plot
#-------------------#
color_gradient(1)

fig = plt.figure()
ax = plt.gca()
plt.xlabel("A")
plt.ylabel(r"$\alpha$")
x = m_A
y = m_alpha
m = pPP.markers.pop()
c = pPP.colors.pop()
me = int(max(1.0, pPP.me * len(x)))
ax.errorbar(x, y, yerr=0.005, color=c, marker=m, markevery=me, markerfacecolor=c, markeredgewidth=pPP.mew, markersize=pPP.ms)

#-------------------#
# Save
#-------------------#

if pPP.save_figs:
	fig.savefig(pPP.save_fig_dir+"alpha(A)"+".pdf", bbox_inches="tight")

#-------------------#
# Plot
#-------------------#
color_gradient(1)

fig = plt.figure()
ax = plt.gca()
plt.xlabel("A")
plt.ylabel(r"$\mu$")
x = m_A
y = m_mu
m = pPP.markers.pop()
c = pPP.colors.pop()
me = int(max(1.0, pPP.me * len(x)))
ax.errorbar(x, y, yerr=np.tan(0.005), color=c, marker=m, markevery=me, markerfacecolor=c, markeredgewidth=pPP.mew, markersize=pPP.ms)

#-------------------#
# Save
#-------------------#

if pPP.save_figs:
	fig.savefig(pPP.save_fig_dir+"mu(A)"+".pdf", bbox_inches="tight")

#-------------------#
# Show
#-------------------#

if pPP.show_figs:
	plt.show()
