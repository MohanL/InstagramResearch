import sys,time
import re
import enchant #for checking english words in the old version
import csv
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

class parseDrug:    
    def __init__(self,input):
        self.text = {}
        self.tag = {}
        self.raw = str(input)
	self.out = "out.txt"
	self.noiselist = ['""']
	self.tagFile = "tag.csv"
	self.textFile = "text.csv"
	self.wnl = WordNetLemmatizer()
 
    def constructDic(self):
	# construct the noiselist from the dailywords.txt
	ny = open('dailywords.txt','r')
	for line in ny:
		self.noiselist.append(self.word(line))	
	print self.noiselist
        f = open(self.raw, 'r')
	count = 0
        for line in f:
	    count += 1
#            print count,
	    list = line.split('\\')
	    self.tagDict(list[1])
            self.textDict(list[2])
            print count,
            self.carriage_return()
            time.sleep(0.1)
	self.deleteNoise()
	f.close()
	
    def	tagDict(self,input):
	list = input.split()
        count= 0
	for var in list:	
#		print var,
		e = self.word(var)
#		print e,
		if re.match("^[A-Za-z]*$", e):
			e = e.lower()
			e = SnowballStemmer("english").stem(e) 
#			print e
			if e not in self.noiselist:
				self.tag[e] = 0
			count+=1	
#		else:
#			self.checkTagEmoji(var)
#		print "\n"
#	print count,
#	print len(self.tag),
    def	textDict(self,input):
#	print "text"
	list = input.split()
	count = 0
        for var in list:
#		print var,
		e = self.word(var)
#		print e,
		if re.match("^[A-Za-z]*$", e):
			e = e.lower()  
			e = SnowballStemmer("english").stem(e) 
#			print e
			if e not in self.noiselist:
				self.text[e] = 0
			count+=1
		#else:
		#	self.checkTextEmoji(var)
#	print count
#	print len(self.text)

    def vectorization(self):
	f = open(self.raw, 'r')
	vec = open(self.out,'w')
	tagw = open ("tagv.csv",'w')
	textw = open ("textv.csv",'w')
	count = 0 
	for line in f:
		self.cleanVector() #what does cleanVector do ? 
		count += 1
		list = line.split('\\')	
		vec.write(list[0])
		vec.write('\\')
		taglist = self.tagVectorization(list[1])
		vec.write(",".join(str(v) for v in taglist))
		vec.write('\\')
		textlist = self.textVectorization(list[2])
		vec.write(",".join(str(v) for v in textlist))
		vec.write('\\')
		vec.write(list[3])
		tagw.write(",".join(str(v) for v in taglist))
		tagw.write("\n")
		textw.write(",".join(str(v) for v in textlist))
		textw.write("\n")
		print count,
	    	self.carriage_return()
            	time.sleep(0.1)

    def tagVectorization(self,input): 
	inputdict = self.tag
	for var in input.split():
		e = self.word(var)
		if re.match("^[A-Za-z]*$", e):
			e = e.lower()  # convert to lower case
			# I don't think the SnowballStemmer is good enough
			e = SnowballStemmer("english").stem(e) 
			if inputdict.get(e) is not None :
				inputdict[e] += 1
		#else:
		#	self.countTagEmoji(var)
	return inputdict.values()
	
    def textVectorization(self,input):
	inputdict = self.text
	d = enchant.Dict("en_US")
	for var in input.split():
		e = self.word(var)
		if re.match("^[A-Za-z]*$", e):
			e = e.lower()  # convert to lower case
			e = SnowballStemmer("english").stem(e) 
			if inputdict.get(e) is not None :
				inputdict[e] += 1
		#else:
		#	self.countTextEmoji(var)
	return inputdict.values()
    
    def checkTagEmoji(self,var):    
	var = unicode(var, 'utf-8')
	code = var.encode('unicode-escape')
	m1 = re.findall(r'\\U0001f...',code)
	m2 = re.findall(r'\\U00002...',code)
	if len(m1)!=0:
		for e in m1:
			self.tag[e] = 0	
	if len(m2)!=0:
		for e2 in m2:
			self.tag[e2] = 0	

    def checkTextEmoji(self,var):    
	var = unicode(var, 'utf-8')
	code = var.encode('unicode-escape')
	m1 = re.findall(r'\\U0001f...',code)
	m2 = re.findall(r'\\U00002...',code)
	if len(m1)!=0:
		for e in m1:
			self.text[e] = 0	
	if len(m2)!=0:
		for e2 in m2:
			self.text[e2] = 0
	
    def countTagEmoji(self,var):    
	var = unicode(var, 'utf-8')
	code = var.encode('unicode-escape')
	m1 = re.findall(r'\\U0001f...',code)
	m2 = re.findall(r'\\U00002...',code)
	if len(m1)!=0:
		for e in m1:
			self.tag[e] = 1	
	if len(m2)!=0:
		for e2 in m2:
			self.tag[e2] = 1	

    def countTextEmoji(self,var):    
	var = unicode(var, 'utf-8')
	code = var.encode('unicode-escape')
	m1 = re.findall(r'\\U0001f...',code)
	m2 = re.findall(r'\\U00002...',code)
	if len(m1)!=0:
		for e in m1:
			self.text[e] = 1	
	if len(m2)!=0:
		for e2 in m2:
			self.text[e2] = 1	

    def dictWrite(self):
	writer = csv.writer(open(self.tagFile, 'wb'))
	for key, value in self.tag.items():
   		writer.writerow([key])
	
	writer2 = csv.writer(open(self.textFile, 'wb'))
	for key, value in self.text.items():
   		writer2.writerow([key])
	
	#readback for future reference 
	# reader = csv.reader(open('dict.csv', 'rb'))
	# mydict = dict(reader)
    
    # make sure the inital count is 0
    def cleanVector(self):
	for var in self.tag:
		self.tag[var] = 0;
	for var in self.text:
		self.text[var] = 0;

    def deleteNoise(self):
	for var in self.noiselist:
		if self.tag.get(var):
			del self.tag[var]
		if self.text.get(var):
			del self.text[var]

    def carriage_return(self):
    	sys.stdout.write('\r')
    	sys.stdout.flush()

    # this function would get rid of the starting symbols and ending dots.
    def word(self, rinput):
	input = rinput
	if(input.startswith("\'")):
		input = input.lstrip("\'")
	if(input.startswith("\"")):
		input = input.lstrip("\"")
	if(input.endswith(".")):
		input = input.rstrip(".")
	if(input.endswith(',')):
		input = input.rstrip(',')
	if(input.endswith("\'")):
		input = input.rstrip("\'")
	if(input.endswith("\"")):
		input = input.rstrip("\"")
	if(input.startswith("\t")):
		input = input.lstrip("\t")
	if(input.startswith("#")):
		input = input.lstrip("#")
	if(input.endswith("#")):
		input = input.rstrip("#")
	if(input.endswith("\n")):
		input = input.rstrip('\n')
	return input

p = parseDrug(str(sys.argv[1]))
p.constructDic()
p.vectorization()
p.dictWrite()
