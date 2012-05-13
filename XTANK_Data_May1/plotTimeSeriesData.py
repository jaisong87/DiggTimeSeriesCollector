import MySQLdb
import dbInfo
import matplotlib.pyplot as plt
import pdb
import nltk

def plotDiggDistro(minDiggs = 2,  lt1 = 10, lt2=70, lt3=120, clSize = 200):
	db = MySQLdb.connect(user = dbInfo.user, passwd = dbInfo.passwd, db = dbInfo.db)
        conn = db.cursor()
        query = "SELECT diggs FROM diggfeatures WHERE diggs > %d" % (minDiggs)
	conn.execute(query)
        data = conn.fetchall()
	conn.close()
	distro1 = []
	distro2 = []
	distro3 = []
	distro4 = []
	for row in data:
		if row[0]<lt1 and len(distro1)<clSize:
			distro1.append(row[0])
		elif row[0]>(lt1+10) and row[0]<lt2 and len(distro2)<clSize:
			distro2.append(row[0])
		elif row[0]>(lt2+20) and row[0]<lt3 and len(distro3)<clSize:
			distro3.append(row[0])
		elif row[0]>lt3+20 and len(distro4)<clSize:
			distro4.append(row[0])
	print len(distro1), len(distro2), len(distro3), len(distro4)
	plt.hist(distro1, 10, color='r')
	plt.hist(distro2, 10, color='g')
	plt.hist(distro3, 10, color='b')
	plt.hist(distro4, 10, color='y')
        query = "4-way classification [%d-%d(%d)], [%d-%d(%d)], [%d-%d(%d)], [%d-INF(%d)] " %(minDiggs, lt1, len(distro1), lt1+10, lt2, len(distro2), lt2+20, lt3, len(distro3), lt3+20, len(distro4))
	plt.title(query)
	plt.grid(True)
	plt.show()	
	plt.hist(distro1, 100, color='r', cumulative = True)
	plt.grid(True)
	plt.title("%s (CDF) " % (query) )
	plt.show()	
	
def getStories(minDiggs = 10):
	db = MySQLdb.connect(user = dbInfo.user, passwd = dbInfo.passwd, db = dbInfo.db)
        conn = db.cursor()
        query = "SELECT digg_id FROM diggfeatures WHERE diggs >= %d" % (minDiggs)
        conn.execute(query)
        data = conn.fetchall()
        distro = []
        for row in data:
                distro.append(row[0])
	return distro


def getParam(digg_id, param):
	db = MySQLdb.connect(user = dbInfo.user, passwd = dbInfo.passwd, db = dbInfo.db)
        conn = db.cursor()
	table = "diggfeatures"
	if param == 'google_pagerank' or param =='title' or param == 'description':
		table = 'diggs_storyinfo'
	elif(param == 'diggs' or param =="fofCount" or param =="authorDiggs" or param == "authorComments" or param == "authorFans" or param == "authorFollows" or param == "authorGender" or param == "authorSubmissions" ):
		table = "diggfeatures"
	elif (param == 'digg1' or param == 'digg2' or param == 'digg3' or param == 'digg4' or param == 'digg5'):
		table = "diggs"
	else:
		table = "socialdynamics"
	query = "SELECT %s FROM %s WHERE digg_id='%s'" % (param, table, digg_id)
	#print query
	conn.execute(query)
	ans = conn.fetchone()
	conn.close()
	#print "ans = ", ans
	if (ans != None):
		return ans[0]
	

def plotSocialDynamicsData(dim, minDiggs=5, th1 = 10, th2=71, th3=121):
	lt1 = th1
	lt2 = th2
	lt3 = th3
	data = getStories(minDiggs)
	diggs1 = []
	param1 = []
	diggs2 = []
	param2 = []
	diggs3 = []
	param3 = []
	diggs4 = []
	param4 = []
	for row in data:
		diggCount = getParam(row, "diggs")
		#print "Calculating for ", row ," with ", diggCount , " diggs "
		if(diggCount<lt1):
			diggs1.append(diggCount)
			param1.append(getParam(row, dim) )
		elif(diggCount<lt2):
			diggs2.append(diggCount)
			param2.append(getParam(row, dim) )
		elif(diggCount<lt3):
			diggs3.append(diggCount)
			param3.append(getParam(row, dim) )
		else:
			diggs4.append(diggCount)
			param4.append(getParam(row, dim) )
	print len(diggs1), len(param1), len(diggs2), len(param2), len(diggs3), len(param3)
	plt.xlabel(dim)
	plt.ylabel("Diggs")
	plt.title("Diggs vs %s green(<%d), blue(%d-%d), red(%d-%d) violet(%d+" % (dim, lt1, lt1, lt2, lt2, lt3, lt3))
	plt.plot(param1, diggs1, "g-")
	plt.plot(param2, diggs2, "bo")
	plt.plot(param3, diggs3, "r*")
	plt.plot(param4, diggs4, "y+")
	plt.show()
	plt.hist(param1,100, color="green", cumulative =True)
	plt.title("CDF of %s for diggs<%d" % (dim, lt1))
	plt.show()
	plt.hist(param2,100, color="blue", cumulative =True)
	plt.title("CDF of %s for diggs>%d AND diggs<%d" % (dim, lt1, lt2))
	plt.show()
	plt.hist(param3,100, color="red", cumulative =True)
	plt.title("CDF of %s for diggs>%d AND diggs<%d" % (dim, lt2, lt3))
	plt.show()
	plt.hist(param4,100, color="magenta", cumulative =True)
	plt.title("CDF of %s for diggs>%d" % (dim, lt3))
	plt.show()

def loadngram(ngram, Ngramfile):
  fp = open(Ngramfile, 'r')
  for i in fp:
    ngram.append(i.strip())
  fp.close()

def fillist(diggid, newlist, ngramlist, ngramsize):
  try:
    fp = open("Comments/" + diggid.replace(':','$'), 'r')
  except IOError:
    return
  for i in fp:
    for gram in range(1,ngramsize):
      for j in nltk.ngrams(i.split(), gram):
        if str(j) in ngramlist:
          index = ngramlist.index(str(j))
          newlist[index] += 1

def fillistpos(diggid, newlist, posngramlist, ngramsize):
  try:
    fp = open("Comments/" + diggid.replace(':','$'), 'r')
  except IOError:
    return
  for line in fp:
    i = [k[1] for k in nltk.pos_tag(line.split())] 
    for gram in range(1,ngramsize):
      for j in nltk.ngrams(i, gram):
        if str(j) in posngramlist:
          index = posngramlist.index(str(j))
          newlist[index] += 1

def makeClassificationSet(file, minDiggs = 2, clSize = 200 , paraList = ['tpc1', 'tpc2', 'upc1', 'upc2', 'digg1', 'digg2', 'authorDiggs', 'authorComments', 'authorFans', 'authorFollows', 'authorSubmissions', 'ngramComments', 'posngramComments', 'google_pagerank' ] , th1 = 11, th2 =71, th3=121, Ngramfile = "Comments/Ngramfeatures", POSNgramfile= "Comments/POSNgramfeatures", ngramsize = 5):
	lt1 = th1
	lt2 = th2
	lt3 = th3
	clA = 0
	clB = 0
	clC = 0
	clD = 0
	curClSz = clSize+1
        ngramlist = []
        posngramlist = []
        loadngram(ngramlist, Ngramfile)
        loadngram(posngramlist, POSNgramfile)
	data = getStories(minDiggs)
        fh = open(file, 'w')
	fh.write("@RELATION Digg_SocialDynamicsBasedFeatures\n")
	for para in paraList:
                if para == "ngramComments" or para == "posngramComments":
                  if para == "ngramComments":
                    for i  in range(0,len(ngramlist)):
                      spec = "@ATTRIBUTE Ngram%s  NUMERIC\n" %i
                      fh.write(spec)
                  else:
                    for i in range(0,len(posngramlist)): 
                      spec = "@ATTRIBUTE POSNgram%s  NUMERIC\n" % i
                      fh.write(spec)
                else:
		  spec = "@ATTRIBUTE %s  NUMERIC\n" % (para)
		  fh.write(spec)
	fh.write("@ATTRIBUTE class {A, B, C, D}\n")
	fh.write("@DATA\n")
	for row in data:
		diggCount = getParam(row, "diggs")
		noiseChance = 0
		cl = '-'
		curClSz = clSize+1
		if(diggCount<lt1):
			cl = 'A'
			clA +=1
			curClSz = clA
		elif diggCount<lt2 and diggCount>(lt1+10):
			cl='B'
			clB +=1
			curClSz = clB
		elif diggCount<lt3 and diggCount>(lt2+20):
			cl='C'
			clC +=1
			curClSz = clC
		elif diggCount>lt3+20:
			cl='D'
			clD +=1
			curClSz = clD
		featureVector = []
		line = ""
		for para in paraList:
                        if "ngram" in para:
                          if para == "ngramComments":
 			    newlist = [0]*len(ngramlist)
                            fillist(row, newlist, ngramlist, ngramsize)
                          else:
                            newlist = [0]*len(posngramlist)
                            fillistpos(row, newlist, posngramlist, ngramsize)
                          for i1 in newlist:
                            line += str(i1) + ','
                        else:   
			  fval = getParam(row, para)
			  if row=='upc1' and para==0:
				noiseChance = noiseChance +2
			  elif row =='upc2' and para==0:
				noiseChance = noiseChance +1
			  featureVector.append(fval)
			  line += "%d," % (fval)
		line += "%s\n" % (cl)
		
		if noiseChance < 2 and curClSz<=clSize:
			fh.write(line)
	fh.close()

def makeRegressionSet(file, paraList, th1 =71, th2=121):
	lt1 = th1
	lt2 = th2
	data = getStories()
	fh = open(file, 'w')
	fh.write("@RELATION Digg_SocialDynamicsBasedFeatures\n")
	for para in paraList:
		spec = "@ATTRIBUTE %s  NUMERIC\n" % (para)
		fh.write(spec)
	fh.write("@ATTRIBUTE class NUMERIC\n")
	fh.write("@DATA\n")
	for row in data:
		diggCount = getParam(row, "diggs")
		featureVector = []
		line = ""
		for para in paraList:
			fval = getParam(row, para)
			featureVector.append(fval)
			line += "%d," % (fval)
		line += "%d\n" % (diggCount)
		fh.write(line)
	fh.close()


