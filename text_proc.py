import re
import jieba
from collections import Counter
#re（正则表达式）、jieba（中文分词库）和collections.Counter（计数器）

def clean_html_tags(text):
    """ 使用正则表达式去除HTML标签 """
    cleanr = re.compile('<.*?>')#< 和 > 分别匹配HTML标签的起始和结束符号。
    cleantext = re.sub(cleanr, '', text)#将所有与cleanr模式匹配的部分替换为空字符串''
    return cleantext


def remove_punctuation(text):
    """ 去除标点符号 """
    punctuation = r'“”‘’、？》《。，】【}{、|+=——-）（*&……%￥#@！~·`~!@#$%%^&*(){}[]\/?><.,;:''""|'
    text_without_punctuation = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text_without_punctuation


def word_segmentation(text):
    """ 对文本进行分词，并过滤掉单个字符的词 """
    words = jieba.lcut(text)#lcut 返回一个列表，其中包含分词后的所有词语。
    # 过滤掉长度为1的词
    filtered_words = [word for word in words if len(word.strip()) >= 2]
    return filtered_words


def count_word_frequency(words):
    """ 统计词频 """
    word_counts = Counter(words)#Counter 类来统计一个可迭代对象（如列表）中每个元素出现的次数
    return word_counts


def process_files(file_list, output_file='words.txt'):
    all_words = []

    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 清理HTML标签
            clean_content = clean_html_tags(content)

            # 移除标点符号
            clean_text = remove_punctuation(clean_content)

            # 分词并过滤
            words = word_segmentation(clean_text)

            # 添加到总的词汇列表
            all_words.extend(words)#将列表 words 中的所有元素添加到列表 all_words 的末尾

        except Exception as e:
            print(f"Error processing {file}: {e}")

    if all_words:
        # 统计词频
        word_freq = count_word_frequency(all_words)

        # 输出词频最高的20个词到控制台
        print("Top 20 most frequent words (2 characters or longer):")
        for word, freq in word_freq.most_common(20):#将每个元组解包为 word 和 freq 变量
            print(f"{word}: {freq}")#使用格式化字符串（f-string）打印每个单词及其频率，格式为 单词: 频率

        # 写入分词结果及词频到文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("Word\tFrequency\n")#向文件写入表头行 "Word\tFrequency\n"，表示接下来的内容是单词和频率的列表
            for word, freq in word_freq.items():
                outfile.write(f"{word}\t{freq}\n")
        print(f"Results saved to {output_file}")
    else:
        print("No valid words found.")


if __name__ == "__main__":
    # 文件列表
    files = ['1.txt', '2.txt', '3.txt']

    process_files(files)