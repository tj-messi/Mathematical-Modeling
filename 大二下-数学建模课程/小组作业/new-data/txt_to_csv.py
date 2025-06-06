import os
import csv

# 输入txt文件所在的目录
input_directory = "/media/tongji/Road-Net/data_preprocess_simplify/train"  # 请替换为实际的txt文件夹路径
output_directory = "/media/tongji/Road-Net/data_preprocess_simplify/train_csv"  # 请替换为你希望保存csv文件的目录

# 确保输出目录存在，如果不存在则创建
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 遍历目录中的所有txt文件
for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        txt_file_path = os.path.join(input_directory, filename)
        
        # 构建输出CSV文件的路径，前缀与txt文件名相同，扩展名为.csv
        csv_filename = os.path.splitext(filename)[0] + '.csv'
        csv_file_path = os.path.join(output_directory, csv_filename)
        
        # 打开输出CSV文件并写入表头
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # 写入CSV表头
            csv_writer.writerow(['agent_id', 'time', 'lng', 'lat'])
            
            # 读取txt文件并处理每一行
            with open(txt_file_path, mode='r', encoding='utf-8') as txtfile:
                for line in txtfile:
                    parts = line.strip().split(',')
                    if len(parts) == 3:  # 如果这一行格式正确
                        agent_id = "Car-1"
                        time = parts[0]
                        lng = parts[1]
                        lat = parts[2]
                        
                        # 将处理后的数据写入CSV
                        csv_writer.writerow([agent_id, time, lng, lat])

        print(f"{filename} 转换完成，保存为 {csv_filename}")

print("所有txt文件已转换为csv文件。")
