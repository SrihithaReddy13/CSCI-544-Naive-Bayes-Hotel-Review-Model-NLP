import os
import glob
import sys
import re
import string
import json 

train_data = []
train_results=[]
class_count = {'00':0,'01':0,'10':0,'11':0}

if len(sys.argv)==1:
    directory = '../training data'
else:
    directory = sys.argv[1]
remove =  ",.'-()/"
pattern = r"[{}]".format(remove)
stop_words = {'and', 'down', 'it', 'of', 'will', 'than', 'all', 'ourselves', 'did', 'most', 'being',
'was', 'on', 'were', 'him', 'such', 'which', 'this', 'at', 'himself', 'for', 'yourself', 'have', 'until', 'be', 'why', 'he', 'during', 'now', 'very', 'myself', 'having', 'your', 'these', 'we', 'with', 'its', 'doing', 'only', 'then', 'both', 'me', 'because', 'after', 'to', 'she', 'between', 'theirs', 'before', 'is', 'ours', 'does', 'pm', 'has', 'can', 'yours', 'other', 'a', 'where', 'from', 'out', 'some', 'hers', 'if', 'by', 'just', 'had', 'they', 'under', 'itself', 'how', 'so', 'the', 'again', 'each', 'yourselves', 'but', 'up', 'are', 'when', 'them', 'you', 'further', 'there', 'her', 'own', 'that', 'who', 'few', 'his', 'any', 'below', 'themselves', 'once', 'or', 'been', 'off', 'above', 'about', 'here', 'should', 'herself', 'an', 'same', 'into', 'more', 'whom', 'my', 'through', 'do', 'those', 'against', 'over', 'while', 'our', 'their', 'in', 'am', 'as', 'what'}

temp_path = os.path.join(directory)
for class1 in os.listdir(temp_path):
    temp_path = os.path.join(directory, class1)
    if os.path.isdir(temp_path): 
        for class2 in os.listdir(temp_path):
            temp_path = os.path.join(directory, class1, class2)
            if os.path.isdir(temp_path):
                for fold in os.listdir(temp_path):
                    temp_path = os.path.join(directory, class1, class2, fold)
                    if os.path.isdir(temp_path):
                        for file in os.listdir(temp_path):
                            txt = open(os.path.join(directory, class1, class2, fold, file)).read()
                            txt = re.sub(pattern, "", txt)
                            txt = txt.lower()
                            txt = txt.split()
                            txt = [i for i in txt if i not in stop_words]
                            txt = [re.sub('(ing|ed|al)$', '', w) for w in txt]
                            txt = [i for i in txt if i.isalpha()]
                            #print(txt)
                            train_data.append(txt)
                            if class1 == 'negative_polarity':
                                if class2 == 'deceptive_from_MTurk':
                                    train_results.append('00')
                                    class_count['00']+=1
                                else:
                                    train_results.append('01')
                                    class_count['01']+=1
                            else:
                                if class2 == 'deceptive_from_MTurk':
                                    train_results.append('10')
                                    class_count['10']+=1
                                else:
                                    train_results.append('11')
                                    class_count['11']+=1

total = sum(class_count.values())
prior_prob= {}
for i in class_count:
    prior_prob[i] = class_count[i]/total

f = open("nbmodel.txt","w")
f.write(json.dumps(prior_prob, indent=4))

word_bag = set()
likelihood_count = {'00':{},'01':{},'10':{},'11':{}} #count of word w in class c
likelihood_prob = {'00':{},'01':{},'10':{},'11':{}} #smoothened probability

for i in range(total):
    for word in train_data[i]:
        if word in likelihood_count[train_results[i]]:
            likelihood_count[train_results[i]][word]+=1
        else:
            likelihood_count[train_results[i]][word]=1


for j in ['00','01','10','11']:
    for i in list(likelihood_count[j]):
        if likelihood_count[j][i]<2:
            del likelihood_count[j][i]
        else:
            word_bag.add(i)

alpha = 2
for i in word_bag:
    for j in ['00','01','10','11']:
        if i in likelihood_count[j]:
            likelihood_prob[j][i] = (alpha+likelihood_count[j][i])/(sum(likelihood_count[j].values())+alpha*len(word_bag))
        else:
            likelihood_prob[j][i] = alpha/(sum(likelihood_count[j].values())+alpha*len(word_bag))

#print(likelihood_count)

f.write(json.dumps(likelihood_prob, indent=4))
f.close()