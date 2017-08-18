#!/usr/bin/env python
__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 20/08/2016'

import codecs
import MeCab
from modules.Vocabulary import *


class Batch:
    dataset_full_passes = 0
    use_mecab = True

    def __init__(self, data_file_name, vocabulary_file_path, batch_size, sequence_length):
        self.data_file = codecs.open(data_file_name, 'r', 'utf_8')

        self.vocabulary = Vocabulary()
        self.vocabulary.retrieve(vocabulary_file_path)

        self.batch_size = batch_size
        self.sequence_length = sequence_length

        self.data_word = []
        self.data_word_index = 0

        if self.use_mecab:
            mecab = MeCab.Tagger("-Owakati")
            for line in self.data_file:
                words_data = mecab.parse(line.encode('utf_8'))
                for word in words_data.split(' '):
                    self.data_word.append(word)

    def get_next_batch(self):
        string_len = self.batch_size * self.sequence_length + self.batch_size
        if not self.use_mecab:
            current_batch = self.data_file.read(string_len)
        else:
            string_length = string_len
            if len(self.data_word) - 1 < self.data_word_index + string_len:
                string_length = len(self.data_word) - self.data_word_index - 1
            current_batch = self.data_word[self.data_word_index : self.data_word_index + string_length]
            self.data_word_index += string_length

        batch_vector = []
        label_vector = []

        if len(current_batch) < string_len:
            while len(current_batch) < string_len:
                current_batch += u' '
            self.data_file.seek(0)
            self.dataset_full_passes += 1
            print "Pass {} done".format(self.dataset_full_passes)

        for i in np.arange(0, string_len, self.sequence_length + 1):
            sequence = current_batch[i:i + self.sequence_length]
            label = current_batch[i + self.sequence_length:i + self.sequence_length + 1]
            sequences_vector = []

            for char in sequence:
                if self.use_mecab:
                    char = char.decode('utf-8')
                sequences_vector.append(self.vocabulary.binary_vocabulary[char])
            batch_vector.append(sequences_vector)
            if not self.use_mecab:
                label_vector.append(self.vocabulary.binary_vocabulary[label])
            else:
                label_vector.append(self.vocabulary.binary_vocabulary[label[0].decode('utf-8')])

        return np.asarray(batch_vector), np.asarray(label_vector)

    def clean(self):
        self.data_file.close()
