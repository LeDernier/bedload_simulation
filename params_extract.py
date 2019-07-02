#-------------------#
# Measures
#-------------------#
json_save = False
measures = {
		"profiles":"getProfiles()",
		"dirs":"getOrientationHist(5.0, 0.0)",
		"mdirs":"getVectorMeanOrientation()",
		"ori":"getOrientationProfiles(pF.dz*20, int(pN.n_z/20))",
		}
