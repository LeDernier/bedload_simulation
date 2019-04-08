execfile("params.py")

n_z = 400
begz = int(z_ground * n_z / h)
endz = begz+n_z/8
lastProfile = True

execfile("../common/post_proc.py")
