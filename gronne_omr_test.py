"""
Define new functions using @qgsfunction. feature and parent must always be the
last args. Use args=-1 to pass a list of values as arguments
"""

from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

@qgsfunction(args="auto", group='Custom')
def gronne_omr_areal_test(intersectLayerName, labelField, atlasGeom, feature, parent):
	
	"""
	Dette er en test Docstring
	"""
	
	#Parametre til beregning af estimeret timer (kvm/min pr. plejeniveau)
	blomster_tid = {'3': 0.1, '4': 0.1}
	belaegning_tid = {'2': 2.62, '3': 2.62, '4': 2.62}
	haek_tid = {'1': 0.3, '2': 0.3, '3': 0.3, '4': 0.3}
	buske_tid = {'1': 2.75, '2': 1.8, '3': 0.92}
	traegrupper_tid = {'1': 2.75, '2': 2.75, '3': 2.75}
	sol_traeer_tid = {'1': 0.11, '3': 0.11}
	hegn_tid = {'1': 3.04, '2': 3.04, '3': 3.04}
	klippet_tid = {'1': 13.89, '2': 5.56, '3': 4.17}
	slaaet_tid = {'1': 30.56, '2': 30.56, '3': 26.19, '4': 22.92}
	skraldespande_tid = {'3': 0.008}
	baenke_tid = {'2': 0.02, '3': 0.02}
	
	
	
	
	
	if (atlasGeom is None):
		return ''
		
	intersectLayer = QgsMapLayerRegistry.instance().mapLayersByName(intersectLayerName)[0]
	
	if intersectLayer is None:
		raise Exception("Layer " + intersectLayerName + " not found!")
		
	type = {}
	for ft in intersectLayer.getFeatures():
		intersectGeom = ft.geometry()
		if (intersectGeom is None):
			continue
		if intersectGeom.intersects(atlasGeom):
			if not ft[labelField] in type:
				type[ft[labelField]] = round(intersectGeom.area(),1)
			else:
				type[ft[labelField]] += round(intersectGeom.area(), 1)
			
	#typeText = ''
	#for key in type:
		#typeText += key +': ' + str(type[key]) + ' kvm\n'
	
	#return typeText
	
	html = ['<table style="border-collapse: collapse; font-size: 110%;" width=100%><tr><th>Type</th><th>Areal (kvm)</th></tr>']
	for key in type:
		html.append('<tr style="border: 1px solid #000">')
		html.append('<td style="border: 1px solid #000; padding-left: 5px;">{0}</td>'.format(key))
		html.append('<td style="border: 1px solid #000; padding-left: 5px;">{0}</td>'.format(type[key]))
		html.append('</tr>')
	html.append('</table>')
	return ''.join(html)
