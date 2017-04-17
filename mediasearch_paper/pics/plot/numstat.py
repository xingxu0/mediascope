f=open('numstat')
a={}
for i in range(300):
	a[i] = 0
for line in f:
	a[int(line)] += 1
	
ff = open('num')
for i in range(300):
	f.write(str(i)+" "+str(a[i]))
ff.close()
f.close()