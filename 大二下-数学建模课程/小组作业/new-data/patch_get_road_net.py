import os
import pandas as pd
import shutil
import math

import pandas as pd
import geopandas as gpd
import osmnx as ox
from gotrackit.map.Net import Net
from gotrackit.MapMatch import MapMatch
from gotrackit.gps.Trajectory import TrajectoryPoints
import gotrackit.netreverse.NetGen as ng
import math
from gotrackit.tools.coord_trans import LngLatTransfer

def wgs84_to_gcj02_df(df, lon_col='lng', lat_col='lat'):
    """
    将 DataFrame 中的 WGS-84 坐标转换为 GCJ-02 坐标，使用 gotrackit 的 LngLatTransfer。
    :param df: 输入 DataFrame，包含经纬度列
    :param lon_col: 经度列名
    :param lat_col: 纬度列名
    :return: 转换后的 DataFrame
    """
    trans = LngLatTransfer()
    lons = df[lon_col].values
    lats = df[lat_col].values
    gcj_lons, gcj_lats = [], []
    for lon, lat in zip(lons, lats):
        if not pd.isna(lon) and not pd.isna(lat):
            gcj_lon, gcj_lat = trans.loc_convert(lng=lon, lat=lat, con_type='84-gc')
            gcj_lons.append(gcj_lon)
            gcj_lats.append(gcj_lat)
        else:
            gcj_lons.append(lon)
            gcj_lats.append(lat)
    df[lon_col] = gcj_lons
    df[lat_col] = gcj_lats
    return df

def get_utm_epsg(lon: float, lat: float) -> str:
    """
    根据经纬度计算 UTM 区域并返回对应的 EPSG 代码。
    :param lon: 经度（中心点）
    :param lat: 纬度（中心点）
    :return: EPSG 代码（如 'EPSG:32649'）
    """
    # 计算 UTM 区域编号
    zone_number = math.floor((lon + 180) / 6) + 1
    # 判断南北半球
    hemisphere = 'north' if lat >= 0 else 'south'
    # EPSG 代码：北部为 32600 + zone_number，南部为 32700 + zone_number
    epsg_code = f"EPSG:{32600 + zone_number if hemisphere == 'north' else 32700 + zone_number}"
    return epsg_code

def process_csv(csv_file_path, file_prefix,subfolder):
    """
    处理每个 CSV 文件，进行 UTM 区域推断、增密处理、网格生成等操作
    :param csv_file_path: 输入 CSV 文件路径
    :param file_prefix: 用作输出文件夹名的前缀
    """
    # 读取 GPS 数据
    gps_df = pd.read_csv(csv_file_path)
    
    # 将 WGS-84 坐标转换为 GCJ-02
    gps_df = wgs84_to_gcj02_df(gps_df, lon_col='lng', lat_col='lat')
    print("GPS 数据已转换为 GCJ-02:")

    # 提取经纬度范围
    min_lon, max_lon = gps_df['lng'].min(), gps_df['lng'].max()
    min_lat, max_lat = gps_df['lat'].min(), gps_df['lat'].max()
    
    # 计算中心点以推断 UTM 区域
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    # 获取 EPSG 代码
    epsg_code = get_utm_epsg(center_lon, center_lat)
    print(f"自动推断的 EPSG 代码: {epsg_code}")
    
    # 在对应的子文件夹中处理 GPS 数据
    output_subfolder = os.path.join(r'/media/tongji/Road-Net/data_preprocess_simplify/output-roadnet', file_prefix)
    if not os.path.exists(output_subfolder):
        os.makedirs(output_subfolder)
    
     # 下载路网数据
    output_dir = subfolder
    tp = TrajectoryPoints(gps_points_df=gps_df, plain_crs=epsg_code)
    # tp.dense(dense_interval=120)  # 由于样例数据是稀疏定位数据，我们在匹配前进行增密处理
    gps_df = tp.trajectory_data(_type='df')
    nv = ng.NetReverse(
        flag_name = 'test-angle',
        net_out_fldr = output_dir,
        plain_crs=epsg_code,
    )
    nv.generate_net_from_request(
        key_list=['cd00da8f838b4032acc4e2a2602eb3fd'],
        save_log_file=False,
        log_fldr='./',
        min_lng=min_lon , min_lat=min_lat,
        w=2000,h=1500,
        od_type='rand_od',od_num=300,gap_n=1000,min_od_length=1200,
    )

    link = gpd.read_file(os.path.join(subfolder,'FinalLink.shp'))
    node = gpd.read_file(os.path.join(subfolder,'FinalNode.shp'))
    my_net = Net(link_gdf=link, node_gdf=node, not_conn_cost=1200)
    my_net.init_net()  # net初始化
    
    # 构建匹配类并执行匹配
    mpm = MapMatch(net=my_net, gps_buffer=120, flag_name='general_sample', time_format='%Y-%m-%d %H:%M:%S',
                   use_heading_inf=True, omitted_l=6.0, export_html=True, del_dwell=False,
                   out_fldr=output_subfolder, dense_gps=False,
                   gps_radius=20.0)
    
    # 执行匹配
    match_res, warn_info, error_info = mpm.execute(gps_df=gps_df)
    match_res.to_csv(os.path.join(output_subfolder,'road_net.csv'),
                     encoding='utf_8_sig', index=False)

def process_files(source_directory,input_dir, output_dir):

    for filename in os.listdir(source_directory):
        if filename.endswith('.csv'):
            # 获取文件前缀（去掉文件扩展名）
            file_prefix = os.path.splitext(filename)[0]
            
            # 创建子文件夹
            subfolder = os.path.join(input_dir, file_prefix)
            if not os.path.exists(subfolder):
                os.makedirs(subfolder)
                     

            # 生成文件路径
            source_file = os.path.join(source_directory, filename)
            destination_file = os.path.join(subfolder, filename)
            
            # 复制文件到子文件夹
            shutil.move(source_file, destination_file)  # 使用 copy 而不是 move
            print(f"文件 {filename} 已复制到 {subfolder}")
            
            # 处理 CSV 文件
            process_csv(destination_file, file_prefix,subfolder)

if __name__ == '__main__':
    source_directory = r'/media/tongji/Road-Net/data_preprocess_simplify/test_masked_csv'
    input_directory = r'/media/tongji/Road-Net/data_preprocess_simplify/input-roadnet'  # 输入目录
    output_directory = r'/media/tongji/Road-Net/data_preprocess_simplify/output-roadnet'  # 输出目录

    # 处理目录中的所有文件
    process_files(source_directory,input_directory, output_directory)

