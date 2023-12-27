
import numpy
import matplotlib

def loadBook(filename):
    lst=[]
    f = open(filename, "r")
    lines=f.readlines()
    for i in lines:
        if ('\n') in i:
            new=i.replace('\n', "")
        else:
            new=i
        data = new.split(' ')
        if data != [""] and data !=[]:
            lst.append(data)        
    return lst

def getCorpusLength(corpus):
    count=sum([len(elem) for elem in corpus])
    return count

def buildVocabulary(corpus):
    newlst=[]
    for lst in corpus:
        for elem in lst:
            if elem not in newlst:
                newlst.append(elem)
              
    return newlst


def makeStartCorpus(corpus):
    first=[]
    for i in corpus:
        first.append([i[0]])
    return first
        
def countUnigrams(corpus):
    d={}
    for list in corpus:
        for innerList in list:
            if innerList not in d:
                d[innerList]=0
            d[innerList]+=1
 
    return d

def countBigrams(corpus):
    d={}
    for key in corpus:
        for index in range(len(key)-1):
            if key[index] not in d:
                d[key[index]]={}
            if key[index+1] not in d[key[index]]:
                d[key[index]][key[index+1]]=1
            else:
                key[index+1] in d[key[index]]
                d[key[index]][key[index+1]]+=1
                     
    return d

import string

def separateWords(line):
    lst=[]
    words = line.split(' ')
    punct = '''!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"'''
    for word in words:
        oldindex=0
        index=0
        hasPunct = False
        for char in word:
            if char in punct:
                hasPunct = True
                if(word[oldindex:index] != ''):
                    lst.append(word[oldindex:index].strip())
                lst.append(word[index].strip())
                oldindex=index+1
            index+=1
        if(word[-1] not in punct and hasPunct):
            lst.append(word[oldindex:].strip())
        if(not hasPunct):
            lst.append(word.strip())
    return lst


def cleanBookData(text):
    lower = text.lower()
    words = separateWords(lower)
    string = ""
    newline = ['!', '.', '?']
    for i in words:
        string+=i
        if i in newline:
            string+='\n'
        else:
            string+=" "
    return string.strip()


def buildUniformProbs(unigrams):
    lst=[]
    total = len(unigrams)
    for i in range(len(unigrams)):
        lst.append(1/total)
    return lst
                   

def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    lst = []
    for i in range(len(unigrams)):
        uniCount = unigramCounts[unigrams[i]]
        prob = uniCount/totalCount
        lst.append(prob)
    return lst

def buildBigramProbs(unigramCounts, bigramCounts):
    dict = {}
    for prevWord in bigramCounts:
        words = []
        probs = []
        for key in bigramCounts[prevWord]:
            words.append(key)
            probs.append(bigramCounts[prevWord][key]/unigramCounts[prevWord])
            tempDict={}
            tempDict["words"]=words
            tempDict["probs"]=probs
        dict[prevWord]=tempDict
    return dict
            
def getTopWords(count, words, probs, ignoreList):
    d = {}
    for i in range(count):
        maxprob = 0
        maxword = ""
        for ind in range(len(words)):
            if(words[ind] not in ignoreList and words[ind] not in d.keys()):
                if(probs[ind] > maxprob):
                    maxprob = probs[ind]
                    maxword = words[ind]
        d[maxword] = maxprob
    return d
                
from random import choices
def generateTextFromUnigrams(count, words, probs):
    sentence = ""
    for i in range(count):
        word = choices(words, weights = probs)[0]
        sentence+=f"{word} "
    return sentence.strip()


def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    sentence = ""
    lastWord = ""
    for i in range(count):
        if(lastWord in ["?", ".", "!", ""]):
            word = choices(startWords, startWordProbs)[0]
            sentence += f"{word} "
        else:
            gen = bigramProbs[lastWord]
            word = choices(gen["words"], gen["probs"])[0]
            sentence += f"{word} "
        lastWord = word
    return sentence.strip()


ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]


def graphTop50Words(corpus):
    totalwords = []
    for l in corpus:
        totalwords.extend(l)
    dictionaryCountUnigrams = countUnigrams(corpus)
    probs = buildUnigramProbs(list(dictionaryCountUnigrams.keys()), dictionaryCountUnigrams, len(totalwords))
    top50 = getTopWords(50, list(dictionaryCountUnigrams.keys()), probs, ignore)
    barPlot(top50, "Top 50 Words")
    return


def graphTopStartWords(corpus):
    startCorpus = makeStartCorpus(corpus)
    totalwords = []
    for l in startCorpus:
        totalwords.extend(l)
    dictionaryCountUnigrams = countUnigrams(startCorpus)
    probs = buildUnigramProbs(list(dictionaryCountUnigrams.keys()), dictionaryCountUnigrams, len(totalwords))
    top50 = getTopWords(50, list(dictionaryCountUnigrams.keys()), probs, ignore)
    barPlot(top50, "Top 50 Start Words")
    return


def graphTopNextWords(corpus, word):
    bigramDict = countBigrams(corpus)
    unigramDict = countUnigrams(corpus)
    bigramProbs = buildBigramProbs(unigramDict, bigramDict)
    listWords = []
    listProbs = []
    listWords.extend(bigramProbs[word]["words"])
    listProbs.extend(bigramProbs[word]["probs"])
    top10 = getTopWords(10, listWords, listProbs, ignore)
    barPlot(top10, "Top 10 Next Words")
    return


def setupChartData(corpus1, corpus2, topWordCount):
    totalwords1 = []
    for l in corpus1:
        totalwords1.extend(l)
    totalwords2 = []
    for l in corpus2:
        totalwords2.extend(l)
    corpus1UnigramProb = buildUnigramProbs(totalwords1, countUnigrams(corpus1), len(totalwords1))
    corpus2UnigramProb = buildUnigramProbs(totalwords2, countUnigrams(corpus2), len(totalwords2))
    completeList = []
    one = (getTopWords(topWordCount, totalwords1, corpus1UnigramProb, ignore))
    two = (getTopWords(topWordCount, totalwords2, corpus2UnigramProb, ignore))
    for word in one:
        if(word not in completeList):
            completeList.append(word)
    for word in two:
        if word not in completeList:
            completeList.append(word)
    corpus1prob = []
    corpus2prob = []
    for w in completeList:
        if w in totalwords1:
            corpus1prob.append(corpus1UnigramProb[totalwords1.index(w)])
        else:
            corpus1prob.append(0)
        if w in totalwords2:
            corpus2prob.append(corpus2UnigramProb[totalwords2.index(w)])
        else:
            corpus2prob.append(0)
    rdict = {}
    rdict["topWords"] = completeList
    rdict["corpus1Probs"] = corpus1prob
    rdict["corpus2Probs"] = corpus2prob
    return rdict

def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    dic = setupChartData(corpus1, corpus2, numWords)
    sideBySideBarPlots(dic["topWords"], dic["corpus1Probs"], dic["corpus2Probs"], name1, name2, title)
    return

def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    dic = setupChartData(corpus1, corpus2, numWords)
    scatterPlot(dic["corpus1Probs"], dic["corpus2Probs"], dic["topWords"], title)
    return


def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()


def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35 

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()


def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    for i in range(len(labels)):
        plt.annotate(labels[i], 
                    (xs[i], ys[i]), 
                    textcoords="offset points", 
                    xytext=(0, 10), 
                    ha='center') 
    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()
