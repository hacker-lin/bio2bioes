from itertools import starmap
from copy import deepcopy
from pprint import pprint

class DataDeal:
    def __init__(self, filename):
        self.filename = filename

    def reform_data(self):
        data_list = []
        label_list = []

        temp_list_data = []
        temp_list_label = []

        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                # pprint.pprint(line.strip())
                if line.strip():
                    data, label = line.strip().split()
                    temp_list_data.append(data)
                    temp_list_label.append(label)
                else:  # 注意，windows某情况可能会显示少量或多量空格，可以按需调整，无文件后缀2空行
                    data_list.append(temp_list_data)
                    label_list.append(temp_list_label)
                    temp_list_data = []
                    temp_list_label = []

        return data_list, label_list

    def dict_or_list(self, data_list, label_list, type='list'):
        assert type in ['dict', 'list'], 'the type arg must type str for "dict" or "list"'

        label_list = deepcopy(label_list)
        a = map(self.bio_2_bioes, label_list)  # 这里直接将value的BIO转化为BIOES，免的一会还得取出value再封装。

        seq_data_label = list(zip(data_list, a))  # ( [[句子1],[标签集1]], [[句子2],[标签集2]] )

        if type == 'dict':  # 字典不要用（统计可能会key重复，自动合并后少字，所以bioes会错乱，dict只是用来分词）
            return list(starmap(lambda x, y: dict(zip(x, y)), seq_data_label))
        elif type == 'list':  # 默认为 list
            return list(starmap(lambda x, y: list(zip(x, y)), seq_data_label))

    def bio_2_bioes(self, all_tag_lists):
        seq_len = len(all_tag_lists)

        for index, label in enumerate(all_tag_lists[:]):
            # 有两种情况抛异常（个人喜欢用 try 代替 if）
            #   1: 为O无法分割
            #   2: 最后一位越界【即使越界了，结合下面第二个try的里面的if，我们把它设为O，个人思想。也可用其他办法】
            try:
                next_tag = all_tag_lists[index + 1].split('-')[0]
            except:
                next_tag = 'O'

            try:
                current_tag, = label.split('-')[0]
                if index < seq_len:
                    if (current_tag == 'B' and next_tag != 'I'):  # B之后无I, 改成S
                        all_tag_lists[index] = 'S' + '-' + label.split('-')[-1]
                    elif (current_tag == 'I' and next_tag != 'I'):  # I之后无I, I改成E
                        all_tag_lists[index] = 'E' + '-' + label.split('-')[-1]
            except:
                pass

        return all_tag_lists


dd = DataDeal('bio')
data_list, label_list = dd.reform_data()
bioes_data_label = dd.dict_or_list(data_list, label_list, type='list')

# pprint(label_list)
# pprint(bioes_data_label)
