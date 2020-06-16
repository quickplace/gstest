#テキストファイルに記載してあるキーワードを１行ずつ読み込み
#google 検索の一番目に表示されたURLをcsvにして書き出す
#
#参考：https://github.com/psalias2006/Google2Csv
# pip install requests
# pip install beautifulsoup4
# pip install pandas

from bs4 import BeautifulSoup
import requests
import pandas as pd

def simpleGoogleSearch(query, start):
  results = []

  query = query.replace(' ', '+')
  URL = f"https://google.co.jp/search?hl=jp&oe=shift_jis&num=3&q={query}&start={start}"

  # desktop user-agent
  USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
  
  headers = {"user-agent" : USER_AGENT}
  resp = requests.get(URL, headers=headers)

  if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")

    for g in soup.find_all('div', class_='r'):
      anchors = g.find_all('a')

      if anchors:
        link  = anchors[0]['href']
        title = g.find('h3').text
        item  = {"keywords": query, "title": title, "link": link}
        results.append(item)

  return results

def googleToPandas(googleQuery):
  resultsCounter  = 0
  resultsList     = []

#  while True:
  pageResults = simpleGoogleSearch(googleQuery, resultsCounter)
  resultsList.extend(pageResults)
    
#    if not pageResults: break
#    else: 
#      resultsList.extend(pageResults)
#      resultsCounter = resultsCounter + 10

  return pd.DataFrame(resultsList)

with open('keyword.txt','r') as f_input:

    for line in f_input.read().splitlines():
        results = googleToPandas(line)
        results.to_csv('googleresults.csv', mode='a')

with open('googleresults.csv', 'r') as f_testread:
    print(f_testread.read())

