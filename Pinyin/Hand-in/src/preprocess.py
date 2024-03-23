import json
import re
from collections import Counter
from tqdm import tqdm


def get_pinyin2word():
    pinyin2word_mapping = {}
    with open('../data/lexicon/pinyin2word_all.txt', 'r', encoding='gbk') as file:
        for line in file:
            line_segments = line.strip().split()
            pinyin2word_mapping[line_segments[0]] = line_segments[1:]
    with open("../data/lexicon/pinyin2word.json", "w", encoding="utf-8") as json_file:
        json.dump(pinyin2word_mapping, json_file, ensure_ascii=False, indent=4)


def count_word_pairs(text):
    # ʹ��������ʽ�ҵ��Ǻ����ַ���������Ϊ�ָ���
    delimiter_pattern = re.compile(r'[^\u4e00-\u9fa5]+')
    segments = delimiter_pattern.split(text)

    word_pairs_counter = [Counter() for _ in range(4)]
    for segment in segments:
        # ȥ�����ַ���
        segment = segment.strip()
        if not segment:
            continue

        # ��ȡ����Ϊ i ���ַ���
        for i in range(1, 4):
            for j in range(len(segment) - i + 1):
                # �� word_pair_counter[i] �и�������ִ���
                word_pairs_counter[i][segment[j:j + i]] += 1
    return word_pairs_counter


def get_word_count():
    uni_word_counter = Counter()
    bi_word_counter = Counter()
    tri_word_counter = Counter()

    # ö��ÿ���ļ����ļ���
    for i in tqdm(range(4, 12)):
        with open(f'../data/sina_news_gbk/2016-{str(i).zfill(2)}.txt', 'r', encoding='gbk') as file:
            for line in tqdm(file):
                try:
                    data = json.loads(line).get('html', "")

                    # ͳ��һԪ����Ԫ����Ԫ�ʵĳ��ִ���
                    processed_data = count_word_pairs(data)
                    uni_word_counter += Counter(
                        {word: count for word, count in processed_data[1].items()})
                    bi_word_counter += Counter(
                        {word: count for word, count in processed_data[2].items()})
                    tri_word_counter += Counter(
                        {word: count for word, count in processed_data[3].items()})
                except:
                    pass

    uni_word_counter_dict = dict(uni_word_counter)
    bi_word_counter_dict = dict(bi_word_counter)
    tri_word_counter_dict = dict(tri_word_counter)

    # ���ֵ�д�뵽 JSON �ļ���
    with open("../data/sina_news_gbk/uni_word_count.json", "w", encoding="utf-8") as json_file:
        json.dump(uni_word_counter_dict, json_file, ensure_ascii=False, indent=4)
    with open("../data/sina_news_gbk/bi_word_count.json", "w", encoding="utf-8") as json_file:
        json.dump(bi_word_counter_dict, json_file, ensure_ascii=False, indent=4)
    with open("../data/sina_news_gbk/tri_word_count.json", "w", encoding="utf-8") as json_file:
        json.dump(tri_word_counter_dict, json_file, ensure_ascii=False, indent=4)


get_pinyin2word()  # ��ȡ pinyin2word.json
get_word_count()  # ��ȡ uni_word_count.json, bi_word_count.json, tri_word_count.json
