import string
import pickle
import unicodedata
import re

code = {'A':'0', 'E':'0', 'I':'0', 'O':'0', 'U':'0', 'H':'0', 'W':'0', 'Y':'0', 'B':'1', 'F':'1', 'P':'1', 'V':'1', 'C':'2', 'G':'2', 'J':'2', 'K':'2', 'Q':'2', 'S':'2', 'X':'2', 'Z':'2', 'D':'3', 'T':'3', 'L':'4', 'M':'5', 'N':'5', 'R':'6'}

def Vocab():          #to create vocabulary
    lookup = {}
    f = open("engmix.txt", mode="r", encoding="utf8")
    view = f.read().strip('').split('\n')
    a = "["+string.punctuation+"]"
    for word in view:
        word = re.sub(a,"",word)
        word = unicodedata.normalize('NFD', word).encode('ascii', 'ignore')
        word = word.decode("utf8")
        word = word.upper()
        res = word[0]
        for i in range(1, word.__len__()):
            res += code[word[i]]

        res = re.sub("0", "", res)
        res = removeDuplicates(res)          #should have been imported from SpellingCorrector.py
        res = res + "0" * (4 - len(res))
        lookup[word] = res[:4]
    dumped = open("dumped.pkl","wb")
    pickle.dump(lookup,dumped)
    dumped.close()
    f.close()
    return lookup