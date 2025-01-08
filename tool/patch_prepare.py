import os
import csv
from osgeo import gdal, ogr, osr

def create_patches(csv_file, tif_file, patch_size_pixels, output_dir):
    # 读取CSV文件
    points = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x_p'])
            y = float(row['y_p'])
            points.append((x, y))
    
    # 读取TIF文件
    ds = gdal.Open(tif_file)
    transform = ds.GetGeoTransform()
    pixel_width = transform[1]
    pixel_height = abs(transform[5])  # 像素高度为负值，取绝对值
    
    # 计算patch的实际大小
    patch_width = patch_size_pixels * pixel_width
    patch_height = patch_size_pixels * pixel_height
    
    # 获取TIF文件的投影信息
    srs = osr.SpatialReference()
    srs.ImportFromWkt(ds.GetProjection())
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 计算patch的边界并写入单独的shapefile
    for i, (x, y) in enumerate(points, start=1):
        min_x = x - (patch_width / 2)
        max_x = x + (patch_width / 2)
        min_y = y - (patch_height / 2)
        max_y = y + (patch_height / 2)
        
        # 确保边界与TIF文件的像素对齐
        min_x = transform[0] + ((min_x - transform[0]) // pixel_width) * pixel_width
        max_x = transform[0] + ((max_x - transform[0]) // pixel_width) * pixel_width
        min_y = transform[3] + ((min_y - transform[3]) // pixel_height) * pixel_height
        max_y = transform[3] + ((max_y - transform[3]) // pixel_height) * pixel_height
        
        # 创建patch的多边形
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(min_x, min_y)
        ring.AddPoint(min_x, max_y)
        ring.AddPoint(max_x, max_y)
        ring.AddPoint(max_x, min_y)
        ring.AddPoint(min_x, min_y)
        
        polygon = ogr.Geometry(ogr.wkbPolygon)
        polygon.AddGeometry(ring)
        
        # 创建shapefile
        shp_filename = os.path.join(output_dir, f'patch_{i}.shp')
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.CreateDataSource(shp_filename)
        layer = ds.CreateLayer('', srs, ogr.wkbPolygon)
        layer.CreateField(ogr.FieldDefn('ID', ogr.OFTInteger))
        
        # 创建feature并写入shapefile
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(polygon)
        feature.SetField('ID', i)
        layer.CreateFeature(feature)
        
        # 清理
        feature = None
        ds = None

if __name__ == '__main__':
    points = "points.csv"
    input_tif = "ndvi.tif"  # 任意研究区tif use for get geotransform
    output_dir = "./output_patches"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    create_patches(points, input_tif, 50, output_dir)