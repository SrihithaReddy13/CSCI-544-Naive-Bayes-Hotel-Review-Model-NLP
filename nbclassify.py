import os
import glob
import sys
import re
import string
import json
import math

test_data = []
test_data_paths = []
test_predictions = []

if len(sys.argv)==1:
    directory = '../development data'
else:
    directory = sys.argv[1]
remove = ",.'-()/"
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
							path = os.path.join(directory, class1, class2, fold, file)
							test_data_paths.append(path)
							txt = open(path).read()
							txt = re.sub(pattern, "", txt)
							txt = txt.lower()
							txt = txt.split()
							txt = [i for i in txt if i not in stop_words]
							txt = [re.sub('(ing|ed|al)$', '', w) for w in txt]
							txt = [i for i in txt if i.isalpha()]
							test_data.append(txt)
				     
with open('nbmodel.txt', 'r') as infile:
    data = infile.read()
    new_data = data.replace('}{', '},{')
    json_data = json.loads(f'[{new_data}]')
    #print(json_data)
    prior_prob = json_data[0]
    likelihood_prob = json_data[1]
    
f = open('nboutput.txt','w')

for i in range(len(test_data)):
	#print(i)
	predictions=[]
	#print(test_data[i])
	for j in ['00','01','10','11']:
		prediction = 0
		#print("j ", j)
		for word in test_data[i]:
			if word in likelihood_prob[j]:
				prediction+=math.log(likelihood_prob[j][word])
		prediction+=math.log(prior_prob[j])
		#print(prediction,past)
		predictions.append(prediction)
	#print("--",predictions)
	prediction=max(predictions)
	if prediction == predictions[3]:		
		f.write("truthful positive ")
		f.write(test_data_paths[i])
		f.write("\n")
	elif prediction == predictions[2]:		
		f.write("deceptive positive ")
		f.write(test_data_paths[i])
		f.write("\n")
	elif prediction == predictions[1]:		
		f.write("truthful negative ")
		f.write(test_data_paths[i])
		f.write("\n")
	elif prediction == predictions[0]:		
		f.write("deceptive negative ")
		f.write(test_data_paths[i])
		f.write("\n")


f.close()