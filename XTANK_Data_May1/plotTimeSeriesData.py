import MySQLdb
import matplotlib.pyplot as plt

def plotDiggDistro(minDiggs = 2):
	db = MySQLdb.connect(user = "root", passwd = "iltwat", db = "X1Diggv2")
        conn = db.cursor()
        query = "SELECT diggs FROM diggFeatures WHERE diggs > %d" % (minDiggs)
        conn.execute(query)
        data = conn.fetchall()
	distro = []
	for row in data:
		distro.append(row[0])
	plt.hist(distro, 100, color='g')
	plt.title(query)
	plt.grid(True)
	plt.show()	
	plt.hist(distro, 100, color='r', cumulative = True)
	plt.grid(True)
	plt.title("%s (CDF) " % (query) )
	plt.show()	
	
def getStories(minDiggs = 10):
	db = MySQLdb.connect(user = "root", passwd = "iltwat", db = "X1Diggv2")
        conn = db.cursor()
        query = "SELECT digg_id FROM diggFeatures WHERE diggs > %d" % (minDiggs)
        conn.execute(query)
        data = conn.fetchall()
        distro = []
        for row in data:
                distro.append(row[0])
	return distro


def getParam(digg_id, param):
	db = MySQLdb.connect(user = "root", passwd = "iltwat", db = "X1Diggv2")
        conn = db.cursor()
	table = "diggFeatures"
	if(param == 'diggs' or param =="fofCount" or param =="authorDiggs" or param == "authorComments" or param == "authorFans" or param == "authorFollows" or param == "authorGender" or param == "authorSubmissions" ):
		table = "diggFeatures"
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
	

def plotSocialDynamicsData(dim, th1=71, th2=121):
	lt1 = th1
	lt2 = th2
	data = getStories()
	diggs1 = []
	param1 = []
	diggs2 = []
	param2 = []
	diggs3 = []
	param3 = []
	for row in data:
		diggCount = getParam(row, "diggs")
		#print "Calculating for ", row ," with ", diggCount , " diggs "
		if(diggCount<lt1):
			diggs1.append(diggCount)
			param1.append(getParam(row, dim) )
		elif(diggCount<lt2):
			diggs2.append(diggCount)
			param2.append(getParam(row, dim) )
		else:
			diggs3.append(diggCount)
			param3.append(getParam(row, dim) )
	print len(diggs1), len(param1), len(diggs2), len(param2), len(diggs3), len(param3)
	plt.xlabel(dim)
	plt.ylabel("Diggs")
	plt.title("Diggs vs %s green(<%d), blue(%d-%d), red(%d+" % (dim, lt1, lt1, lt2, lt2))
	plt.plot(param1, diggs1, "go")
	plt.plot(param2, diggs2, "bo")
	plt.plot(param3, diggs3, "ro")
	plt.show()
	plt.hist(param1,100, color="green", cumulative =True)
	plt.title("CDF of %s for diggs<%d" % (dim, lt1))
	plt.show()
	plt.hist(param2,100, color="blue", cumulative =True)
	plt.title("CDF of %s for diggs>%d AND diggs<%d" % (dim, lt1, lt2))
	plt.show()
	plt.hist(param3,100, color="red", cumulative =True)
	plt.title("CDF of %s for diggs>%d" % (dim, lt2))
	plt.show()

def makeClassificationSet(file, paraList, th1 =71, th2=121):
	lt1 = th1
	lt2 = th2
	data = getStories()
	fh = open(file, 'w')
	fh.write("@RELATION Digg_SocialDynamicsBasedFeatures\n")
	for para in paraList:
		spec = "@ATTRIBUTE %s  NUMERIC\n" % (para)
		fh.write(spec)
	fh.write("@ATTRIBUTE class {A, B, C}\n")
	fh.write("@DATA\n")
	for row in data:
		diggCount = getParam(row, "diggs")
		noiseChance = 0
		cl = 'A'
		if(diggCount<lt1):
			cl = 'A'
		elif(diggCount<lt2):
			cl='B'
		else:
			cl='C'
		featureVector = []
		line = ""
		for para in paraList:
			fval = getParam(row, para)
			if row=='upc1' and para==0:
				noiseChance = noiseChance +2
			elif row =='upc2' and para==0:
				noiseChance = noiseChance +1
			featureVector.append(fval)
			line += "%d," % (fval)
		line += "%s\n" % (cl)
		
		if noiseChance < 2:
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
