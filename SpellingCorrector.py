#Self-enhancements in SOUNDEX:
# GM with M
# DG with G
# GH with H ...WHEN... not at start of word!!!!!!!!!
# GN with N (not 'ng')
# KN with N
# PH with F
# MP with M ...WHEN... it is followed by S, Z, or T!!!!!!!!!!!!!
# PS with S ...WHEN... it starts a word!!!!!!!!
# PF with F ...WHEN... it starts a word!!!!!!!!
# MB with M
# TCH with CH
# A or I with E WHEN - starts word+followed by[AEIO] !!!

import sys
import string
import speech_recognition as sr
import re
import unicodedata
from nltk.tokenize import WordPunctTokenizer
import pickle

code = {'A':'0', 'E':'0', 'I':'0', 'O':'0', 'U':'0', 'H':'0', 'W':'0', 'Y':'0', 'B':'1', 'F':'1', 'P':'1', 'V':'1', 'C':'2', 'G':'2', 'J':'2', 'K':'2', 'Q':'2', 'S':'2', 'X':'2', 'Z':'2', 'D':'3', 'T':'3', 'L':'4', 'M':'5', 'N':'5', 'R':'6'}
numerals = {'1':'ONE','2':'TWO', '3':'THREE','4':'FOUR','5':'FIVE','6':'SIX','7':'SEVEN','8':'EIGHT','9':'NINE','0':'ZERO'}


def SoundexEnhancementRules(word):

    if(word[:2]== "PS"):
        word = re.sub("PS","S",word,count=1)
    elif(word[:2]== "PF"):
        word = re.sub("PF", "F", word,count=1)

    if(word[:2]!="GH"):
        word = re.sub("GH", "H", word)


    word = re.sub("MPS","MS",word)
    word = re.sub("MPZ","MZ",word)
    word = re.sub("MPT","MT",word)
    word = re.sub("TCH","CH",word)
    word = re.sub("MB","M",word)
    word = re.sub("PH","F",word)
    word = re.sub("KN","N",word)
    word = re.sub("GN","N",word)
    word = re.sub("GM","M",word)
    word = re.sub("DG","G",word)

    if(word[0]=="A" or word[0]=="I") and len(word)>1:
        if(word[1] in ["E","I"]):
            word = re.sub("A","E",word,count=1)

    for i in word:
        if(i in numerals):
            word = re.sub(i,numerals[i],word)
    return word


def Preprocess(inp):
    inp = unicodedata.normalize('NFD', inp).encode('ascii', 'ignore')
    inp = inp.decode("utf8")
    inp = WordPunctTokenizer().tokenize(inp)
    return inp

def ApplyRules(inp):
    inp = [SoundexEnhancementRules(word) for word in inp]
    return inp


def removeDuplicates(S):
    ans = ""
    n = len(S)
    if (n < 2):
        return S

    S = list(S.rstrip())
    j=0
    for i in range(n):
        if (S[j] != S[i]):
            j += 1
            S[j] = S[i]

    j += 1
    S = S[:j]
    for i in S:
        ans += i
    return ans


def editDistance(str1, str2, m, n):
    if m == 0:
        return n

    if n == 0:
        return m

    if str1[m - 1] == str2[n - 1]:
        return editDistance(str1, str2, m - 1, n - 1)

    return 1 + min(editDistance(str1, str2, m, n - 1),  # Insert
                   editDistance(str1, str2, m - 1, n),  # Remove
                   editDistance(str1, str2, m - 1, n - 1)  # Replace
                   )


def Soundex(inp):
    codex = {}
    for word in inp:
        if(word not in string.punctuation):
            res = word[0]
            for i in range(1, word.__len__()):
                res += code[word[i]]

            res = re.sub("0","",res)
            res = removeDuplicates(res)
            res = res + "0"*(4-len(res))
            codex[word] = res[:4]
    return codex

def impSoundex(inp):
    inp = Preprocess(inp)
    inp = ApplyRules(inp)
    res = Soundex(inp)
    return res

def spellCorrectorforSound(inp):
    inp = impSoundex(inp)
    f = open("dumped.pkl", "rb")
    vocab = pickle.load(f)
    f.close()
    lookup = {}
    store = set(inp)
    for word1 in store:
        if(word1 not in vocab):
            li = []
            for i in vocab:
                if(inp[word1] == vocab[i]):
                    li.append(i)
            lookup[word1] = li
    if(lookup=={}):
        return "No correction needed"

    results = {}
    min = sys.maxsize
    for word in lookup:
        editdist = {}
        for i,tok in enumerate(lookup[word]):
            res = editDistance(tok,word,len(tok),len(word))
            if(res not in editdist):
                editdist[res] = [tok]
            else:
                editdist[res].append(tok)
            if(res<min): min = res
        results[word] = editdist[min]

    return results

def SR(duration=10, filename=None):
    # initialize the recognizer
    r = sr.Recognizer()
    print("Please talk")
    if(filename!=None):
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    else:
        with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=duration)
            print("Recognizing...")
            try:
                text = r.recognize_google(audio_data)
                return text
            except:
                return "No Human Voice Detected"

def TASKS(file):

    print("PRESS 1 TO CORRECT A SPEECH")
    print("PRESS 2 TO CORRECT .wav file")
    print("PRESS 3 TO CORRECT WRITTEN TRANSCRIPT FILE")

    userdata = input()

    if(userdata=='1'):
        print("Please say the line you want to correct:")
        res = SR().upper()
        print("Transcript:", res)
        res = spellCorrectorforSound(res)
        return res

    elif(userdata=='2'):
        if(file==None):
            print("Please pass the wav file whose transcript, you want to correct with extension in arguement:")
            return

        res = SR(filename=file).upper()
        print("Your Transcipt:",res)
        res = spellCorrectorforSound(res)
        return res

    elif(userdata=='3'):
        print("Provide the transcript you want to correct:")
        inp = input().upper()
        return spellCorrectorforSound(inp)

    else:
        return "wrong input"

while(1):
    t = TASKS(file=None)     #you can assign (.wav) file here, if you want to correct transcription of a (.wav) file
    print(t)