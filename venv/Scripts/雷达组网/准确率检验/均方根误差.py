import cv2
import numpy as np

def calculate_rmse(image1, image2):
    # 确保两张图像尺寸一致，如果不一致，进行调整
    if image1.shape != image2.shape:
        # 调整第二张图像的尺寸与第一张图像一致
        image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

    # 将图像转换为灰度图像（如果是彩色图像）
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 计算均方根误差
    mse = np.mean((image1_gray - image2_gray) ** 2)
    rmse = np.sqrt(mse)
    return rmse

# 读取图像
image1 = cv2.imread(r'D:\test-data\radar-netting\radar\process-network\20240701\202407010020\CR_6.png')
image2 = cv2.imread(r'D:\test-data\radar-netting\radar\process-network\20240701\202407010050\CR.png')

# 计算RMSE
rmse = calculate_rmse(image1, image2)
print(f"RMSE between the images: {rmse}")
max_rmse = 255
similarity_percentage = (1 - rmse / max_rmse) * 100
print(f"Estimated structure similarity percentage: {similarity_percentage}%")



