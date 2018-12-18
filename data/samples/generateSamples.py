from src.gis.utils import road, roads, circlePoly

RAW = "/home/medzied/PycharmProjects/GisClusterer/data/raw/raw.geojson"
SAMPLE = "/home/medzied/PycharmProjects/GisClusterer/data/samples/sample.geojson"


import random

def comment(msg):
    print '[ INFO ] ' + msg
def read(fin):
    rds = roads()
    rds.from_feature_file(fin)
    return rds

# READ RAW
rds = read(RAW)
comment("Reading raw data")

# CREATE MACRO SAMPLES
rds = rds.crop([[10.0446,36.8732],[10.3090,36.8669],[10.3021,36.7040],[10.0506,36.7265],[10.0446,36.8732]])
comment("Cropping raw data")
rds.toGeoJSON("/home/medzied/PycharmProjects/GisClusterer/data/samples/sample.geojson")

# READ SAMPLE
rds = read(SAMPLE)
comment("Reading croped data")


randomPoints = 50

for i in range(randomPoints):
    center = rds.getCenter()
    cx1 = center[0] + random.randint(-1000,1000)*0.0001
    cy1 = center[1] + random.randint(-1000, 1000) * 0.0001

    poly = circlePoly([cx1,cy1], radius=1500, edges=24)
    rdss = rds.crop(poly)
    rdss.toGeoJSON("/home/medzied/PycharmProjects/GisClusterer/data/samples/s" + str(i) + ".geojson")


