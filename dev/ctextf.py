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
