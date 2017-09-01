__author__ = 'Tony Beltramelli www.tonybeltramelli.com - 19/08/2016'

import numpy as np
import codecs
import MeCab
from collections import OrderedDict

class Vocabulary:
    vocabulary = OrderedDict()
    binary_vocabulary = {}
    char_lookup = {}
    size = 0
    separator = '->'
    use_mecab = True

    def generate(self, input_file_path):
        input_file = codecs.open(input_file_path, 'r', 'utf_8')
        mecab = MeCab.Tagger("-Owakati")
        index = 0
        for line in input_file:
            if self.use_mecab:
                text = mecab.parse(line.encode('utf_8'))
                line = text.split(' ')
            for char in line:
                if char not in self.vocabulary:
                    self.vocabulary[char] = index
                    self.char_lookup[index] = char
                    index += 1
            if " " not in self.vocabulary:
                self.vocabulary[" "] = index
                self.char_lookup[index] = " "
                index += 1
        input_file.close()
        self.set_vocabulary_size()
        self.create_binary_representation()

    def retrieve(self, input_file_path):
        input_file = codecs.open(input_file_path, 'r', 'utf_8')
        buffer = ""
        index = 0
        vocab_count = {}
        for line in input_file:
            if not line in vocab_count:
                vocab_count[line] = 0
        self.size = len(vocab_count)
        input_file.seek(0)

        for line in input_file:
            try:
#                separator_position = len(buffer) + line.index(self.separator)
#                buffer += line
#                key = buffer[:separator_position]
                key = line.replace('\n','').replace('\r','')
#                value = buffer[separator_position + len(self.separator):]
#                value = np.fromstring(value, sep=',')

                if key not in self.binary_vocabulary:
                    value = np.zeros(self.size)
                    value[index] = 1
                    index+=1
                    self.binary_vocabulary[key] = value
                    self.vocabulary[key] = np.where(value == 1)[0][0]
                    self.char_lookup[np.where(value == 1)[0][0]] = key

                buffer = ""
            except ValueError:
                buffer += line
        input_file.close()
        self.set_vocabulary_size()

    def create_binary_representation(self):
        for key, value in self.vocabulary.iteritems():
            binary = np.zeros(self.size)
            binary[value] = 1
            self.binary_vocabulary[key] = binary

    def set_vocabulary_size(self):
        self.size = len(self.vocabulary)
        print "Vocabulary size: {}".format(self.size)

    def get_serialized_binary_representation(self):
        string = ""
        np.set_printoptions(threshold='nan')
        for key, value_v in self.vocabulary.iteritems():
#            array_as_string = np.array2string(value, separator=',', max_line_width=self.size * self.size)
            if not self.use_mecab:
                key = key.encode('utf-8')
#            string += "{}{}{}\n".format(key, self.separator, array_as_string[1:len(array_as_string) - 1])
            string += "{}\n".format(key)
        return string
