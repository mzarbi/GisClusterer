import json

import geog
import pygeoj
import shapely
from shapely.geometry import Polygon, LineString
import numpy as np

class road:
    def __init__(self,properties= None,geometry=None):
        self.properties = properties
        self.geometry = geometry

    def isInside(self,bounding_box):
        poly = Polygon(bounding_box)
        return poly.contains(LineString(self.geometry))

    def getCenter(self):
        xs,ys = [],[]
        for i in self.geometry:
            xs.append(i[0])
            ys.append(i[1])
        return [sum(xs)/len(xs), sum(ys)/len(ys)]
class roads(list):
    def __init__(self):
        list.__init__(self)

    def from_feature_file(self,fin):
        huge_map = pygeoj.load(filepath=fin)
        for feature in huge_map:
            tmp = road(feature.properties,feature.geometry.coordinates)
            self.append(tmp)

    def getCenter(self):
        c_array = []
        for rd in self:
            c_array.append(rd.getCenter())
        xs, ys = [], []
        for i in c_array:
            xs.append(i[0])
            ys.append(i[1])
        v = [0,0]
        try:
            v = [sum(xs) / len(xs), sum(ys) / len(ys)]
        except:
            pass
        return v

    def crop(self,bounding_box):
        tmp = roads()
        for rd in self:
            if rd.isInside(bounding_box):
                tmp.append(rd)
        return tmp

    def toGeoJSON(self,fout):
        geos = []
        for rd in self:
            poly = {"type": "Feature",
                    "properties": {},
                    "geometry":
                        {"type": "LineString","coordinates": rd.geometry}}
            geos.append(poly)

        geometries = {
            "type": "FeatureCollection",
            "features": geos,
        }

        geo_str = json.dumps(geometries)
        with open(fout,'w') as f:
            f.write(geo_str)


def circlePoly(center, radius=1500, edges=24):
    p = shapely.geometry.Point(center)
    angles = np.linspace(0, 360, edges)
    polygon = geog.propagate(shapely.geometry.Point(center), angles, radius)
    pl = []
    for i in polygon:
        pl.append([i[0],i[1]])
    pl.append(polygon[0])
    return pl
    #print(json.dumps(shapely.geometry.mapping(shapely.geometry.Polygon(polygon))))



#print circlePoly([-90.0667, 29.9500])
