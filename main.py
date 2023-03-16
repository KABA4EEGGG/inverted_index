import re
from typing import Dict, List
import json


def load_documents(filepath: str):
    dataset = open(filepath, encoding="utf8")
    doc = dict()
    for i in dataset:
        doc_id, content = i.lower().split("\t", 1)
        content = content.rstrip()
        content = re.sub(r'[^\x00-\x7f]', '', content)
        doc_id = int(doc_id)
        doc[doc_id] = content
    dataset.close()
    return doc


class InvertedIndex(Dict):
    def query(self, words: List[str]):
        first_word = set(self[words[0]])
        set_words = [set(self[words[i]]) for i in range(1, len(words))]
        out = list(first_word.intersection(*set_words))
        return out

    def dump(self, filepath: str):
        file = open(filepath, mode="w", encoding="utf8")
        json.dump(self, file)
        file.close()

    @classmethod
    def load(cls, filepath: str):
        file = open(filepath, mode="r", encoding="utf8")
        load_file = cls(json.load(file))
        file.close()
        return load_file


def build_inverted_index(documents: Dict[int, str]):
    index = InvertedIndex()
    stop_word = [h.rstrip() for h in open('stop_words_en.txt').readlines()]
    for i, text in documents.items():

        text_pars = re.split(r"\W+", text)

        words = []
        [words.append(x) for x in text_pars if x not in words]
        terms = [word for word in words if word not in stop_word]
        for word in terms:
            if not (word in index.keys()):
                index[word] = [i]
            else:
                index[word].append(i)
    return index


