
# Lav et temp_layer og tilføj det til lagliste
d_lyr = QgsVectorLayer('LineString?field=distance:float', 'stik', 'memory')
QgsProject.instance().addMapLayer(d_lyr)

# Definer dit punkt, linie og temp_layer
pkt = QgsProject.instance().mapLayersByName('nedlobsriste_kom_veje')[0]
linie = QgsProject.instance().mapLayersByName('vejkort_vejman')[0]
d_lyr = QgsProject.instance().mapLayersByName('stik')[0]

# Find dataprovider
prov = d_lyr.dataProvider()

# Lav en tom liste til at gemme de nye linier i
feats = []

# Loop over alle punkter
for p in pkt.getFeatures():
    # Find det nærmeste pkt på linien
    minDistPoint = min([l.geometry().closestSegmentWithContext(p.geometry().asPoint()) for l in linie.getFeatures()])[1]
    # Lav en ny QGIS feature, som skal gemme den nye geometry
    feat = QgsFeature()
    # Definer geometrien som en polylinie lavet fra de to punkter
    feat.setGeometry(QgsGeometry.fromPolyline([QgsPoint(p.geometry().asPoint()), QgsPoint(minDistPoint[0], minDistPoint[1])]))
    # tilføj længden i en attribut
    feat.setAttributes([feat.geometry().length()])
    # tilføj til den tomme liste
    feats.append(feat)

# tilføj de nye features fra feats listen til dataprovideren
prov.addFeatures(feats)
# Opdater dit temp_layer
d_lyr.updateExtents()
# Tegn laget om igen
d_lyr.triggerRepaint()