import geopandas as gpd

# 读取edges.shp文件
edges = gpd.read_file(r"D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\小组作业\road_net\network-new\edges.shp")

# 查看数据结构
print(edges.head())
print(f"边数量: {len(edges)}")

# 如果需要转换为networkx图对象
import osmnx as ox
G = ox.graph_from_gdfs(None, edges)  # 第一个参数是nodes（可以为None）