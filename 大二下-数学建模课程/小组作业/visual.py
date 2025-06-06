import folium
import os
from folium.plugins import MarkerCluster  # 导入MarkerCluster

# 读取txt文件，解析出经纬度
def read_coordinates_from_txt(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('MASK'):  # 跳过注释行
                continue
            parts = line.strip().split(',')
            lat = float(parts[2])  # 纬度
            lon = float(parts[1])  # 经度
            coordinates.append((lat, lon))
    return coordinates

# 文件夹路径，包含多个txt文件
directory = r'D:\Mathematical Modeling\Mathematical-Modeling\大二下-数学建模课程\小组作业\Final_fold\answer\final_result'

# 遍历目录中的每个txt文件
for idx, filename in enumerate(os.listdir(directory)):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        coordinates = read_coordinates_from_txt(file_path)
        
        # 创建一个初始地图，设置地图中心为第一个文件的第一个点的经纬度
        m = folium.Map(location=coordinates[0], zoom_start=15)

        # 定义不同的颜色
        colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink']

        # 为每个文件的数据添加标记，使用不同的颜色
        for i, (lat, lon) in enumerate(coordinates):
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,  # 设置标记的大小
                color=colors[idx % len(colors)],  # 颜色
                fill=True,
                fill_color=colors[idx % len(colors)],
                fill_opacity=0.6,  # 设置透明度
                popup=f'{filename} - Point {i+1}: ({lat}, {lon})'  # 显示文件名、点的编号及经纬度
            ).add_to(m)

        # 获取文件的前缀作为输出HTML文件名
        prefix = filename.split('.')[0]  # 提取文件名前缀
        html_filename = f'./part/{prefix}_trajectory_map.html'

        # 保存地图为HTML文件，名称与txt文件前缀一致
        m.save(html_filename)

        print(f'Saved {html_filename}')
