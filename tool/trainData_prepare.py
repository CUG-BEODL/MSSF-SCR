import os
import numpy as np
from osgeo import gdal, ogr

def extract_and_merge_patches(tif_path, shp_dir, aux_image_paths, output_path):
    """
    提取遥感影像和其它地球数据
    
    tif_path: 主影像文件路径
    shp_dir: 矢量文件目录路径
    aux_image_paths: 一维影像文件路径列表
    output_path: 输出.npy文件的保存路径
    """
    # 打开主影像文件
    main_raster_ds = gdal.Open(tif_path, gdal.GA_ReadOnly)
    gt = main_raster_ds.GetGeoTransform()
    num_main_bands = main_raster_ds.RasterCount

    # 准备辅助影像数据
    aux_datasets = [gdal.Open(path, gdal.GA_ReadOnly) for path in aux_image_paths]

    # 遍历shp目录中的所有shapefile
    for shp_file in os.listdir(shp_dir):
        if shp_file.endswith('.shp'):
            shp_path = os.path.join(shp_dir, shp_file)
            vector_ds = ogr.Open(shp_path)
            layer = vector_ds.GetLayer()
            feature = layer.GetNextFeature()
            geom = feature.GetGeometryRef()
            minx, maxx, miny, maxy = geom.GetEnvelope()
            xoff = int((minx - gt[0]) / gt[1])
            yoff = int((maxy - gt[3]) / gt[5])
            xcount = int((maxx - minx) / gt[1])
            ycount = int((maxy - miny) / abs(gt[5]))
            
            # 读取主影像数据
            main_data = np.zeros((num_main_bands, ycount, xcount), dtype=np.float32)
            for band in range(1, num_main_bands + 1):
                data = main_raster_ds.GetRasterBand(band).ReadAsArray(xoff, yoff, xcount, ycount)
                main_data[band-1, :, :] = data
            
            # 读取并添加辅助影像数据
            for i, aux_ds in enumerate(aux_datasets):
                aux_band = aux_ds.GetRasterBand(1)
                aux_data = aux_band.ReadAsArray(xoff, yoff, xcount, ycount)
                # 假设辅助影像也是单波段，直接扩展数组维度以匹配主数据
                aux_data_reshaped = aux_data.reshape(1, ycount, xcount)
                main_data = np.vstack((main_data, aux_data_reshaped))

            # 保存为.npy文件
            np.save(os.path.join(output_path, f"{os.path.splitext(shp_file)[0]}.npy"), main_data)

            # 关闭矢量数据集
            vector_ds = None

    # 关闭主影像数据集和辅助影像数据集
    main_raster_ds = None
    for ds in aux_data:
        ds = None

def geochemistry_data_prepare(tif_path, shp_dir, output_path):
    """
    提取地球化学数据
    
    tif_path: 主影像文件路径
    shp_dir: 矢量文件目录路径
    output_path: 输出.npy文件的保存路径
    """
    # 打开主影像文件
    main_raster_ds = gdal.Open(tif_path, gdal.GA_ReadOnly)
    gt = main_raster_ds.GetGeoTransform()
    num_main_bands = main_raster_ds.RasterCount

    # 遍历shp目录中的所有shapefile
    for shp_file in os.listdir(shp_dir):
        if shp_file.endswith('.shp'):
            shp_path = os.path.join(shp_dir, shp_file)
            vector_ds = ogr.Open(shp_path)
            layer = vector_ds.GetLayer()
            feature = layer.GetNextFeature()
            geom = feature.GetGeometryRef()
            minx, maxx, miny, maxy = geom.GetEnvelope()
            xoff = int((minx - gt[0]) / gt[1])
            yoff = int((maxy - gt[3]) / gt[5])
            xcount = int((maxx - minx) / gt[1])
            ycount = int((maxy - miny) / abs(gt[5]))
            
            # 读取主影像数据
            main_data = np.zeros((num_main_bands, ycount, xcount), dtype=np.float32)
            for band in range(1, num_main_bands + 1):
                data = main_raster_ds.GetRasterBand(band).ReadAsArray(xoff, yoff, xcount, ycount)
                main_data[band-1, :, :] = data

            # 保存为.npy文件
            np.save(os.path.join(output_path, f"{os.path.splitext(shp_file)[0]}.npy"), main_data)

            # 关闭矢量数据集
            vector_ds = None

    # 关闭主影像数据集
    main_raster_ds = None

if __name__ == '__main__':
    # 示例调用
    tif_path = 'xxx.tif'
    shp_dir = '/output_patches'
    aux_image_paths = ['ndvi.tif', 'DEM.tif', 'xxx.tif']
    output_path = './data'
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    extract_and_merge_patches(tif_path, shp_dir, aux_image_paths, output_path)
    print("Done data!")
    
    geochems = ['al2o3', 'fe2o3']
    
    geochem_path = "/geochemistry"
    output_path_geo = '/label'
    
    for item in geochems:
        data_path = os.path.join(geochem_path, item + '.tif')
        save_path = os.path.join(output_path_geo, item)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        geochemistry_data_prepare(data_path, shp_dir, save_path)
        print(f"Done {item}!")
    
    