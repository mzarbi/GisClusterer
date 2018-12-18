from src.gis.utils import road, roads

RAW = "/home/medzied/PycharmProjects/GisClusterer/data/raw/raw.geojson"


def crop(fin, fout):
    rds = roads()
    rds.from_feature_file(RAW)
    for rd in rds:
        print rd.__dict__




