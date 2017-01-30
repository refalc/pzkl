import nltk
import codecs
import pymorphy2
import os
from pymystem3 import Mystem
from nltk.tokenize import sent_tokenize, word_tokenize
mystem = Mystem(entire_input=False)
list_of_file = os.listdir('../Data/TextData')
i = 0
fileObjs = []
KeyFile = codecs.open( "../Data/Key/keys.txt", "r", "utf_8_sig" )
for file in list_of_file:
    ffile = '../Data/TextData/' + file
    fileObjs.insert(i, codecs.open( ffile, "r", "utf_8_sig" ))
    i+=1

print(list_of_file)
keys = KeyFile.read().splitlines()
print(keys)
morph = pymorphy2.MorphAnalyzer()
i = 0
sentence_id = 136
out_file = codecs.open( "../Data/Key/answer2.txt", "w", "utf_8_sig" )
for obj in fileObjs: 
    print("Start text #", i)
    i+=1
    magic = []
    number_of_word = 0
    size_of_word = 0
    punkt = 0
    text = obj.read() # или читайте по строке
    s = sent_tokenize(text)
    
    all_impad_num = 0
    all_infinitive = 0
    all_worlds_before_impad = 0
    sent_num = 1
    for sent in s:
        key_word = 0
        past_verb_in_sent = 0
        out_text = "Sentence = " + str(sent_num) + "/" + str(len(s))
        print(out_text)
        words_before_verb = 0
        find = False
        morph_data = mystem.analyze(sent)
        for w_data in morph_data:
            #print(w_data)
            if w_data["text"].lower() in keys :
                key_word = 1
            if len(w_data["analysis"]) > 0 :
                #print(w_data["text"].lower())
                if ((w_data["analysis"][0]["gr"].find('V,', 0, 2) > -1) and (w_data["analysis"][0]["gr"].find('пе=прош') > -1)):
                    past_verb_in_sent += 1
                    find = True

            if not(find) :
                words_before_verb += 1

        #out_text = "\tFirst position of pastV = " + str(words_before_verb) + "\n\tAll pastV count = " + str(past_verb_in_sent)
        #print(out_text)
        out_text = "<sentence id=\"" + str(sentence_id)\
        + "\" learn_params=\"" + str(sent_num / len(s))\
        + "," + str(key_word) + "," + str(past_verb_in_sent)\
        + "," + str(words_before_verb) + "\"" + " class =\"\">" + sent + "</sentence>\r\n"
            
        print(out_text)
        out_file.write(out_text)
        out_file.flush()
        sentence_id += 1
        sent_num += 1