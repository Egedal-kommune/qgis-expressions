"""
Define new functions using @qgsfunction. feature and parent must always be the
last args. Use args=-1 to pass a list of values as arguments
"""

from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

@qgsfunction(args='auto', group='Custom')
def groenne_omr_areal(groenne_omraader, label_field, geom_atlas, feature, parent):
	
	#Check if atlas geometry is empty
	if geom_atlas is None:
		return 'Der mangler en Atlas geometri'
		
	# Get groenne_omr layer
	lyr_groenne_omr =  QgsMapLayerRegistry.instance().mapLayersByName(groenne_omraader)[0]

	if lyr_groenne_omr is None:
		raise Exception("Layer not found: " + groenne_omraader)
		
	# Get features that overlap geom_atlas
	type = {}
	for feature in lyr_groenne_omr.getFeatures():
		lyr_groenne_omr_geom = feature.geometry()
		if lyr_groenne_omr_geom is None:
			continue
		if lyr_groenne_omr_geom.intersects(geom_atlas):
			if not feature[label_field] in type:
				type[feature[label_field]] = round(lyr_groenne_omr_geom.area(), 1)
			else:
				type[feature[label_field]] += round(lyr_groenne_omr_geom.area(), 1)
	
	# Create html table
	html = ['<table style="border-collapse: collapse; font-size: 110%;" width=100%><tr><th>Type</th><th>Areal (kvm)</th></tr>']
	for key in type:
		html.append('<tr style="border: 1px solid #000">')
		html.append('<td style="border: 1px solid #000; padding-left: 5px;">{0}</td>'.format(key))
		html.append('<td style="border: 1px solid #000; padding-left: 5px;">{0}</td>'.format(type[key]))
		html.append('</tr>')
	html.append('</table>')
	return ''.join(html)
