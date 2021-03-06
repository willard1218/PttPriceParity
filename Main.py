# -*- coding: utf-8 -*-  
import requests
from bs4 import BeautifulSoup
import sys
import re

import Number
from PttDate import PttDate


    






def Main():
    
  baseUrl = 'https://www.ptt.cc'
  targetUrl = '/bbs/MacShop/index.html'
  


  titlePattern = "(iphone ?(6s+|6s|6\+|6|5s|5c|5|4s|4|3g|3))"
  capacityPattern = "((16|32|64|128) ?g)"
  conditions = [ 'phone', u'賣' ]
  # 售出
  pageNumber = 400
  for j in range(pageNumber):


    r = requests.get(baseUrl + targetUrl, verify=False)
    soup = BeautifulSoup( r.text.encode( r.encoding ) )
    articles = soup.findAll( 'a', href = True )

    for i, article in enumerate(articles):
      hasMatch = True

      title = article.text.lower()
      
      for k in conditions:
        if k not in title:
          hasMatch = False
          break


      if hasMatch:

        try:
          targetUrl = article['href']
          title = article.text.encode('utf8').lower()
          r = requests.get(baseUrl + targetUrl, verify=False)


          soup = BeautifulSoup( r.text.encode( r.encoding ) )
          content = soup.findAll( 'div', class_ = 'bbs-screen bbs-content' )[0].text.lower()



          if u"售出"  in content:
            raise "sold out"

          contentLines = content.split('\n')

          
          posttime = soup.findAll( 'span', class_ = 'article-meta-value' )
          posttime = posttime[3].text if len(posttime) > 3 else None
          posttime = posttime.split()
          pttDate = PttDate(posttime[-1], posttime[1], posttime[2])


      
            

          specArr = [a for a in contentLines if u'物品型號' in a]
          spec = None


          if len(specArr) > 0:
            spec = spec[0].encode('utf8')
            if len(specArr) > 1 and specArr[1].lower().strip() == 'plus':
              spec += '+'

          price = [a for a in contentLines if u'價格' in a]
          price = price[0].encode('utf8') if len(price) > 0 else None          
          price = price.replace('k','000').replace('.','').replace(',','')
          regex = re.compile("([0-9]+)")
          result = regex.search(price)

          price = result.group(1).replace(' ','')




          regex = re.compile(titlePattern)          
          result = regex.search(title)

        
          version = result.group(1).replace(' ','').replace('iphone','')
          regex = re.compile(capacityPattern)

          result = regex.search(title)
         
          spec = result.group(1).replace('g','').replace(' ','')

          if len(version) == 1:
            version = version + ' ' 


          
          if not Number.IsInt(price):
            raise "price isn't int :", price


          print "%2s %3sG $%5s %s %s" %(version, spec, price, pttDate.__str__(), baseUrl+targetUrl)
        except Exception as e:
          #print (type(e), str(e))
          break
     

      if u'上頁' in article.text:
        nextPageUrl = article['href']
        #print "nextPageUrl :" + nextPageUrl

    targetUrl = nextPageUrl


if __name__ == '__main__':
  Main()