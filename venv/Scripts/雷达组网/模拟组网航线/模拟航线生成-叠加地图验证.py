import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import rcParams

# 设置中文字体
rcParams['font.family'] = 'SimHei'
rcParams['axes.unicode_minus'] = False

# 初始位置和偏移量
a_pos = np.array([17.0, 117.0])
distance_to_a = 200  # 距离A船200公里

# 计算B船的初始经纬度偏移量
def calculate_offset(lat, distance_km, angle_deg):
    delta_lat = distance_km / 111  # 纬度上的偏移
    delta_lon = distance_km / (111 * np.cos(np.radians(lat)))  # 经度偏移
    offset_lat = delta_lat * np.cos(np.radians(angle_deg))
    offset_lon = delta_lon * np.sin(np.radians(angle_deg))
    return np.array([offset_lat, offset_lon])

b_offsets = [
    calculate_offset(a_pos[0], distance_to_a, 0),
    calculate_offset(a_pos[0], distance_to_a, 90),
    calculate_offset(a_pos[0], distance_to_a, 180),
    calculate_offset(a_pos[0], distance_to_a, 270)
]

taiwan_pos = np.array([22.5, 120.5])
speed = 30 * 1.852
time_interval = 6 / 60

def move_ship(pos, direction, speed, time_interval):
    distance = speed * time_interval
    delta_lat = distance / 111
    delta_lon = distance / (111 * np.cos(np.radians(pos[0])))
    norm_direction = direction / np.linalg.norm(direction)
    new_pos = pos + norm_direction * np.array([delta_lat, delta_lon])
    return new_pos

def calculate_direction(start, end):
    return end - start

a_positions = [a_pos]
b_positions = [[a_pos + offset] for offset in b_offsets]
direction_to_taiwan = calculate_direction(a_pos, taiwan_pos)
amplitude = 3
frequency = 0.1

# 模拟航行
hours = 10
steps = int(hours * 60 / 6)

for t in range(steps):
    angle_variation = amplitude * np.sin(frequency * t)
    direction_with_variation = direction_to_taiwan + np.array([angle_variation, 0])
    a_pos = move_ship(a_pos, direction_with_variation, speed, time_interval)
    a_positions.append(a_pos)

    for i in range(4):
        b_pos = move_ship(a_positions[-1] + b_offsets[i], direction_with_variation, speed, time_interval)
        b_positions[i].append(b_pos)

a_positions = np.array(a_positions)

# 绘制航线叠加地图
fig = plt.figure(figsize=(10, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([110, 125, 15, 25], crs=ccrs.PlateCarree())

# 添加地图特征
ax.add_feature(cfeature.LAND, color="lightgray")
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.gridlines(draw_labels=True)

# 绘制A船和B船航线
plt.plot(a_positions[:, 1], a_positions[:, 0], label="A船航线", color="blue", transform=ccrs.PlateCarree())
colors = ['red', 'green', 'orange', 'purple']
for i in range(4):
    b_positions_i = np.array(b_positions[i])
    plt.plot(b_positions_i[:, 1], b_positions_i[:, 0], label=f"B{i+1}船航线", color=colors[i], transform=ccrs.PlateCarree())

# 台湾位置
plt.scatter(taiwan_pos[1], taiwan_pos[0], color='black', label="台湾", transform=ccrs.PlateCarree())

# 设置标题和图例
plt.title("A船和B船的弯曲航线图叠加地图")
plt.legend()

plt.show()

# 输出经纬度数组
print("A船经纬度路径：")
print(a_positions)
for i in range(4):
    print(f"B{i+1}船经纬度路径：")
    print(np.array(b_positions[i]))
