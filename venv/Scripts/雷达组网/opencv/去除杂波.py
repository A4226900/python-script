import cv2
import numpy as np

# 加载带透明通道的彩色图像（四通道，BGRA）
image = cv2.imread(r'C:\Users\23059\Desktop\tmp\opencvTest\REF_0.png', cv2.IMREAD_UNCHANGED)

# 检查图像是否有 Alpha 通道
if image.shape[2] == 4:
    # 分离通道
    b_channel, g_channel, r_channel, alpha_channel = cv2.split(image)

    # 使用 alpha 通道来创建二值图像
    _, binary_alpha = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

    # 创建结构元素（内核），去除小的孤立像素块
    kernel = np.ones((5, 5), np.uint8)
    cleaned_alpha = cv2.morphologyEx(binary_alpha, cv2.MORPH_OPEN, kernel)

    # 将处理后的 alpha 通道与原始颜色通道合并
    cleaned_image = cv2.merge((b_channel, g_channel, r_channel, cleaned_alpha))

    # 保存为带透明背景的 PNG 图像
    output_path = r'C:\Users\23059\Desktop\tmp\opencvTest\before_quality_REF_0.png'
    success = cv2.imwrite(output_path, cleaned_image)

    if success:
        print("图像保存成功，带透明背景！")
    else:
        print("图像保存失败，请检查路径或文件夹权限。")
else:
    print("图像不包含 Alpha 通道，请检查输入图像格式。")
