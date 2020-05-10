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
					"is equal to": "=",
					"is greater than": ">",
					"is greater than": ">",
					"is greater than or equal to": ">=",
					"is greater than equal to": ">=",
					"is less than": "<",
					"is less than or equal to": "<=",
					"is less than equal to": "<=",
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

query="show me everything from products where product id is equal to 1"
query=processVoice(query)
print("FINAL",query)