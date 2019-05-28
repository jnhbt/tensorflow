#!/usr/bin/python
import sys
import os
import json

def gen_labels(src="./text.txt",dist="../data/labels.txt"):
    text_file = os.path.join(sys.path[0],src)
    fr = open(text_file,"r+",encoding="utf-8")
    content = fr.read().replace("\n","").replace(" ","")
    labels = get_labels(dist)
    cnt = len(labels)
    labels_file = os.path.join(sys.path[0], dist)
    fw = open(labels_file, "w+", encoding="utf-8")
    for index,char in enumerate(content,cnt+1):
        if char != None and char not in labels.values():
            key = str(index).zfill(5)
            labels[key] = char
    json_labels = json.dumps(labels)
    fw.write(json_labels)
    fw.close()
    return labels


def get_labels(src="../data/labels.txt"):
    labels_file = os.path.join(sys.path[0], src)
    labels = {}
    if not os.path.exists(labels_file):
        return  labels
    fr = open(labels_file, "r+", encoding="utf-8")
    labels_content = fr.read().strip().replace("\n", "")
    fr.close()
    if len(labels_content) > 0:
        labels = json.loads(labels_content)
    return labels


if __name__ == "__main__":
    labels = gen_labels("../../assets/text.txt","../../data/labels.txt")
    # labels = get_labels()
    # for (key,char) in labels.items():
    #     print(key+":"+char)