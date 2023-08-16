import geopandas as gpd

fp = "bestandsgebaeude_export.shp"
data = gpd.read_file(fp)
print(type(data))