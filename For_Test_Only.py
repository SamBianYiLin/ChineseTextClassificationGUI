from Classify import MyClassifier
from utils import build_vocab, MAX_VOCAB_SIZE, DatasetIterater
classifier = MyClassifier(model_name='DPCNN', dataset='saved_dict', embedding='random', word=False)
rnn_result=classifier.classify("芯片科技厂商")
print(rnn_result)
