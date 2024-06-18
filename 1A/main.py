import numpy as np
import cv2


# 获取最小通道图像
def MinChannel(self):
    # 检查输入图像是否为三通道图像
    if len(self.shape) == 3 and self.shape[2] == 3:
        pass
    else:
        print("图像非三通道图像，无法处理！")
        return None

    # 创建单通道图像暂存最小像素
    img_single = np.zeros((self.shape[0], self.shape[1]), dtype=np.uint8)
    point_min = 255  # 初始化局部最小值为上限

    # 遍历图像的每个像素点，获取每个像素点的最小值
    for i in range(self.shape[0]):
        for j in range(self.shape[1]):
            point_min = min(self[i, j, :])
            img_single[i, j] = point_min

    return img_single


# 获取暗通道图像
def DarkChannel(self, block_size=5):
    # 检查输入图像是否为二维灰度图像
    if len(self.shape) == 2:
        pass
    else:
        print("图像非灰度图像，无法处理！") 
        return None
    
    # 检查块大小参数是否符合设定
    if block_size % 2 == 0 or block_size < 3:
        print("块大小参数不符合设定！")
        return None
    add_size = block_size // 2

    # 计算扩展后的图像尺寸
    new_height = self.shape[0] + block_size - 1
    new_width = self.shape[1] + block_size - 1

    # 使用边缘填充扩展图像
    img_expand = np.pad(self, ((add_size, add_size), (add_size, add_size)), 'edge')

    # 初始化暗通道图像
    img_dark = np.zeros((self.shape[0], self.shape[1]), dtype=np.uint8)

    # 遍历图像的每个像素点，获取指定块内最小值作为暗通道值
    for i in range(self.shape[0]):
        for j in range(self.shape[1]):
            point_min = np.min(img_expand[i:i + block_size, j:j + block_size])
            img_dark[i, j] = point_min

    return img_dark


# 获取图像大气光
class Channel(object):
    def __init__(self, x, y, value):
        self.x = x 
        self.y = y 
        self.value = value

def AtomsphericLight(dark, img):
    # 暗通道图像大小
    size = dark.size
    height, width = dark.shape

    # 创建列表并降序存储暗通道图像每点像素信息
    points = [Channel(i, j, dark[i, j]) for i in range(height) for j in range(width)]
    points.sort(key=lambda point: point.value, reverse=True)

    # 计算大气光值
    atomspheric_light = 0
    if int(0.001 * size) == 0:
        atomspheric_light = np.max(img[points[0].x, points[0].y])
        return atomspheric_light
    atomspheric_light = np.mean([img[node.x, node.y] for node in points[:int(0.001 * size)]])
    
    return int(atomspheric_light)


# 恢复场景光线【可调参数：omega、t0、block_size】
def Dehaze(img, omega=0.95, t0=0.1, block_size=13):
    img_min = MinChannel(img)  # 获取最小通道图像
    img_dark = DarkChannel(img_min, block_size=block_size)  # 获取暗通道图像
    atomspheric_light = AtomsphericLight(img_dark, img)  # 获取大气光

    # 计算透射率
    transmission = 1 - omega * img_dark / atomspheric_light
    transmission[transmission < t0] = t0  # 设置透射率下限
    
    # 初始化场景光线
    img_dehaze = np.zeros(img.shape)
    img = img.astype('float64')

    # 每个通道恢复场景光线
    for i in range(3):
        img_dehaze[:, :, i] = (img[:, :, i] - atomspheric_light) / transmission + atomspheric_light
        img_dehaze[:, :, i] = np.clip(img_dehaze[:, :, i], 0, 255)
    img_dehaze = img_dehaze.astype('uint8')

    
    '''
    # 可选展示过程性图像
    cv2.imwrite("process_img\\1_0_haze_img.png", img_haze)  # 原始雾霾图像
    cv2.imwrite("process_img\\1_1_min_img.png", img_min)  # 最小通道图像
    cv2.imwrite("process_img\\1_2_dark_img.png", img_dark)  # 暗通道图像
    cv2.imwrite("process_img\\1_3_dehaze_img.png", img_dehaze)  # 去雾图像
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    '''

    return img_dehaze


# 接口函数
def inputoutput():
    #'''
    for i in range(1, 10):
        inp = "strong_haze_data\\" + str(i) + "-test.png"
        img = cv2.imread(f'{inp}', cv2.IMREAD_COLOR)
        img_dehaze = Dehaze(img)
        cv2.imwrite("strong_haze_data\\" + str(i) + "-result.png", img_dehaze)
    #'''
    #'''
    for i in range(1, 10):
        inp = "middle_haze_data\\" + str(i) + "-test.bmp"
        img = cv2.imread(f'{inp}', cv2.IMREAD_COLOR)
        img_dehaze = Dehaze(img)
        cv2.imwrite("middle_haze_data\\" + str(i) + "-result.png", img_dehaze)
    #'''
    #'''
    for i in range(1, 10):
        inp = "weak_haze_data\\" + str(i) + "-test.png"
        img = cv2.imread(f'{inp}', cv2.IMREAD_COLOR)
        img_dehaze = Dehaze(img)
        cv2.imwrite("weak_haze_data\\" + str(i) + "-result.png", img_dehaze)
    #'''
    '''
    # test
    inp = "strong_haze_data\\2-test.png"
    img = cv2.imread(f'{inp}', cv2.IMREAD_COLOR)
    img_dehaze = Dehaze(img)
    cv2.imwrite("test-result.png", img_dehaze)
    '''


# 主函数
if __name__ == '__main__':
    inputoutput()