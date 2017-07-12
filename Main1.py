'''
Created on Mar 21, 2017

@author: sangeeta
'''

def trainMNB(classList,trainingSet):
    count=1
    vocabulary = list()
    totalDocs = 0
    countDocsInClass = list()
    priorList = list()
    textOfEachClass = list() 
    lines = ""
    #print("DBG pt 1")
    for name in sorted(os.listdir(trainingSet)):
        # print("DBG pt 2")
        if (os.path.isdir(os.path.join(trainingSet,name)) and count<=len(classList)):
            localDocs = 0
            testCls = ""
            for fileList in os.listdir(os.path.join(trainingSet,name)):
                #print("DBG pt 3")
                totalDocs+=1
                localDocs+=1
                f = open(os.path.join(trainingSet,name,fileList))
                #lines = lines +" ".join(f.readlines())
                readFileOfClass=""
                readFileOfClass = re.sub(r'[<|>|?|_|,|!|:|;|(|)|\"|=|-|$|\\|/|*|\'|+|\[|\]|#|$|%|^|?|~|`]', r'', str(f.readlines()))
                testCls = testCls+" "+readFileOfClass
                #lines=lines+testCls
            #newtestCls  = re.sub(r'[<|>|?|_|,|!|:|;|(|)|"|=|-|$|\\|/]', r'', testCls)
            vocabulary.extend(testCls.split())
            textOfEachClass.append(testCls)
            countDocsInClass.append(localDocs)
            count+=1
    #newLines  = re.sub(r'[<|>|?|_|,|!|:|;|(|)|"|=|-|$|\\|/]', r'', lines)
    #print("DBG pt 4")
    #for word in newLines.split():
    #    vocabulary.append(word)
    vocabulary = set(vocabulary)
    #print("DBG pt 5")
    #print(vocabulary)
    i = 0
    condProbOfClass =list()
    
    for className in classList:
        Tct = list()
        condProbOfTerm = defaultdict(list)
        priorList.append(countDocsInClass[i]/totalDocs)
        counterText = Counter(textOfEachClass[i].split())
        for term in vocabulary:
            #print("DBG pt 8")
            Tct.append(counterText[term])
        j=0
        TctSum = sum(Tct)
        lenTct = len(Tct)
        for term in vocabulary:
            condProbOfTerm[term].append((Tct[j]+1)/(TctSum+lenTct))
            j+=1
        condProbOfClass.append(condProbOfTerm)
        i+=1
    return vocabulary, priorList, condProbOfClass    
    
def applyMNB(classList, vocabulary, prior, condProbOfClass, document, testSet):
    wVocabulary = list()
    score = list()
    #print("Entered apply MNB")
    f = open(os.path.join(testSet,name,document))
    tokensStr  = " ".join(f.readlines())
    #print(tokensStr)
    tokenList  = re.sub(r'[<|>|?|_|,|!|:|;|(|)|\"|=|-|$|\\|/|*|\'|+|\[|\]|#|$|%|^|?|~|`]', r'', tokensStr)
    for word in tokenList.split():
        wVocabulary.append(word)
    wVocabulary = set(wVocabulary)
    m = 0
    for className in classList:
        score.append(math.log(prior[m]))
        for term in wVocabulary:
            if not condProbOfClass[m][term]:
                continue;
            score[m]+=math.log(condProbOfClass[m][term][0])
        m+=1
    score = np.array(score)
    #print(np.argmax(score))
    return np.argmax(score)
    
    

trainingSet = sys.argv[1]
testSet = sys.argv[2]

classList = list()

dirname2 = os.path.split(trainingSet)[1]
count = 1
folders =8
for name in sorted(os.listdir(trainingSet)):
    if (os.path.isdir(os.path.join(trainingSet,name)) and count<=folders):
        classList.append(name)
        print(name)
        count+=1

count =1
vocabulary, priorList, condProbOfClass = trainMNB(classList,trainingSet)
success = 0
failure = 0
for name in sorted(os.listdir(testSet)):
    if (os.path.isdir(os.path.join(testSet,name)) and count<=folders):
        for doc in os.listdir(os.path.join(testSet,name)):
            folderPred = applyMNB(classList,vocabulary, priorList, condProbOfClass, doc, testSet)
            if (classList[folderPred]==name):
                success+=1
            else:
                #print(str(classList[folderPred])+" "+str(name))
                failure+=1
    count+=1
#print("Success : "+str(success))
#print("Failure : "+str(failure))
print("Accuracy : "+str(success/(success+failure)))




