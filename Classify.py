# coding: UTF-8
import os
import sys
import pickle as pkl
from importlib import import_module
import numpy as np
import torch
from train_eval import init_network
from utils import build_vocab, MAX_VOCAB_SIZE, DatasetIterater
sys.path.append(os.path.join(os.path.dirname(__file__), '/saved_dict'))

class MyClassifier:
    def __init__(self, model_name, dataset, embedding, word):
        self.save_path = './saved_dict/' + model_name + '.ckpt'
        self.dataset = dataset  # 数据集目录
        self.model_name = model_name  # 模型
        self.embedding = embedding  # embedding
        self.word = word  # 数据集是否已分词
        self.labels = []
        # 读取类别
        with open(self.dataset + '/class.txt', 'r', encoding='utf-8') as file:
            for line in file:
                s = line.strip()
                self.labels.append(s)
                #print("%s" % s)

        #print("一共读取到%s个类别" % len(self.labels))

        # 创建模型配置
        x = import_module('models.' + self.model_name)
        self.config = x.Config(self.dataset, self.embedding)
        np.random.seed(1)
        torch.manual_seed(1)
        torch.cuda.manual_seed_all(1)
        torch.backends.cudnn.deterministic = True  # 保证每次结果一样

        #print("加载词汇表vocab.pkl...")
        self.vocab = self.build_dataset(self.config, self.word)

        # eval
        self.config.n_vocab = len(self.vocab)
        self.model = x.Model(self.config).to(self.config.device)
        if self.model_name != 'Transformer':
            init_network(self.model)

        #print("加载模型参数ckpt文件...")

        # 加载模型权重
        self.model.load_state_dict(torch.load(self.config.save_path, map_location='cpu', weights_only=True))
        self.model.eval()

    def build_dataset(self, config, ues_word):
        if ues_word:
            #print("按空格分词生成向量")
            tokenizer = lambda x: x.split(' ')  # 以空格隔开，word-level
        else:
            #print("按字生成向量")
            tokenizer = lambda x: [y for y in x]  # char-level
        if os.path.exists(config.vocab_path):
            #print("读取已生成的词汇表vocab.pkl")
            vocab = pkl.load(open(config.vocab_path, 'rb'))
        else:
            #print("读取训练集生成词汇表")
            if self.model_name == 'FastText':
                from utils_fasttext import build_vocab, MAX_VOCAB_SIZE, DatasetIterater
            else:
                from utils import build_vocab, MAX_VOCAB_SIZE, DatasetIterater
            vocab = build_vocab(config.train_path, tokenizer=tokenizer, max_size=MAX_VOCAB_SIZE, min_freq=1)
        #print(f"词汇大小: {len(vocab)}")
        return vocab

    def my_to_tensor(self, config, datas):
        x = torch.LongTensor([_[0] for _ in datas]).to(config.device)
        y = torch.LongTensor([_[1] for _ in datas]).to(config.device)

        # pad前的长度(超过pad_size的设为pad_size)
        seq_len = torch.LongTensor([_[2] for _ in datas]).to(config.device)
        return (x, seq_len), y
    def my_to_tensorFastText(self, config, datas):
        # xx = [xxx[2] for xxx in datas]
        # indexx = np.argsort(xx)[::-1]
        # datas = np.array(datas)[indexx]
        x = torch.LongTensor([_[0] for _ in datas]).to(config.device)
        y = torch.LongTensor([_[1] for _ in datas]).to(config.device)
        bigram = torch.LongTensor([_[3] for _ in datas]).to(config.device)
        trigram = torch.LongTensor([_[4] for _ in datas]).to(config.device)

        # pad前的长度(超过pad_size的设为pad_size)
        seq_len = torch.LongTensor([_[2] for _ in datas]).to(config.device)
        return (x, seq_len, bigram, trigram)


    def str2numpy(self, text, config):
        UNK, PAD = '<UNK>', '<PAD>'
        tokenizer = lambda x: [y for y in x]  # char-level
        vocab = self.vocab

        def to_numpy(content, pad_size=32):
            word_line = []
            token = tokenizer(content)
            seq_len = len(token)
            if pad_size:
                if len(token) < pad_size:
                    token.extend([PAD] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size
            # word to id
            for word in token:
                word_line.append(vocab.get(word, vocab.get(UNK)))
            # 文本转换为向量，标签设置为-1
            return [(word_line, -1, len(token))]

        npy = to_numpy(text, config.pad_size)
        return DatasetIterater(npy, config.batch_size, config.device)
    def str2numpyFastText(self, text, config):
        UNK, PAD = '<UNK>', '<PAD>'
        tokenizer = lambda x: [y for y in x]  # char-level
        vocab = pkl.load(open('./saved_dict/vocab.pkl', 'rb'))
        #print(text)

        def biGramHash(sequence, t, buckets):
            t1 = sequence[t - 1] if t - 1 >= 0 else 0
            return (t1 * 14918087) % buckets

        def triGramHash(sequence, t, buckets):
            t1 = sequence[t - 1] if t - 1 >= 0 else 0
            t2 = sequence[t - 2] if t - 2 >= 0 else 0
            return (t2 * 14918087 * 18408749 + t1 * 14918087) % buckets

        def to_numpy(content, pad_size=32):
            words_line = []
            token = tokenizer(content)
            seq_len = len(token)
            #print("生成的npy:", npy)
            #print("npy长度:", len(npy))
            if pad_size:
                if len(token) < pad_size:
                    token.extend([PAD] * (pad_size - len(token)))
                else:
                    token = token[:pad_size]
                    seq_len = pad_size
            # word to id
            for word in token:
                words_line.append(vocab.get(word, vocab.get(UNK)))

            # fasttext ngram
            buckets = config.n_gram_vocab
            bigram = []
            trigram = []
            # ------ngram------
            for i in range(pad_size):
                bigram.append(biGramHash(words_line, i, buckets))
                trigram.append(triGramHash(words_line, i, buckets))
            # -----------------
            return [(words_line, -1, seq_len, bigram, trigram)]

        npy = to_numpy(text, config.pad_size)
        npy = self.my_to_tensorFastText(config, npy)
        return npy
    def classify(self, text):
        # FastText
        if self.model_name == 'FastText':
            data = self.str2numpyFastText(text, self.config)
            outputs = self.model(data)
            probabilities = torch.softmax(outputs, dim=1)

            # 获取前5个最大概率及其索引
            topk_values, topk_indices = torch.topk(probabilities, k=5, dim=1)

            # 打印结果
            # for i in range(len(topk_indices[0])):
            #     print(
            #         f"{[self.labels[topk_indices[0].cpu().numpy()[i]]]} {topk_values[0].cpu().detach().numpy()[i]:.4f}")
            # 概率值最大的预测结果
            predict_result = torch.max(outputs.data, 1)[1].cpu().numpy()[0]
            # 对应的分类
            cls = self.labels[predict_result]
            #print(cls)
            return cls
        # 除了FastText
        else:
            data = self.str2numpy(text, self.config)
            for texts, labels in data:
                outputs = self.model(texts)
                if len(outputs.shape) == 1:
                    outputs = outputs.unsqueeze(0)
                probabilities = torch.softmax(outputs, dim=1)

                # 获取前5个最大概率及其索引
                topk_values, topk_indices = torch.topk(probabilities, k=5, dim=1)

                # 打印结果
                # for i in range(len(topk_indices[0])):
                #     print(
                #         f"{[self.labels[topk_indices[0].cpu().numpy()[i]]]} {topk_values[0].cpu().detach().numpy()[i]:.4f}")
                # 概率值最大的预测结果
                predict_result = torch.max(outputs.data, 1)[1].cpu().numpy()[0]
                # 对应的分类
                cls = self.labels[predict_result]
                return cls

# classifier = MyClassifier(model_name='DPCNN', dataset='saved_dict', embedding='random', word=False)
# classifier.classify("篮球明星")