import nltk
import codecs
import pymorphy2
import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn import linear_model, datasets
from sklearn import svm
list_of_file = os.listdir('../Data/TextData')
i = 0
fileObjs = []

for file in list_of_file:
    ffile = '../Data/TextData/' + file
    fileObjs.insert(i, codecs.open( ffile, "r", "utf_8_sig" ))
    i+=1

main_file = codecs.open( '../Data/Key/test1.txt', "r", "utf_8_sig" )
items = main_file.read().splitlines()
X_train = []
Y_train= []
X_test = []
Y_test= []
i = 0
last_i = 75
for item in items :
    params = re.search( r'learn_params="(.*?)"', item, re.M)
    pars = re.match( r'(.*),(.*),(.*),(.*)', params.group(1), re.M|re.I)
    temp = []
    temp.append(float(pars.group(1)))
    temp.append(float(pars.group(2)))
    temp.append(float(pars.group(3)))
    temp.append(float(pars.group(4)))
    metka = re.search( r'class ="(.*?)"', item, re.M)
    
    if i < last_i :
        X_train.append(temp)
        Y_train.append(float(metka.group(1)))  
    else :
        X_test.append(temp)
        Y_test.append(float(metka.group(1)))
    i += 1
    
logreg = linear_model.LogisticRegression(C=10)
logreg.fit(X_train, Y_train)
clf = svm.SVC()
clf.fit(X_train, Y_train) 
Y_predict = logreg.predict(X_test)
#Y_predict = clf.predict(X_test)
print(Y_predict)
print(Y_test)

hit = 0
i = 0
class_1_hit = 0
class_1 = 0
false_class_1_hit = 0
for elem in Y_predict :
    if Y_test[i] == 1 :
        class_1 += 1
        if elem == 1 :
            class_1_hit += 1
    else :
        if elem == 1 :
            false_class_1_hit += 1
    
    if Y_test[i] == elem :
        hit += 1
    i += 1

print(hit / len(Y_test))
print(class_1_hit / class_1)
print(false_class_1_hit / (len(Y_test) - class_1_hit))
    