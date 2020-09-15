import csv
import time
import pandas as pd

if __name__ == '__main__':
    file_path = '../data/qtw1.csv'

    df = pd.read_csv(file_path, header=None,
                     names=['level', 'parent_id', 'data_id', '评论ID', '抓取目录', '评论内容', '评论时间'])
    data = []
    max_col = -1

    for _, l1_row in df.iterrows():
        data_id = l1_row['data_id']
        l2 = df[df['parent_id'] == data_id]
        for _, l2_row in l2.iterrows():
            data_id = l2_row['data_id']
            l3 = df[df['parent_id'] == data_id]

            ll1 = [l1_row['抓取目录'], l1_row['评论ID'], l1_row['评论时间'], l1_row['评论内容']]
            ll1.extend([l2_row['评论ID'], l2_row['评论时间'], l2_row['评论内容']])
            for a, b, c in zip(l3['评论ID'].values, l3['评论时间'].values, l3['评论内容'].values):
                ll1.extend([a, b, c])
            if len(ll1) > max_col:
                max_col = len(ll1)
            data.append(ll1)

    with open('a.csv', 'w') as f:
        writer = csv.writer(f)
        max_col -= 7
        head = ['互评ID','互评时间','互评内容'] * (max_col//3)
        p_head = ['抓取目录', '评论ID', '评论时间', '评论内容', '回应ID', '回应时间', '回应内容']
        p_head.extend(head)
        writer.writerow(p_head)
        writer.writerows(data)