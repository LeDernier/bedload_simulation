class pPP:
	# Saving figures
	save_fig_dir = "/home/rmonthil/Documents/post_proc/"
	save_figs = True
	# Adimensionalisation
	d_ad = "pow(pS.d_vol, 3.0)/pow(pS.d_surf, 2.0)"
	d_ad_name = "d_{vs}"
	# Mean operation 
	mean_over_time_enable = False
	mean_begin_time = 200.0
	mean_end_time = 400.0
	# 2D plot parameters
	batch_plot_enable = False
	batch_plot_param = "pS.A"
	batch_param_name = "A"
