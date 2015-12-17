# -*- coding: utf-8 -*-                                                                                                                                                                                                       
# cabocha を pythonから使うために、、、                                                                                                                                                                                       
import commands,sys,re

# 入力文をファイルに保存して、コマンドライン実行でcabocha解析                                                                                                                                                                 
def parse(sent):
    f = open("aaaaa.txt","w")
    f.write(sent)
    f.close()
    return commands.getoutput("cat aaaaa.txt | cabocha -f 1 -n 3")

# 形態素のクラス                                                                                                                                                                                                              
class Morph:
    def __init__(self,surface,pos,pos1,pos2,base):
        self.surface = surface
        self.pos = pos
        self.pos1 = pos1
        self.pos2 = pos2
        self.base = base
        self.all = "-".join([surface,pos,pos1,pos2])

# チャンクのクラス                                                                                                                                                                                                            
class Chunk:
    def __init__(self,morphs):
        self.morphs = morphs
    def update(self,surface,parent):
        self.surface = surface
        self.parent = parent
        self.tagged = " ".join([m.all for m in self.morphs])

# パーズされた文を出現順をキーとするチャンクの辞書として返す                                                                                                                                                                  
def parsed2chunks(parsed_sent):
    parsed_list = parsed_sent.split("\n")
    chunks = {}
    pids = {}
    for l in parsed_list:
        if l[0] == "*":
            id,dep = int(l.split()[1]),int(l.split()[2][:-1])
            chunk = Chunk(morphs=[])
            chunks[id] = chunk
            pids[id] = dep
        elif l == "EOS":
            break
        else:
            (surface, others) = l.split()[:2]
            temp = others.split(",")
            (pos, pos1, pos2, base) = temp[0], temp[1], temp[2], temp[6]
            morph = Morph(surface,pos,pos1,pos2,base)
            chunk.morphs.append(morph)
    for key,chunk in chunks.items():
        if pids[key] == -1:
            parent = None
        else:
            parent = chunks[pids[key]]
        surface = "".join([m.surface for m in chunk.morphs])
        chunk.update(surface,parent)
    return chunks
