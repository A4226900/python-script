import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import json

# 设置中文字体（比如使用 SimHei）
rcParams['font.family'] = 'SimHei'  # 黑体字体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 初始位置
a_pos = np.array([17.0, 117.0])  # A船初始位置
distance_to_a = 200  # B船距离A船的距离，单位：公里

# 根据地理距离计算B船初始的经纬度偏移
def calculate_offset(lat, distance_km, angle_deg):
    delta_lat = distance_km / 111  # 纬度上每度约111公里
    delta_lon = distance_km / (111 * np.cos(np.radians(lat)))  # 经度按纬度调整
    offset_lat = delta_lat * np.cos(np.radians(angle_deg))
    offset_lon = delta_lon * np.sin(np.radians(angle_deg))
    return np.array([offset_lat, offset_lon])

# B船相对A船的初始偏移（200公里，分别在正北、正东、正南、正西方向）
b_offsets = [
    calculate_offset(a_pos[0], distance_to_a, 0),    # B1 在A船北方
    calculate_offset(a_pos[0], distance_to_a, 90),   # B2 在A船东方
    calculate_offset(a_pos[0], distance_to_a, 180),  # B3 在A船南方
    calculate_offset(a_pos[0], distance_to_a, 270)   # B4 在A船西方
]

# 台湾位置（目标点）
taiwan_pos = np.array([22.5, 120.5])

# 航速（每小时速度为30节，6分钟每次前进约5.56公里）
speed = 30 * 1.852  # 速度：30节换算为公里/小时
time_interval = 6 / 60  # 时间间隔（6分钟）

# 计算每个船的位置，换算距离为合适的经纬度增量
def move_ship(pos, direction, speed, time_interval):
    distance = speed * time_interval  # 每次前进的距离（公里）

    # 纬度和经度变化
    delta_lat = distance / 111  # 纬度上每度约111公里
    delta_lon = distance / (111 * np.cos(np.radians(pos[0])))  # 经度按纬度调整

    # 归一化方向向量并更新位置
    norm_direction = direction / np.linalg.norm(direction)
    new_pos = pos + norm_direction * np.array([delta_lat, delta_lon])
    return new_pos

# 计算航向方向
def calculate_direction(start, end):
    return end - start

# 存储每个时间点的位置
a_positions = [a_pos]  # 初始化a_positions为一个包含a_pos的列表
b_positions = [[a_pos + offset] for offset in b_offsets]

# 台湾航向
direction_to_taiwan = calculate_direction(a_pos, taiwan_pos)

# 增加航向的弯曲：周期性的小扰动
amplitude = 3  # 扰动幅度
frequency = 0.1   # 扰动频率

# 模拟10小时的航行，每6分钟计算一个位置
hours = 10
steps = int(hours * 60 / 6)

# 模拟航行过程
for t in range(steps):
    # 引入航向的周期性变化，使航线有些弯曲
    angle_variation = amplitude * np.sin(frequency * t)
    direction_with_variation = direction_to_taiwan + np.array([angle_variation, 0])

    # A船位置更新
    a_pos = move_ship(a_pos, direction_with_variation, speed, time_interval)
    a_positions.append(a_pos)

    # B船位置更新
    for i in range(4):
        b_pos = move_ship(a_positions[-1] + b_offsets[i], direction_with_variation, speed, time_interval)
        b_positions[i].append(b_pos)

# 将a_positions转换为numpy数组
a_positions = np.array(a_positions)

# 绘制航线
plt.figure(figsize=(10, 8))

# 绘制A船的航线
plt.plot(a_positions[:, 1], a_positions[:, 0], label="A船航线", color="blue")

# 绘制B船的航线
colors = ['red', 'green', 'orange', 'purple']
for i in range(4):
    b_positions_i = np.array(b_positions[i])
    plt.plot(b_positions_i[:, 1], b_positions_i[:, 0], label=f"B{i+1}船航线", color=colors[i])

# 绘制台湾位置
plt.scatter(taiwan_pos[1], taiwan_pos[0], color='black', label="台湾")

# 设置图形标签和标题
plt.xlabel("经度")
plt.ylabel("纬度")
plt.title("A船和B船的弯曲航线图")
plt.legend()

# 显示图形
plt.grid(True)
plt.show()

# 输出A船的经纬度数组
print("A船经纬度路径：")
print(a_positions)

# 输出B1-B4船的经纬度数组
for i in range(4):
    print(f"B{i+1}船经纬度路径：")
    print(np.array(b_positions[i]))

# 保存航线数据到 JSON 文件
航线_data = {
    "A": a_positions.tolist(),
    "B1": np.array(b_positions[0]).tolist(),
    "B2": np.array(b_positions[1]).tolist(),
    "B3": np.array(b_positions[2]).tolist(),
    "B4": np.array(b_positions[3]).tolist()
}

# 保存为JSON文件
with open("航线.json", "w", encoding="utf-8") as f:
    json.dump(航线_data, f, ensure_ascii=False, indent=4)

print("航线数据已保存到 '航线.json' 文件。")


# 获取每条船的前10个点
a_positions_trimmed = a_positions[:50].tolist()
b_positions_trimmed = [np.array(b_pos)[:50].tolist() for b_pos in b_positions]

# 保存航线数据到 JSON 文件
航线前15个点_data = {
    "A": a_positions_trimmed,
    "B1": b_positions_trimmed[0],
    "B2": b_positions_trimmed[1],
    "B3": b_positions_trimmed[2],
    "B4": b_positions_trimmed[3]
}

# 保存为JSON文件
with open("航线前15个点.json", "w", encoding="utf-8") as f:
    json.dump(航线前15个点_data, f, ensure_ascii=False, indent=4)

print("航线数据（前15个点）已保存到 '航线.json' 文件。")