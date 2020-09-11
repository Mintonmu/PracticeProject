#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: 'AD'
@license: Apache Licence
@time: 2018/10/11 11:22
Describe：

"""
import csv
import time

import pandas as pd
import glob
import os
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt


## 面积
def judge_with_area(acc_array, threshold):
    # 先根据对应的方法进行判断
    # 是否满足阈值
    # 返回 true or false

    area = np.trapz(acc_array, list(range(len(acc_array))), dx=0.001)

    if area >= threshold:
        return True
    return False


## 方差
def judge_with_mv(acc_array, threshold):
    var = np.var(acc_array)
    if var >= threshold:
        return True
    return False


# 阈值
def judge_with_th(acc_array, threshold):
    sum_ = sum(acc_array)
    if sum_ >= threshold:
        return True
    return False


def save_sta(rows):
    with open(os.path.join(os.getcwd(), 'stat.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


dir = 'actionData-acc-6axis'


def identify():
    windows_witd = 90
    files_path = glob.glob(os.path.join(dir, '*.csv'))
    files_path.sort()
    stas = [['阈值', '方法', '动作', '识别个数', '耗时']]  # 统计数据， 插入csv
    ths = [[901, 910, 910, 910, 910],  # area的阈值
           [11.7, 3, 4.1, 4, 2.3],  # var的阈值
           [910, 910, 910, 910, 910]]  # th的阈值
    for idx, (name, func) in enumerate(zip(['area', 'var', 'th'], [judge_with_area, judge_with_mv, judge_with_th])):

        for file, th in zip(reversed(files_path), ths[idx]):
            s_time = time.time()
            cnt = 0  # 提取数量计数器
            dataMat = pd.read_csv(file,
                                  names=['d' + str(i) for i in range(0, 44)],
                                  low_memory=False)[1:].drop(['d0'], axis=1).astype("float64")

            d_len = len(dataMat)

            start = 0
            end = windows_witd
            all_action_windows = DataFrame()
            while True:
                if end > d_len:
                    break
                windows = dataMat[start:end]
                acc_array = np.array(windows['d43'])

                if func(acc_array, th):
                    # 从 acc_array 获取最大值的位置
                    max_idx = acc_array.argmax()

                    action_windows = windows[max_idx - 20:max_idx + 20]
                    if len(action_windows) == 40:
                        all_action_windows = all_action_windows.append(action_windows, ignore_index=True)
                        cnt += 1
                start += windows_witd // 2
                end += windows_witd // 2
                # print(windows)
            # print(all_action_windows)
            # 保存all_action_windows
            e_time = time.time()
            all_action_windows.to_csv(os.path.join(dir, 'proed', name + file.split('/')[1]))
            stas.append([th, name, file.split('/')[1], cnt, format(e_time - s_time, '0.2f')])

    save_sta(stas)


def draw():
    files_path = glob.glob(os.path.join(dir, '*.csv'))
    files_path.sort()

    in_ = glob.glob(os.path.join(dir, 'proed', '*.csv'))
    in_.sort()

    files_path.extend(in_)

    plt.rcParams['figure.figsize'] = (12.0, 6.0)

    for idx, file_name in enumerate(files_path):
        dataMat = pd.read_csv(file_name,
                              names=['d' + str(i) for i in range(0, 44)],
                              low_memory=False)[1:].drop(['d0'], axis=1).astype("float64")['d43'][:300]

        plt.subplot(4, 5, idx + 1)
        plt.plot(list(range(len(dataMat))), dataMat)
        plt.title(file_name.split('/')[-1])
        plt.xticks([])
        plt.yticks([])
    plt.show()


if __name__ == '__main__':
    identify()
    draw()
