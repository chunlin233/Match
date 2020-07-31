# -*- coding:utf-8 -*-
#
# Created by Drogo Zhang
#
# On 2019-04-10

import numpy as np
import difflib

import re
from simhash import Simhash

from nltk.text import TextCollection
from nltk.tokenize import word_tokenize


def cosine_similarity(sentence1: str, sentence2: str) -> float:
    """
    compute normalized COSINE similarity.
    :param sentence1: English sentence.
    :param sentence2: English sentence.
    :return: normalized similarity of two input sentences.
    """
    seg1 = sentence1.strip(" ").split(" ")
    seg2 = sentence2.strip(" ").split(" ")
    word_list = list(set([word for word in seg1 + seg2]))
    word_count_vec_1 = []
    word_count_vec_2 = []
    for word in word_list:
        word_count_vec_1.append(seg1.count(word))
        word_count_vec_2.append(seg2.count(word))

    vec_1 = np.array(word_count_vec_1)
    vec_2 = np.array(word_count_vec_2)

    num = vec_1.dot(vec_2.T)
    denom = np.linalg.norm(vec_1) * np.linalg.norm(vec_2)
    cos = num / denom
    sim = 0.5 + 0.5 * cos

    return sim


def compute_levenshtein_distance(sentence1: str, sentence2: str) -> int:
    """
    compute levenshtein distance.

    """
    leven_cost = 0
    s = difflib.SequenceMatcher(None, sentence1, sentence2)
    for tag, i1, i2, j1, j2 in s.get_opcodes():

        if tag == 'replace':
            leven_cost += max(i2 - i1, j2 - j1)
        elif tag == 'insert':
            leven_cost += (j2 - j1)
        elif tag == 'delete':
            leven_cost += (i2 - i1)

    return leven_cost


def compute_levenshtein_similarity(sentence1: str, sentence2: str) -> float:
    """Compute the hamming similarity."""
    leven_cost = compute_levenshtein_distance(sentence1, sentence2)
    return 1-(leven_cost / len(sentence2))


def compute_simhash_hamming_similarity(sentence1: str, sentence2: str) -> float:
    """need to normalize after compute!"""

    def get_features(s):
        width = 3
        s = s.lower()
        s = re.sub(r'[^\w]+', '', s)
        return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

    hash_value1 = Simhash(get_features(sentence1)).value
    hash_value2 = Simhash(get_features(sentence2)).value

    return compute_levenshtein_similarity(str(hash_value1), str(hash_value2))


def compute_jaccard_similarity(sentence1: str, sentence2: str) -> float:
    word_set1 = set(sentence1.strip(" ").split(" "))
    word_set2 = set(sentence2.strip(" ").split(" "))

    return len(word_set1 & word_set2) / len(word_set1 | word_set2)


def compute_bm25_similarity(sentence1: str, sentence2: str) -> float:
    # todo
    return 1.0


def compute_tf_idf_similarity(query: str, content: str, type: str) -> float:
    """
    Compute the mean tf-idf or tf
     similarity for one sentence with multi query words.
    :param query: a string contain all key word split by one space
    :param content: string list with every content relevent to this query.
    :return: average tf-idf or tf similarity.
    """
    sents = [word_tokenize(content), word_tokenize("")]  # add one empty file to smooth.
    corpus = TextCollection(sents)  # 构建语料库

    result_list = []
    for key_word in query.strip(" ").split(" "):
        if type == "tf_idf":
            result_list.append(corpus.tf_idf(key_word, corpus))
        elif type == "tf":
            result_list.append(corpus.tf(key_word, corpus))
        else:
            raise KeyError

    return sum(result_list) / len(result_list)


def edit(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    return matrix[len(str1)][len(str2)]

class StringPatternt(object):
    def __init__(self, chr, p):
        self.chr = chr;
        self.p = p;
        self.p_len = len(p);
        self.pi = [0 for i in range(self.p_len)];

    def set_pattern(self, p):
        self.p = p;
        self.p_len = len(p);

    def set_chr(self, chr):
        self.chr = chr;

    '''KMP'''

    def __kmp_partial_match_table__(self):
        k = 0;
        q = 1;
        # self.pi[0] = 0;
        while q < self.p_len:
            while (k > 0) and (self.p[k] != self.p[q]):
                k = self.pi[k - 1];
            if self.p[k] == self.p[q]:
                k = k + 1;
            self.pi[q] = k;
            q = q + 1;
        return 0;

    def string_pattern_kmp(self):
        self.__kmp_partial_match_table__();
        print(self.pi);
        list_size = len(self.chr);
        pi_len = len(self.pi);
        k = 0;
        for q in range(list_size):
            while (k > 0) and (self.p[k] != self.chr[q]):
                k = self.pi[k - 1];
            if self.p[k] == self.chr[q]:
                k = k + 1;
            if k == pi_len:
                return q - pi_len + 1;
            # q = q+1;
        return 0;

    '''BM'''

    def __calc_match__(self, num):
        k = num;
        j = 0;
        while k >= 0:
            if self.p[-k] == self.p[j]:
                k = k - 1;
                j = j + 1;
                if k <= 0:
                    self.pi[num - 1] = num;
                    return 0;
            else:
                if num == 1:
                    return 0;
                self.pi[num - 1] = self.pi[num - 2];
                return 0;

    def __init_good_table__(self):
        i = 1;
        while i <= self.p_len:
            self.__calc_match__(i);
            i = i + 1;
        print(self.pi);
        return 0;

    def __check_bad_table__(self, tmp_chr):
        i = 1;
        while self.p_len - i >= 0:
            if self.p[-i] == tmp_chr:
                return i;
            else:
                i = i + 1;
        return self.p_len + 1;

    def __check_good_table__(self, num):
        if not num:
            return self.p_len;
        else:
            return self.pi[num];

    def string_pettern_bm(self):
        self.__init_good_table__();
        tmp_len = self.p_len;
        i = 1;
        while tmp_len <= len(self.chr):
            if self.p[-i] == self.chr[tmp_len - i]:
                i = i + 1;
                if i > self.p_len:
                    return tmp_len - self.p_len;
            else:
                tmp_bad = self.__check_bad_table__(self.chr[tmp_len - i]) - i;
                tmp_good = self.p_len - self.__check_good_table__(i - 1);
                tmp_len = tmp_len + max(tmp_bad, tmp_good);
                print(tmp_bad, tmp_good, tmp_len);
                i = 1;
        return 0;

    '''sunday'''

    def __check_bad_shift__(self, p):
        i = 0;
        while i < self.p_len:
            if self.p[i] == p:
                return i;
            else:
                i = i + 1;
        return -1;

    def string_pattern(self):
        # self.__init_good_table__();
        tmp_len = 0;
        tmp_hop = self.p_len;
        i = 0;
        while tmp_hop <= len(self.chr):
            if self.p[i] == self.chr[tmp_len + i]:
                i = i + 1;
                if i == self.p_len:
                    return tmp_len;
            else:
                tmp_len = tmp_len + self.p_len - self.__check_bad_shift__(self.chr[tmp_hop]);
                tmp_hop = tmp_len + self.p_len;
                i = 0;
        return 0;

if __name__ == '__main__':
    # print(compute_tf_idf_similarity("one sentence",
    #                                 ["this is sentence one", "this is sentence two", "this is sentence three"],
    #                                 'tf_idf'))


    # print(compute_tf_idf_similarity("sentence",
    #                                 "this is sentence one, this is sentence two, this is sentence three",
    #                                 'tf'))
    #
    # print("ray@iitp.ac.in".split('@')[0])
    # print(compute_levenshtein_similarity("ray", "raydn"))
    #
    # print(compute_simhash_hamming_similarity("ray", "raynd"))
    #
    # print(compute_tf_idf_similarity("ray", "ray nd", 'tf'))
    #
    # similarity = compute_tf_idf_similarity('combat readiness',
    #                           'Al Qassam: Our combat readiness comes after Israel determination to launch aggressive attack prior Israeli elections\n',
    #                           'tf')
    # print(similarity)

    # import re
    # pattern = 'Gardner'
    # text = 'jgardner'
    # result = re.match(r'.*('+ pattern +').*', text, re.I)
    # print(result.group())
    # print(result.group(1))
    #
    # pattern = ['JG', 'qin']
    # text = 'jgqin'
    # for p in pattern:
    #     result = re.match(r'.*(' + p + ').*', text, re.I)
    #     print(result.group(1))
    #
    # str1 = "Xiao, BG; Gu, MY; Xiao, SS".lower().replace(', ', '').replace('; ', ' ')
    # print(str1)
    # print(compute_levenshtein_similarity(str1, "xiaobg"))
    # print(compute_levenshtein_similarity("zhang", "zhang"))
    #
    # print(compute_simhash_hamming_similarity(str1, "xiaobg"))
    # print(compute_simhash_hamming_similarity("zhang", "zhang"))
    #
    # str1 = 'Chung, CC; Narra, S; Jokar, E; Wu, HP; Diau, EWG'
    # str1_ = 'Chung, CC; Narra, S; Jokar, E; Wu, HP; Diau, EWG'.lower().replace(', ', '').replace('; ', ' ')
    # print(str1_)
    # print(compute_simhash_hamming_similarity(str1, "diau"))
    # print(compute_simhash_hamming_similarity(str1, "naitaoyan"))

    sp = StringPatternt('zhangnpc', 'zhangp')
    sp.string_pattern_kmp()

    # print(edit("ray", "raynd"))
#     # print(cosine_similarity("a v c ", "ab v c"))
#     # print(Simhash('aa').distance(Simhash('bb')))

