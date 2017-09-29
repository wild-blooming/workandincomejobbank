import pymysql
import re
import requests
from bs4 import BeautifulSoup

#cookies
jar = requests.cookies.RequestsCookieJar()
jar.set('ASP.NET_SessionId','zcbbo0551pspxk55vs12s245',domain='job-bank.workandincome.govt.nz',path='/')
jar.set('TS015cea2c','014cf3b645b65b52d67bd0e655a7561d2f4ebe47967a122b5998ea40ecdc86fadc5ed62db34931660709ed7f4c88e4fc8a8f7f42c0',domain='job-bank.workandincome.govt.nz',path='/')

#initial page
url = 'http://job-bank.workandincome.govt.nz/find-a-job/search.aspx'

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
		'Content-Type':'application/x-www-form-urlencoded',
		'referer':'http://job-bank.workandincome.govt.nz/find-a-job/search.aspx'}

payload = {'__EVENTTARGET':'',
		'__EVENTARGUMENT':'',
		'__LASTFOCUS':'',
		'__VIEWSTATE':'/wEPDwUKMTYyNzEyMjAyNQ9kFgICAg9kFgQCAw8QDxYGHg1EYXRhVGV4dEZpZWxkBQVUaXRsZR4ORGF0YVZhbHVlRmllbGQFAklkHgtfIURhdGFCb3VuZGdkEBUfCEF1Y2tsYW5kFUJheSBvZiBQbGVudHkgQ2VudHJhbBJCYXkgb2YgUGxlbnR5IEVhc3QSQmF5IG9mIFBsZW50eSBXZXN0BkJ1bGxlchJDYW50ZXJidXJ5IENvdW50cnkNQ2VudHJhbCBPdGFnbw9DZW50cmFsIFBsYXRlYXUSQ2hyaXN0Y2h1cmNoIE1ldHJvB0hhdXJha2kLSGF3a2UncyBCYXkKSG9yb3doZW51YQxLaW5nIENvdW50cnkITWFuYXdhdHULTWFybGJvcm91Z2gGTmVsc29uDE5vcnRoIElzbGFuZAlOb3J0aGxhbmQFT3RhZ28LUG92ZXJ0eSBCYXkQU291dGggQ2FudGVyYnVyeQxTb3V0aCBJc2xhbmQNU291dGggV2Fpa2F0bwlTb3V0aGxhbmQIVGFyYW5ha2kGVGFzbWFuB1dhaWthdG8JV2FpcmFyYXBhCFdhbmdhbnVpCldlbGxpbmd0b24KV2VzdCBDb2FzdBUfBDY3MDkENTQwNwQ4NDkwBDg0OTEEODQ5OQQ4NDk0BDg0OTYEODQ5MwQ2MDYxBDg1MDAENTM3OAQ4NDk1BDg0OTgENjg2OAQ2MjgwBDc4NTkEODUyMAQ1NjUwBDU1NTcENjI5MAQ4NDk3BDg1MjEEODQ5MgQ4Mjg5BDYzNzMENjQxNwQ2MDg4BDg0ODgEODQ4OQQ2Njk3BDc1NjMUKwMfZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAgcPFgIeC18hSXRlbUNvdW50AgwWGAIBD2QWAgIBD2QWAmYPFQUGLTg1MDAyBi04NTAwMgYtODUwMDIGLTg1MDAyEEF1Y2tsYW5kIENlbnRyYWxkAgIPZBYCAgEPZBYCZg8VBQYtNDk5MjQGLTQ5OTI0Bi00OTkyNAYtNDk5MjQLSGVsZW5zdmlsbGVkAgMPZBYCAgEPZBYCZg8VBQYtNDk5NTYGLTQ5OTU2Bi00OTk1NgYtNDk5NTYGSG93aWNrZAIED2QWAgIBD2QWAmYPFQUGLTg0OTA1Bi04NDkwNQYtODQ5MDUGLTg0OTA1B01hbnVrYXVkAgUPZBYCAgEPZBYCZg8VBQYtODQ4NzgGLTg0ODc4Bi04NDg3OAYtODQ4NzgLTm9ydGggU2hvcmVkAgYPZBYCAgEPZBYCZg8VBQYtODQ4NjUGLTg0ODY1Bi04NDg2NQYtODQ4NjUFT3Jld2FkAgcPZBYCAgEPZBYCZg8VBQYtODQ4NDAGLTg0ODQwBi04NDg0MAYtODQ4NDATUHVrZWtvaGUgLyBQYXBha3VyYWQCCA9kFgICAQ9kFgJmDxUFBi04NDc2OAYtODQ3NjgGLTg0NzY4Bi04NDc2OA5XYWloZWtlIElzbGFuZGQCCQ9kFgICAQ9kFgJmDxUFBi04NDc1NwYtODQ3NTcGLTg0NzU3Bi04NDc1NwlXYWl0YWtlcmVkAgoPZBYCAgEPZBYCZg8VBQYtODQ3NTIGLTg0NzUyBi04NDc1MgYtODQ3NTIGV2FpdWt1ZAILD2QWAgIBD2QWAmYPFQUGLTQ5OTU3Bi00OTk1NwYtNDk5NTcGLTQ5OTU3CVdhcmt3b3J0aGQCDA9kFgICAQ9kFgJmDxUFBy0xMTk5MjcHLTExOTkyNwctMTE5OTI3By0xMTk5MjcLV2hhbmdhcGFyb2FkZNQo2rbNOVhrzvDAQZDCrRo9tfHe',
		'__EVENTVALIDATION':'/wEWIwKgjpj5DgKjr8zKDAKk09H9CQKA/ez4BAKB/eD0CgLRnr2PAQLRnonqCQLRnqmNDALRns37DwLRnqWyDQLRnuGcBwLi9r3WDQKW/ej6CQLG3eOIBQLRntnWBALRnt2xBwLi9pGdCwLot4egBwKO79+NBgLM06TMDQKI75uMCwKI75OODALDnqWPAQLRnrGJAgLM07CrAgLRnpXBDgL+t7OmAgLF3Yf3BAKbxJ7jBALot6/LDQL+t7/LDQL+t4umAgLDnomJAgLh9uGICwKP58jqDZvaq95DK7Tvzdrne9+/W8+VMm9B',
		'fn':'',
		'fnData':'',
		'SearchString':'',
		'Region':'6709',
		'btn1_1':'Search'}
		

r = requests.post(url,cookies=jar,data=payload,headers=headers) #Object moved to,302,URL redirect

#connect mysql
conn = pymysql.connect(host='127.0.0.1',unix_socket='/tmp/mysql.sock',user='root',passwd='asdf1234*',db='mysql')
cur = conn.cursor()
cur.execute("USE workandincome")

#define recur,traversing all pages
def next(res):
	soup = BeautifulSoup(res.text,'lxml')
	#do something here
	table = soup.find_all('table')[0]
	print soup.find('div',class_='paging').span.string
#	print table
	for row in table.find_all('tr'):
#		print row
		has_td = row.find_all('td')
		if len(has_td) != 0:

			#extract JobId from 1st <td>
			match = re.search('\d+',has_td[0].a['href'])
			if match:
				JobId = match.group(0)

			values = [int(JobId)]
			for string in row.stripped_strings:
				values.append(string)
			print values
			sql = "INSERT INTO jobbankauckland (jobid,title,added,category,area) VALUES (%s,%s,%s,%s,%s)" #TypeError: %d format: a number is required, not str

			cur.execute(sql,values)

	next_page = soup.find('a',string=re.compile("^Next"))
	if(next_page):

		#return to initial page if request without cookies 
		#ASP.NET est a unique session for user during visit,track a session id,map the user to session state information,store user specific info
		next(requests.get('http://job-bank.workandincome.govt.nz/find-a-job/' + next_page['href'],cookies=jar)) 

next(r)

cur.connection.commit()
#close mysql
cur.close()
#conn.close()
