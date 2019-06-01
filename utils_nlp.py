import numpy as np
import os
import pickle
from pyhanlp import HanLP

current_path = os.getcwd()


class Word2Vec:
    """
    简洁版词向量转换脚本

    :param  sentence_list       :   传入的句子，以列表形式存储。如['我们是中国人，我们爱自己的祖国', '蜀道难，难于上青天']
    :param  vec_space           :   词向量空间，如{'的': [.....], '银行': [......]}
    :param  file_name           :   如果没有传入vec_apace，请传入其他格式的文本，此处以[https://github.com/Embedding/Chinese-Word-Vectors]的嵌入语料库为基准
                                        如果是其他形式的词向量，建议重写load_vec_space函数
    :param  overload_space      :   是否重新生成新的词向量映射表，一般用于修改 「语料库」 的情况下置为True
    :param  overload_sentence   :   是否重新生成新的句子向量映射表，一般用于修改 「输入句子」 的情况下置为True

    example:
        a = '他说的是假话'
        b = '他骗人'
        w2v = nlp.Word2Vec(sentence_list=[a, b], file_name='sgns.financial.char')
        # 语料库来源于：[https://github.com/Embedding/Chinese-Word-Vectors]
        print(w2v.sentence_mapping)
        v_a, v_b = w2v.sentence_mapping[a], w2v.sentence_mapping[b]
        print('余弦相似度:', w2v.cosine_similarity(v_a, v_b))

    """

    def __init__(self, sentence_list, vec_space=None, file_name=None, overload_space=False, overload_sentence=False):

        self.sentence_list = sentence_list
        if not vec_space:
            self.vec_space = self.load_vec_space(file_name, overload=overload_space)
        else:
            self.vec_space = vec_space
        # 单词单字映射表
        # {'的': [....], '人民银行': [....]}
        self.char_mapping = self.vec_space
        self.dim = len(self.char_mapping['的'])
        # 句子映射表
        # {'我们是中国人': [......]}
        self.sentence_mapping = self.get_sentence_mapping(overload=overload_sentence)

    def load_vec_space(self, file_name, overload=False):
        """

        :param file_name:   解析传入的文件，转成pkl文件
        :return:            vec_space,如： {'的': [.....], '银行': [......]}
        """
        vec_space_file = current_path + '/char_mapping.pkl'
        if not os.path.isfile(vec_space_file) or overload:
            print('首次加载词向量时间较长，请稍等......')
            with open(file_name, 'r') as f:
                items = f.readlines()[1:]
                f.close()
            vec_space = {}
            for item in items:
                info = item.split(' ')
                key = info[0]
                values = np.asarray(info[1:-1], dtype=np.float)
                vec_space[key] = values
            with open(vec_space_file, 'wb') as f:
                pickle.dump(vec_space, f)
                f.close()
        else:
            with open(vec_space_file, 'rb') as f:
                vec_space = pickle.load(f)
                f.close()
        return vec_space

    def get_sentence_mapping(self, overload=False):
        """
        句子映射表
        :return:    vec_space,如： {'我们是中国人，我们爱自己的祖国':[......], '蜀道难，难于上青天':[......]}
        """
        sentence_to_vec_file = current_path + '/sentence_mapping.pkl'
        if not os.path.isfile(sentence_to_vec_file) or overload:
            print('首次加载句子时间较长，请稍等......')
            sentence_to_vec = {}
            for sentence in self.sentence_list:
                tmp = np.zeros(shape=self.dim)
                index = 0
                for obj in HanLP.segment(sentence):
                    word = obj.word
                    if word in self.char_mapping:
                        tmp += self.char_mapping[word]
                    else:
                        tmp += np.zeros(shape=self.dim)
                    index += 1
                tmp /= index
                sentence_to_vec[sentence] = tmp

                with open(sentence_to_vec_file, 'wb') as f:
                    pickle.dump(sentence_to_vec, f)
                    f.close()

        else:
            with open(sentence_to_vec_file, 'rb') as f:
                sentence_to_vec = pickle.load(f)
                f.close()

        return sentence_to_vec

    @staticmethod
    def cosine_similarity(v1, v2):
        """
        计算两个向量的余弦相似度
        :param v1: 向量1
        :param v2: 向量2
        :return:
        """
        # 余弦距离
        if not isinstance(v1, np.ndarray) or not isinstance(v2, np.ndarray):
            v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
        up = np.dot(v1, v2)
        down = np.linalg.norm(v1) * np.linalg.norm(v2)
        return round(up / down, 6)

    @staticmethod
    def euclid_distince(v1, v2):
        """
        计算两个向量的欧氏距离
        :param v1: 向量1
        :param v2: 向量2
        :return:
        """
        # 欧氏距离
        if not isinstance(v1, np.ndarray) or not isinstance(v2, np.ndarray):
            v1, v2 = np.asarray(v1, dtype=np.float), np.asarray(v2, dtype=np.float)
        v1 /= np.sum(v1)
        v2 /= np.sum(v2)
        return round(np.linalg.norm(v1 - v2), 6)


from sklearn.cluster import KMeans


class Kmeans:

    def __init__(self, vectors, sentence=None, cluster_n=5, sample_n=5, max_iter=1000):
        self.vectors = vectors
        self.sentence = sentence
        self.result = self.fit(cluster_n=cluster_n, sample_n=sample_n, max_iter=max_iter)

    def fit(self, cluster_n=5, sample_n=5, max_iter=1000):
        info = KMeans(n_clusters=cluster_n, random_state=0, max_iter=max_iter).fit(self.vectors)
        lables = info.labels_
        centers = info.cluster_centers_
        # dic = {'0': {'indexs':[20, 28, 46...], 'info': [[adasd], [adh]......]}}
        dic = {}
        for i in range(cluster_n):
            dic['%s' % i] = dict()
            dic['%s' % i]['indexs'] = np.where(lables == i)[0][:sample_n]
            dic['%s' % i]['info'] = []
            dic['%s' % i]['center'] = centers[i]
            for index in dic['%s' % i]['indexs']:
                distance = Word2Vec.euclid_distince(centers[i], self.vectors[j])
                if self.sentence:
                    dic['%s' % i]['info'].append(
                        {'index': index,
                         'vector': self.vectors[index],
                         'sentence': self.sentence[index],
                         'distance': distance}
                    )
                else:
                    dic['%s' % i]['info'].append(
                        {'index': index,
                         'vector': self.vectors[index],
                         'distance': distance}
                    )
            dic['%s' % i]['info'] = sorted(dic['%s' % i]['info'], key=lambda x: x['distance'])
        return dic
