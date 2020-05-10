import numpy as np
from flask import Flask, render_template, request, send_file
import flask
#from flask_talisman import Talisman
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import logging
import sqlalchemy
import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_pymongo import pymongo
import json
import re

app = Flask(__name__)
#Talisman(app)

#MongoDB Connection
CONNECTION_STRING="mongodb+srv://td:hello123@tdcluster-9louv.gcp.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
mydb = client["instacart"]
mycol = mydb["denorm_ic"]
#dbM = client.get_database('instacart')
#mydb = client["instacart"]
#colc = mydb["denorm_ic"]


# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/kms/ to help keep secrets secret.
db_user = "root"
db_pass = "hello123"
db_name = "instacart"
cloud_sql_connection_name = "cldsql:us-east4:ic-mysql"



logger = logging.getLogger()

@app.route('/')
@app.route('/index.html', methods=["GET","POST"])
def index():
	return render_template('index.html')

@app.route('/navigation.html', methods=["GET","POST"])
def navigationPage():
	return render_template('navigation.html')


@app.route('/textBased.html', methods=['GET'])
def textBased():
	logging.error("a ["+flask.request.method+"] request came")
	logging.error("00")
	if flask.request.method == 'GET':
		opt = request.values.get('opt')
		
		logging.error("01")
		if opt=="ms":
			logging.error("02")
		#===============================CLOUD SQL====================
		
			# [START cloud_sql_mysql_sqlalchemy_create]
			# The SQLAlchemy engine will help manage interactions, including automatically
			# managing a pool of connections to your database
			db = sqlalchemy.create_engine(
				# Equivalent URL:
				# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
				sqlalchemy.engine.url.URL(
					drivername="mysql+pymysql",
					username=db_user,
					password=db_pass,
					database=db_name,
					query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
				),
				# ... Specify additional properties here.
				# [START_EXCLUDE]
				# [START cloud_sql_mysql_sqlalchemy_limit]
				# Pool size is the maximum number of permanent connections to keep.
				pool_size=5,
				# Temporarily exceeds the set pool_size if no connections are available.
				max_overflow=2,
				# The total number of concurrent connections for your application will be
				# a total of pool_size and max_overflow.
				# [END cloud_sql_mysql_sqlalchemy_limit]
				# [START cloud_sql_mysql_sqlalchemy_backoff]
				# SQLAlchemy automatically uses delays between failed connection attempts,
				# but provides no arguments for configuration.
				# [END cloud_sql_mysql_sqlalchemy_backoff]
				# [START cloud_sql_mysql_sqlalchemy_timeout]
				# 'pool_timeout' is the maximum number of seconds to wait when retrieving a
				# new connection from the pool. After the specified amount of time, an
				# exception will be thrown.
				pool_timeout=30,  # 30 seconds
				# [END cloud_sql_mysql_sqlalchemy_timeout]
				# [START cloud_sql_mysql_sqlalchemy_lifetime]
				# 'pool_recycle' is the maximum number of seconds a connection can persist.
				# Connections that live longer than the specified amount of time will be
				# reestablished
				pool_recycle=1800,  # 30 minutes
				# [END cloud_sql_mysql_sqlalchemy_lifetime]
				# [END_EXCLUDE]
			)
			# [END cloud_sql_mysql_sqlalchemy_create]
		
			logging.error("03")
			votes = []
			with db.connect() as conn:
				# Execute the query and fetch all results
			#	recent_votes = conn.execute(
			#		"SELECT * from departments"
			#	).fetchall()
			#	# Convert the results into a list of dicts representing votes
			#	for row in recent_votes:
			#		votes.append({"candidate": row[0], "time_cast": row[1]})
			
				stmt=""
				try:
					
					query = request.values.get('DBquery').replace("%","%%")
					#res=conn.execute(
					#	"SELECT * from departments LIMIT 4"
					#).fetchall()
					#for row in res:
					#	data=data+row
					
					t1=datetime.datetime.now()
					
					if "select" in query.lower() or "show" in query.lower():
						#rows=conn.execute(query).fetchmany(1000)
						#query=query.limit(1000)
						query=setLimit(query,1000)
						rows=conn.execute(query).fetchall()
						header=conn.execute(query).keys()
						r,h=sqlTable(rows,header)
					else:
						rows=conn.execute(query)#.fetchall()
						r=""
						h=""
					
					logging.error("04")

					t2=datetime.datetime.now()
					tDiff=t2-t1
					time=tDiff.total_seconds()
					time="Time to execute query: "+str(time)+" seconds"
					#table=sqlTable(data)
					#stmt = sqlalchemy.text(
					#	"SELECT * FROM aisles LIMIT 10"
					#)
					# Count number of votes for tabs
					#tab_result = conn.execute(stmt).fetchone()
					#data = tab_result[0]
				
					#header=conn.column_names
					
					query = query.replace("%%","%")
					stmt="Query completed successfully. "
					logging.error("05")
					return render_template("textBased.html", stmt=stmt, r=r, h=h, time=time, query=query,chc=opt)
				
				except SQLAlchemyError as e:
					error = str(e.__dict__['orig'])
					#print("SQLAlchemyError\n")
					#print(e)
					stmt=error
					#print("Stmt Error :: "+error)
					return render_template("textBased.html", stmt=stmt, r="", h="", time="", query=query,chc=opt)
					

		elif opt=="bq":
		#===============================BIG QUERY=====================
			stmt=""
			try:
				client = bigquery.Client()
				Q = request.values.get('DBquery')
				
				# Perform a query.
				#Q = ('SELECT * FROM `cldsql.instacart.aisles` LIMIT 10')
				#Q=query
				t1=datetime.datetime.now()
				
				query_job = client.query(Q)  # API request
				rows = query_job.result()  # Waits for query to finish
				
				t2=datetime.datetime.now()
				tDiff=t2-t1
				time=tDiff.total_seconds()
				time="Time to execute query: "+str(time)+" seconds"
				#for row in rows:
					#print(row.name)
				#	data=row.aisle
				#select * from cldsql.instacart.INFORMATION_SCHEMA.COLUMNS where table_catalog=cldsql and table_schema=instacart and table_name=aisles
				
				#sch=rows.schema
				
				header = ["{0}".format(schema.name) for schema in rows.schema]
				
				r,h=sqlTable(rows,header)

				
				stmt="Query completed successfully. "
				return render_template("textBased.html", stmt=stmt, r=r, h=h, time=time,query=Q,chc=opt)
			except BadRequest as e:
				for e in query_job.errors:
					print('ERROR: {}'.format(e['message']))
					stmt+='ERROR: {}'.format(e['message'])
				return render_template("textBased.html", stmt=stmt, r="", h="", time="",query=Q,chc=opt)
		elif opt=="md":
		#===============================MONGO DB ATLAS=====================			
			t1=datetime.datetime.now()
			
			query = request.values.get('DBquery')

			query_j=json.loads(query)
			alldocs=mycol.find(query_j)
			
			header=[]
			rows=[]
			i=0
			for doc in alldocs:
				rows.append([])
				for key in doc:
					if(len(header)<len(doc)):
						header.append(key)
					rows[i].append(doc[key])
				i+=1
			
			t2=datetime.datetime.now()
			tDiff=t2-t1
			time=tDiff.total_seconds()
			
			r,h=sqlTable(rows,header)
			time="Time to execute query: "+str(time)+" seconds"
			stmt="Query completed successfully. "
			return render_template("textBased.html", stmt=stmt, r=r, h=h, time=time,query=query,chc=opt)
		else:
			return render_template("textBased.html", stmt="",time="",query="",chc="ms")


@app.route('/voiceBased.html', methods=["GET","POST"])
def voiceBasedPage():
	logging.error("a ["+flask.request.method+"] request came")
	#return render_template("voiceBased.html")
	if flask.request.method == 'GET':
		opt = request.values.get('opt')		
		
		if opt=="ms":
		#===============================CLOUD SQL====================
		
			# [START cloud_sql_mysql_sqlalchemy_create]
			# The SQLAlchemy engine will help manage interactions, including automatically
			# managing a pool of connections to your database
			db = sqlalchemy.create_engine(
				# Equivalent URL:
				# mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
				sqlalchemy.engine.url.URL(
					drivername="mysql+pymysql",
					username=db_user,
					password=db_pass,
					database=db_name,
					query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)},
				),
				# ... Specify additional properties here.
				# [START_EXCLUDE]
				# [START cloud_sql_mysql_sqlalchemy_limit]
				# Pool size is the maximum number of permanent connections to keep.
				pool_size=5,
				# Temporarily exceeds the set pool_size if no connections are available.
				max_overflow=2,
				# The total number of concurrent connections for your application will be
				# a total of pool_size and max_overflow.
				# [END cloud_sql_mysql_sqlalchemy_limit]
				# [START cloud_sql_mysql_sqlalchemy_backoff]
				# SQLAlchemy automatically uses delays between failed connection attempts,
				# but provides no arguments for configuration.
				# [END cloud_sql_mysql_sqlalchemy_backoff]
				# [START cloud_sql_mysql_sqlalchemy_timeout]
				# 'pool_timeout' is the maximum number of seconds to wait when retrieving a
				# new connection from the pool. After the specified amount of time, an
				# exception will be thrown.
				pool_timeout=30,  # 30 seconds
				# [END cloud_sql_mysql_sqlalchemy_timeout]
				# [START cloud_sql_mysql_sqlalchemy_lifetime]
				# 'pool_recycle' is the maximum number of seconds a connection can persist.
				# Connections that live longer than the specified amount of time will be
				# reestablished
				pool_recycle=1800,  # 30 minutes
				# [END cloud_sql_mysql_sqlalchemy_lifetime]
				# [END_EXCLUDE]
			)
			# [END cloud_sql_mysql_sqlalchemy_create]
		
		
			votes = []
			with db.connect() as conn:
				# Execute the query and fetch all results
			#	recent_votes = conn.execute(
			#		"SELECT * from departments"
			#	).fetchall()
			#	# Convert the results into a list of dicts representing votes
			#	for row in recent_votes:
			#		votes.append({"candidate": row[0], "time_cast": row[1]})
			
				stmt=""
				try:
					query = request.values.get('final_span')
					query = " "+query
					query = processVoice(query)
					query = query.replace("%","%%")
					#res=conn.execute(
					#	"SELECT * from departments LIMIT 4"
					#).fetchall()
					#for row in res:
					#	data=data+row
					
					t1=datetime.datetime.now()
					
					if "select" in query.lower() or "show" in query.lower():
						#rows=conn.execute(query).fetchmany(1000)
						#query=query.limit(1000)
						query=setLimit(query,1000)
						rows=conn.execute(query).fetchall()
						header=conn.execute(query).keys()
						r,h=sqlTable(rows,header)
					else:
						rows=conn.execute(query)#.fetchall()
						r=""
						h=""
					
					t2=datetime.datetime.now()
					tDiff=t2-t1
					time=tDiff.total_seconds()
					time="Time to execute query: "+str(time)+" seconds"
					#table=sqlTable(data)
					#stmt = sqlalchemy.text(
					#	"SELECT * FROM aisles LIMIT 10"
					#)
					# Count number of votes for tabs
					#tab_result = conn.execute(stmt).fetchone()
					#data = tab_result[0]
				
					#header=conn.column_names
					
					query = query.replace("%%","%")
					stmt="Query completed successfully. "
					return render_template("voiceBased.html", stmt=stmt, r=r, h=h, time=time, query=query,chc=opt)
				
				except SQLAlchemyError as e:
					error = str(e.__dict__['orig'])
					#print("SQLAlchemyError\n")
					#print(e)
					stmt=error
					#print("Stmt Error :: "+error)
					return render_template("voiceBased.html", stmt=stmt, r="", h="", time="", query=query,chc=opt)
		else:
			return render_template("voiceBased.html", stmt="",time="",query="",chc="ms")


def sqlTable(rows,header):
	h=""
	for x in header:
		h+="<th>"+str(x)+"</th>"
	
	h2="<tr>"+h+"</tr>"
	text=""
	for row in rows:
		text+="<tr>"
		for d in row:
			text+="<td>"+str(d)+"</td>"
		text+="</tr>"
	return text,h2

def setLimit(query,limit):
	if ("select" in query.lower() and "limit" not in query.lower() and "create" not in query.lower()):
		query = query.replace(";","")
		query += " LIMIT "+str(limit)+";"
	return query


def processVoice(query):
	select=[" find", " show", " give"]
	remove=[" me", " us", " the"]
	star=[" star"," everything", " entries"]
	and_=[" and"]

	query=replaceString(query,select," select")
	query=replaceString(query,remove," ")
	query=replaceString(query,star," *")
	query=replaceString(query,and_," ,")

	query=query.replace("  "," ")
	query=whereClause(query)
	query=topX_Limit(query)
	query=spaceToUnderScore(query)

	return query

def replaceString(query, old, new):
	for item in old:
		query = query.replace(item, new, 1)
	return query


def whereClause(query):
    #add underscore to where attribute
	start = 'where '
	end = ' is'
	mid=query[query.find(start)+len(start):query.rfind(end)]

	mid2=mid.replace(' ','_')
	mid2=mid2.replace('_,_',', ')
	mid2=mid2.replace(',_',', ')
	mid2=mid2.replace('_,',', ')

	query=query.replace(mid,mid2)
	#============================================
	whereDict=	{
					"is greater than or equal to": ">=",
					"is greater than equal to": ">=",
					"is less than or equal to": "<=",
					"is less than equal to": "<=",
					"is equal to": "=",
					"is greater than": ">",
					"is less than": "<",
					"is not equal to": "!="
				}

	for key in whereDict:
		query = query.replace(key, whereDict[key], 1)

	return query


def topX_Limit(query):
	startIndex=query.find(" top ", 0, query.find(" from "))
	if(startIndex==-1):
		startIndex=query.find(" first ", 0, query.find(" from "))
		if(startIndex==-1):
			return query
		else:
			ind1=query.find(" ", startIndex+1)+1
			ind2=query.find(" ", ind1)
			limit=query[ind1:ind2]
			query=query[:startIndex]+query[ind2:]
	else:
		ind1=query.find(" ", startIndex+1)+1
		ind2=query.find(" ", ind1)
		
		limit=query[ind1:ind2]
		query=query[:startIndex]+query[ind2:]


	query=query+" limit "+limit
	return query


def spaceToUnderScore(query):
	start = 'select '
	end = ' from'
	mid=query[query.find(start)+len(start):query.rfind(end)]

	mid2=mid.replace(' ','_')
	mid2=mid2.replace('_,_',', ')
	mid2=mid2.replace(',_',', ')
	mid2=mid2.replace('_,',', ')

	query=query.replace(mid,mid2)
	return query






if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)