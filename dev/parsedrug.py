import sys,time
import re
import enchant #for checking english words in the old version
import csv
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

class parseDrug:    
    def __init__(self,input):
        self.text = {}
        self.dtext = {}
        self.ndtext = {}
        
	self.tag = {}
        self.dtag = {}
        self.ndtag = {}
        
	self.raw = str(input)
	
	self.out = "out.txt"	# this is a mixed file with drug related and non-drug related records
	self.dout = "dout.txt"	# drug related
	self.ndout = "ndout.txt" # non-drug related
	
	self.noiselist = ['""']
	
	self.tagFile = "tag.csv" 
	self.dtagFile = "dtag.csv" 
	self.ndtagFile = "ndtag.csv" 
	
	self.textFile = "dtext.csv"
	self.dtextFile = "dtext.csv"
	self.ndtextFile = "ndtext.csv"
#	self.wnl = WordNetLemmatizer()
 
    def constructDic(self):
	# construct the noiselist from the dailywords.txt
	ny = open('dailywords.txt','r')
	for line in ny:
		self.noiselist.append(self.word(line))	
#	print self.noiselist
        f = open(self.raw, 'r')
	count = 0
        for line in f:
	    count += 1
#            print count,
	    list = line.split('\\')
	    self.tagDict(list[1],list[3])
            self.textDict(list[2],list[3])
            print count,
            self.carriage_return()
            time.sleep(0.1)
#	self.deleteNoise()
	f.close()
	
    def	tagDict(self,input,input2): # input is the list of tags, input2 is the label
	list = input.split()
        count= 0
	label = int(input2)
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
				if label == 1:
					self.dtag[e] = 0
				else:
					self.ndtag[e] = 0
			count+=1	
#		else:
#			self.checkTagEmoji(var)
#		print "\n"
#	print count,
#	print len(self.tag),
    def	textDict(self,input,input2):
#	print "text"
	list = input.split()
	count = 0
       	label = int(input2)
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
				if label == 1:
					self.dtag[e] = 0
				else:
					self.ndtag[e] = 0
			count+=1
		#else:
		#	self.checkTextEmoji(var)
#	print count
#	print len(self.text)


    def vectorization(self):
	# out files are for the vectorization
	f = open(self.raw, 'r')
	vec = open(self.out,'w')
	dvec = open(self.dout,'w')
	ndvec = open(self.ndout,'w')

	# v files are for storing vectorization and used to computer the frequency values
	tagw = open ("tagv.csv",'w')
	dtagw = open ("dtagv.csv",'w')
	ndtagw = open ("ndtagv.csv",'w')

	textw = open ("textv.csv",'w')
	dtextw = open ("dtextv.csv",'w')
	ndtextw = open ("ndtextv.csv",'w')

	count = 0 
	for line in f:
		self.cleanVector() #what does cleanVector do ? 
		count += 1
		list = line.split('\\')	
		vec.write(list[0])
		vec.write('\\')
		label = int(list[3])
		taglist = self.tagVectorization(list[1])
		vec.write(",".join(str(v) for v in taglist))
		vec.write('\\')
		textlist = self.textVectorization(list[2])
		vec.write(",".join(str(v) for v in textlist))
		vec.write('\\')
		vec.write(list[3])
		if label == 1:
			dvec.write(list[0])
			dvec.write('\\')
			dvec.write(",".join(str(v) for v in self.dtag.values()))
 	                dvec.write('\\')
			dvec.write(",".join(str(v) for v in self.dtext.values()))
	                dvec.write('\\')
			dvec.write(list[3])
		else:
			ndvec.write(list[0])
			ndvec.write('\\')
			ndvec.write(",".join(str(v) for v in self.ndtag.values()))
 	                ndvec.write('\\')
			ndvec.write(",".join(str(v) for v in self.ndtext.values()))
	                ndvec.write('\\')
			ndvec.write(list[3])

		tagw.write(",".join(str(v) for v in taglist))
		tagw.write("\n")
		textw.write(",".join(str(v) for v in textlist))
		textw.write("\n")
		if label == 1:
			dtagw.write(",".join(str(v) for v in self.dtag.values()))
			dtagw.write("\n")
			dtextw.write(",".join(str(v) for v in self.dtext.values()))
			dtextw.write("\n")
		else:
			ndtagw.write(",".join(str(v) for v in self.ndtag.values()))
			ndtagw.write("\n")
			ndtextw.write(",".join(str(v) for v in self.ndtext.values()))
			ndtextw.write("\n")
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
			if self.dtag.get(e) is not None:
				self.dtag[e] += 1
			if self.ndtag.get(e) is not None:
				self.ndtag[e] += 1
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
			if self.dtext.get(e) is not None:
				self.dtext[e] += 1
			if self.ndtext.get(e) is not None:
				self.ndtext[e] += 1
		#else:
		#	self.countTextEmoji(var)
	return inputdict.values()
    
#    def checkTagEmoji(self,var):    
#	var = unicode(var, 'utf-8')
#	code = var.encode('unicode-escape')
#	m1 = re.findall(r'\\U0001f...',code)
#	m2 = re.findall(r'\\U00002...',code)
#	if len(m1)!=0:
#		for e in m1:
#			self.tag[e] = 0	
#	if len(m2)!=0:
#		for e2 in m2:
#			self.tag[e2] = 0	
#
#    def checkTextEmoji(self,var):    
#	var = unicode(var, 'utf-8')
#	code = var.encode('unicode-escape')
#	m1 = re.findall(r'\\U0001f...',code)
#	m2 = re.findall(r'\\U00002...',code)
#	if len(m1)!=0:
#		for e in m1:
#			self.text[e] = 0	
#	if len(m2)!=0:
#		for e2 in m2:
#			self.text[e2] = 0
#	
#    def countTagEmoji(self,var):    
#	var = unicode(var, 'utf-8')
#	code = var.encode('unicode-escape')
#	m1 = re.findall(r'\\U0001f...',code)
#	m2 = re.findall(r'\\U00002...',code)
#	if len(m1)!=0:
#		for e in m1:
#			self.tag[e] = 1	
#	if len(m2)!=0:
#		for e2 in m2:
#			self.tag[e2] = 1	
#
#    def countTextEmoji(self,var):    
#	var = unicode(var, 'utf-8')
#	code = var.encode('unicode-escape')
#	m1 = re.findall(r'\\U0001f...',code)
#	m2 = re.findall(r'\\U00002...',code)
#	if len(m1)!=0:
#		for e in m1:
#			self.text[e] = 1	
#	if len(m2)!=0:
#		for e2 in m2:
#			self.text[e2] = 1	

    def dictWrite(self):
	writer = csv.writer(open(self.tagFile, 'wb'))
	for key, value in self.tag.items():
   		writer.writerow([key])

	writer = csv.writer(open(self.dtagFile, 'wb'))
	for key, value in self.dtag.items():
   		writer.writerow([key])

	writer = csv.writer(open(self.ndtagFile, 'wb'))
	for key, value in self.ndtag.items():
   		writer.writerow([key])

	writer2 = csv.writer(open(self.textFile, 'wb'))
	for key, value in self.text.items():
   		writer2.writerow([key])

	writer2 = csv.writer(open(self.dtextFile, 'wb'))
	for key, value in self.dtext.items():
   		writer2.writerow([key])

	writer2 = csv.writer(open(self.ndtextFile, 'wb'))
	for key, value in self.ndtext.items():
   		writer2.writerow([key])
	
	#readback for future reference 
	# reader = csv.reader(open('dict.csv', 'rb'))
	# mydict = dict(reader)
    
    # make sure the inital count is 0
    def cleanVector(self):
	for var in self.tag:
		self.tag[var] = 0;
	for var in self.dtag:
		self.dtag[var] = 0;
	for var in self.ndtag:
		self.ndtag[var] = 0;
	for var in self.text:
		self.text[var] = 0;
	for var in self.dtext:
		self.dtext[var] = 0;
	for var in self.ndtext:
		self.ndtext[var] = 0;

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

    # calculate the word frequency	
    def tagf(self):
	f = open("tagv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("tagf.txt",'w')
	s.write("\n".join(str(v) for v in a))

	f = open("dtagv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("dtagf.txt",'w')
	s.write("\n".join(str(v) for v in a))

	f = open("ndtagv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("ndtagf.txt",'w')
	s.write("\n".join(str(v) for v in a))

    def textf(self): 
	f = open("textv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("textf.txt",'w')
	s.write("\n".join(str(v) for v in a))

	f = open("dtextv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("dtextf.txt",'w')
	s.write("\n".join(str(v) for v in a))
	
	f = open("ndtextv.csv",'r')
	count = 0
	for line in f:
		sum = 0
		li = line.split(',')
		a = [0] * len(li)
	f.seek(0)
	for line in f:
		li = line.split(',')
		for i in range(0,len(li)):
			a[i] = a[i]+int(li[i])
	s = open("ndtextf.txt",'w')
	s.write("\n".join(str(v) for v in a))


p = parseDrug(str(sys.argv[1]))
p.constructDic()
p.vectorization()
p.dictWrite()
#p.tagf()
#p.textf()
