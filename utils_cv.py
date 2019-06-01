import cv2
import numpy as np
import copy

'''
数据增强模块
'''


def augment(image_raw_data, flip=True, rotate=True, rate=0.5):
    assert 'filepath' in image_raw_data
    assert 'bboxes' in image_raw_data
    assert 'width' in image_raw_data
    assert 'height' in image_raw_data

    image_raw_data_copy = copy.deepcopy(image_raw_data)

    image = cv2.imread(image_raw_data_copy['filepath'])

    rows, cols = image.shape[:2]

    # 做增强的概率
    rate_bound = int(rate * 100)

    # flip翻转
    # cv2.flip: 1水平翻转， 0垂直翻转，-1水平垂直翻转
    if np.random.randint(100) < rate_bound and flip:
        image = cv2.flip(image, 1)
        for bbox in image_raw_data_copy['bboxes']:
            x1 = bbox['x1']
            x2 = bbox['x2']
            bbox['x2'] = cols - x1
            bbox['x1'] = cols - x2

    if np.random.randint(100) < rate_bound and flip:
        image = cv2.flip(image, 0)
        for bbox in image_raw_data_copy['bboxes']:
            y1 = bbox['y1']
            y2 = bbox['y2']
            bbox['y2'] = rows - y1
            bbox['y1'] = rows - y2

    # rotate旋转，度数以逆时针为正向
    # TODO 增加随机角度旋转功能
    if np.random.randint(100) < rate_bound and rotate:
        for bbox in image_raw_data_copy['bboxes']:
            x1 = bbox['x1']
            x2 = bbox['x2']
            y1 = bbox['y1']
            y2 = bbox['y2']
            angle = np.random.choice([90, 180, 270], 1)[0]
            if angle == 90:
                image = np.transpose(image, (1, 0, 2))
                image = cv2.flip(image, 0)
                bbox['x1'] = y1
                bbox['x2'] = y2
                bbox['y1'] = cols - x2
                bbox['y2'] = cols - x1
            elif angle == 180:
                image = cv2.flip(image, -1)
                bbox['x2'] = cols - x1
                bbox['x1'] = cols - x2
                bbox['y2'] = rows - y1
                bbox['y1'] = rows - y2
            elif angle == 270:
                image = np.transpose(image, (1, 0, 2))
                image = cv2.flip(image, 1)
                bbox['x1'] = rows - y2
                bbox['x2'] = rows - y1
                bbox['y1'] = x1
                bbox['y2'] = x2

    image_raw_data_copy['width'] = image.shape[1]
    image_raw_data_copy['height'] = image.shape[0]
    return image_raw_data_copy, image
