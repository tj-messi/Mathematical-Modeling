import folium
import numpy as np

# 读取坐标数据的函数
def read_coordinates_from_txt(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            lat = float(parts[2])  # 纬度
            lon = float(parts[1])  # 经度
            coordinates.append((lat, lon))
    return coordinates

# 添加高斯扰动的函数
def add_gaussian_noise_to_path(path, noise_level=0.02):
    noisy_path = []
    for lat, lon in path:
        # 添加高斯噪声，生成新的经纬度
        noise_lat = lat + np.random.normal(0, noise_level)  # 噪声加入纬度
        noise_lon = lon + np.random.normal(0, noise_level)  # 噪声加入经度
        noisy_path.append((noise_lat, noise_lon))
    return noisy_path

# 路径文件路径（这里替换为实际路径）
file_path = r'D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\小组作业\traj\train\20111227015335.txt'  # 请用实际路径替换

# 读取原始轨迹数据
original_path = read_coordinates_from_txt(file_path)

# 生成扰动后的轨迹
noisy_path = add_gaussian_noise_to_path(original_path, noise_level=0.02)

# 创建一个基础地图，设置初始位置为原始轨迹的第一个点
m = folium.Map(location=original_path[0], zoom_start=15)

# 绘制原始轨迹（红色）
folium.PolyLine(original_path, color='red', weight=2.5, opacity=1).add_to(m)

# 绘制扰动后的轨迹（蓝色）
folium.PolyLine(noisy_path, color='blue', weight=2.5, opacity=1).add_to(m)

# 添加原始轨迹和扰动轨迹的离散坐标点标记
for idx, (lat, lon) in enumerate(original_path):
    folium.Marker([lat, lon], popup=f'Original Path - Point {idx+1}: ({lat}, {lon})', icon=folium.Icon(color='green')).add_to(m)

for idx, (lat, lon) in enumerate(noisy_path):
    folium.Marker([lat, lon], popup=f'Noisy Path - Point {idx+1}: ({lat}, {lon})', icon=folium.Icon(color='blue')).add_to(m)

# 添加起点标记
folium.Marker(location=original_path[0], popup="Start Point", icon=folium.Icon(color='green')).add_to(m)

# 保存地图为HTML文件
m.save('trajectory_map_with_noisy_path.html')

# 在Jupyter中显示地图（如果在Jupyter环境下）
m
