import math

import pygeoj
from shapely.geometry import Polygon, LineString




class road:
    def __init__(self,properties= None,geometry=None):
        self.properties = properties
        self.geometry = geometry

    def isInside(self,bounding_box):
        poly = Polygon(bounding_box)
        return poly.contains(LineString(self.geometry))

    def measure_distance(self,point):
        ds = []
        for i in range(len(self.geometry)-1):
            x = point[0]
            y = point[1]
            x1 = self.geometry[i][0]
            y1 = self.geometry[i][1]
            x2 = self.geometry[i+1][0]
            y2 = self.geometry[i+1][0]
            A = x - x1;
            B = y - y1;
            C = x2 - x1;
            D = y2 - y1;

            dot = A * C + B * D;
            len_sq = C * C + D * D;
            param = -1;
            if (len_sq != 0):
                param = dot / len_sq;

            xx, yy = 0,0

            if (param < 0):
                xx = x1
                yy = y1
            elif (param > 1):
                xx = x2
                yy = y2
            else:
                xx = x1 + param * C
                yy = y1 + param * D


            dx = x - xx;
            dy = y - yy;
            ds.append(math.sqrt(dx * dx + dy * dy))
        return min(ds)

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



def readData(filename):
    with open(filename, "r") as f:
        all = f.read()
    all = all.split("\n")
    data = []

    for i in all[1:]:
        data.append([float(d) for d in i.split(",")])
    return data

def readStreetData(fname):
    rds = roads()
    rds.from_feature_file(fname)
    return rds


def getNearestStreets(path,rds):
    ds = []
    for i in rds:
        ds.append(i.measure_distance(path))
    print min(ds),ds.index(min(ds)),ds
    print rds[7].__dict__

def computeCorrelation(path,rds):
    pass




if __name__ == "__main__":
    fname_data = "/home/medzied/PycharmProjects/GisClusterer/Kalmanizer/data/fictional/raw.csv"
    data = readData(fname_data)

    fname_street = "/home/medzied/PycharmProjects/GisClusterer/Kalmanizer/data/fictional/street.geojson"
    rds = readStreetData(fname_street)
    print data[1]
    getNearestStreets(data[1],rds)



