import numpy as np
from pyhanlp import *
import os
import pickle


class Word2Vec:
    """
    假设输入至少需要两个部分
    一部分是文本，以列表形式存储，如：['我们是中国人，我们爱自己的祖国', '蜀道难，难于上青天']
    一部分是语料库，以键值对组成，如：{'我们':[20.78, 276.12, .....]}, 要求向量空间为numpy格式，非list格式

    """

    def __init__(self, sentence_list, word_bag=None, diy=True, file_name=None):
        if diy:
            self.word_bag = self.diy(file_name)
        else:
            self.word_bag = word_bag
        self.sentence_list = sentence_list
        self.char_mapping, self.vec_mapping = self.get_char_mapping()
        self.dim = len(self.char_mapping['的'])  # - -
        self.char_mapping_plus, self.vec_mapping_plus = self.get_sentence_mapping()

    def diy(self, file_name):
        with open(file_name, 'r') as f:
            items = f.readlines()[1:]
            f.close()
        word_bag = {}
        for item in items:
            info = item.split(' ')
            key = info[0]
            values = np.asarray(info[1:-1], dtype=np.float)
            word_bag[key] = values
        return word_bag

    def get_char_mapping(self):
        """
        加载或计算词向量
        :return:
        """
        current_path = os.getcwd()
        char_to_sum_file = current_path + '/char_to_sum.pkl'
        sum_to_char_file = current_path + '/sum_to_char.pkl'
        if not os.path.isfile(char_to_sum_file) or not os.path.isfile(sum_to_char_file):
            char_to_sum = {}
            sum_to_char = {}

            for key in self.word_bag:
                sum_ = str(np.sum(self.word_bag[key]))
                char_to_sum[key] = self.word_bag[key]
                sum_to_char[sum_] = key

            with open(char_to_sum_file, 'wb') as f:
                pickle.dump(char_to_sum, f)
                f.close()

            with open(sum_to_char_file, 'wb') as f:
                pickle.dump(sum_to_char, f)
                f.close()
        else:
            with open(char_to_sum_file, 'rb') as f:
                char_to_sum = pickle.load(f)
                f.close()

            with open(sum_to_char_file, 'rb') as f:
                sum_to_char = pickle.load(f)
                f.close()
        return char_to_sum, sum_to_char

    def get_sentence_mapping(self):
        current_path = os.getcwd()
        char_to_sum_plus_file = current_path + '/char_to_sum_plus.pkl'
        sum_to_char_plus_file = current_path + '/sum_to_char_plus.pkl'
        if not os.path.isfile(char_to_sum_plus_file) or not os.path.isfile(sum_to_char_plus_file):
            char_to_sum_plus = {}
            sum_to_char_plus = {}
            for sentence in self.sentence_list:
                tmp = np.zeros(shape=self.dim)
                index = 1
                for obj in HanLP.segment(sentence):
                    word = obj.word
                    if word in self.char_mapping:
                        tmp += self.char_mapping[word]
                    else:
                        tmp += np.zeros(shape=self.dim)
                    index += 1
                tmp /= index
                char_to_sum_plus[sentence] = tmp
                sum_to_char_plus[str(np.sum(tmp))] = sentence

                with open(char_to_sum_plus_file, 'wb') as f:
                    pickle.dump(char_to_sum_plus, f)
                    f.close()

                with open(sum_to_char_plus_file, 'wb') as f:
                    pickle.dump(sum_to_char_plus, f)
                    f.close()
        else:
            with open(char_to_sum_plus_file, 'rb') as f:
                char_to_sum_plus_file = pickle.load(f)
                f.close()

            with open(sum_to_char_plus_file, 'rb') as f:
                sum_to_char_plus_file = pickle.load(f)
                f.close()

        return char_to_sum_plus_file, sum_to_char_plus_file

    @staticmethod
    def cosine_similarity(v1, v2):
        # 余弦距离
        v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
        up = np.dot(v1, v2)
        down = np.linalg.norm(v1) * np.linalg.norm(v2)
        return round(up / down, 6)

    @staticmethod
    def euclid_distince(v1, v2):
        # 欧氏距离
        v1 /= np.sum(v1)
        v2 /= np.sum(v2)
        v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
        return round(np.linalg.norm(v1 - v2), 6)
