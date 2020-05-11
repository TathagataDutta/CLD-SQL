print(chr(27)+'[2j')

def processVoice(query):
	query=" "+query
	select=[" find", " show", " give"]
	remove=[" me", " us", " the"]
	star=[" star"," everything", " entries", "entry"]
	and_=[" and"]

	query=replaceString(query,select," select")
	query=replaceString(query,remove," ")
	query=replaceString(query,star," *")
	query=replaceString(query,and_," ,")

	query=query.replace("  "," ")

	query=mathOps(query)
	query=whereClause(query)
	query=orderByClause(query)
	query=topX_Limit(query)
	query=spaceToUnderScore(query)

	#capitalize keywords and remove space from start
	query=query.replace(" from "," FROM ").replace(" where "," WHERE ").replace(" select ", " SELECT ").replace(" and ", " AND ").replace(" or "," OR ").replace(" order by ", " ORDER BY ")
	return query

def replaceString(query, old, new):
	query1=query[0:query.find("from")]
	query2=query[query.find("from"):]
	for item in old:
		query1 = query1.replace(item, new, 1)
	query=query1+query2
	return query

def mathOps(query):
	pass
	#show me the smallest value of order_hour_of_day from orders
	#SELECT MIN(order_hour_of_day) FROM orders;

	if not(" value of " in query or " average of " in query or " mean of " in query or " sum of " in query):
		return query

	mathOpsDict={
					" smallest value of ": "MIN(",
					" least value of ": "MIN(",
					" lowest value of ": "MIN(",

					" largest value of ": "MAX(",
					" highest value of ": "MAX(",

					" average value of ": "AVG(",
					" average of ": "AVG(",
					" mean value of ": "AVG(",
					" mean of ": "AVG(",

					" sum of ": "SUM("
				}

	for key in mathOpsDict:
		query = query.replace(key, mathOpsDict[key])

	query=query.replace(" from", ") from")
	return query

def whereClause(query):
    #add underscore to where attribute
	if " where " not in query:
		return query
	start = 'where '
	end = ' is'
	mid=query[query.find(start)+len(start):query.find(end)]

	mid2=mid.replace(' ','_')
	mid2=mid2.replace('_,_',', ')
	mid2=mid2.replace(',_',', ')
	mid2=mid2.replace('_,',', ')

	query=query.replace(mid,mid2)

	if " and " in query:
		start=' and '
		end = ' is'
		mid=query[query.find(start)+len(start):query.rfind(end)]

		mid2=mid.replace(' ','_')
		mid2=mid2.replace('_,_',', ')
		mid2=mid2.replace(',_',', ')
		mid2=mid2.replace('_,',', ')

		query=query.replace(mid,mid2)
	elif " or " in query:
		start=' or '
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
					"is not equal to": "!=",
					
					"is between": "BETWEEN",
					"is":"="
				}

	for key in whereDict:
		query = query.replace(key, whereDict[key])

	return query

def orderByClause(query):
	
	if " sorted by " not in query:
		return query

	query=query.replace(" sorted by "," order by ")
	
	start = 'order by '
	end = ' in'
	mid=query[query.find(start)+len(start):query.find(end)]

	mid2=mid.replace(' ','_')
	mid2=mid2.replace('_,_',', ')
	mid2=mid2.replace(',_',', ')
	mid2=mid2.replace('_,',', ')

	query=query.replace(mid,mid2)

	#========================================================================

	orderByDict={
					"in ascending order": "ASC",
					"in descending order": "DESC"
				}

	for key in orderByDict:
		query = query.replace(key, orderByDict[key])

	print("HELLO")
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


query="show me the smallest value of order_hour_of_day from orders"
query=processVoice(query)
print("FINAL: ",query)