import MySQLdb
import matplotlib.pyplot as plt

def plotAuthorData(dim, th1=71, th2=121):
	lt1 = th1
	lt2 = th2
	db = MySQLdb.connect(user = "root", passwd = "iltwat", db = "digg_newdatabase")
	conn = db.cursor()
	query = "SELECT diggs, %s FROM digg_final_jaison" % (dim)
	conn.execute(query)
	data = conn.fetchall()
	conn.close()
	diggs1 = []
	param1 = []
	diggs2 = []
	param2 = []
	diggs3 = []
	param3 = []
	for row in data:
		if(row[0]<lt1):
			diggs1.append(row[0])
			param1.append(row[1])
		elif(row[0]<lt2):
			diggs2.append(row[0])
			param2.append(row[1])
		else:
			diggs3.append(row[0])
			param3.append(row[1])
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

def makeClassificationSet(file, th1 =71, th2=121):
	lt1 = th1
	lt2 = th2
	db = MySQLdb.connect(user = "root", passwd = "iltwat", db = "digg_newdatabase")
	conn = db.cursor()
	query = "SELECT authorDiggs, authorComments, authorFans, authorFollows, authorSubmissions, diggs FROM digg_final_jaison"
	conn.execute(query)
	data = conn.fetchall()
	conn.close()
	fh = open(file, 'w')
	fh.write("@RELATION DiggSocialDynamics_AuthorshipBasedFeatures\n")
	fh.write("@ATTRIBUTE authorDiggs  NUMERIC\n")
	fh.write("@ATTRIBUTE authorcomments  NUMERIC\n")
	fh.write("@ATTRIBUTE authorFans  NUMERIC\n")
	fh.write("@ATTRIBUTE authorFollows  NUMERIC\n")
	fh.write("@ATTRIBUTE authorSubmissions  NUMERIC\n")
	fh.write("@ATTRIBUTE class {A, B, C}\n")
	fh.write("@DATA\n")
	for row in data:
		cl = 'A'
		if(row[5]<lt1):
			cl = 'A'
		elif(row[5]<lt2):
			cl='B'
		else:
			cl='C'
		line = "%d, %d, %d, %d, %d, %s\n" % (row[0], row[1], row[2], row[3], row[4], cl)

		fh.write(line)
	fh.close()
