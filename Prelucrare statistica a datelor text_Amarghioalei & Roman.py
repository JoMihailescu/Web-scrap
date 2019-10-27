# -*- coding: utf-8 -*-
#import libraries
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
quote_page =['https://www.emag.ro/frigider-cu-doua-usi-arctic-250-l-clasa-a-garden-fresh-eco-led-h-160-6-cm-argintiu-ad54280mt/pd/DMZ1W5BBM/',
        'https://www.emag.ro/frigider-cu-doua-usi-beko-565-l-clasa-a-neofrost-h-182-cm-inox-antiamprenta-dn161220x/pd/DPFWLYBBM/',
        'https://www.emag.ro/frigider-cu-doua-usi-lg-438-l-clasa-a-display-led-no-frost-compresor-liniar-smart-diagnosis-wifi-racire-prin-usa-h-178-cm-argintiu-gtb574pzhzd/pd/D1JX30BBM/',
        'https://www.emag.ro/frigider-cu-doua-usi-samsung-384-l-clasa-a-no-frost-h-178-5-inox-rt38k5530s9-eo/pd/DMQPC3BBM/',
        'https://www.emag.ro/frigider-cu-doua-usi-lg-506-l-clasa-a-no-frost-compresor-inverter-linear-display-extern-smart-thinq-h-180-cm-inox-gtb744pzhzd/pd/DLNQ1VBBM/',
        'https://www.emag.ro/frigider-samsung-440-l-clasa-a-no-frost-twin-cooling-plus-digital-inverter-smart-convertible-display-iluminare-led-h-178-5-cm-bej-rt43k6330ef-es/pd/DQ1HHZBBM/']

# for loop
data = []
for pg in quote_page:
# query the website and return the html to the variable ‘page’
 page = urllib.request.urlopen(pg)
 soup=BeautifulSoup(page, 'html.parser')
 print(soup)

 price_box = soup.find('p', attrs={'class':'product-new-price'})
 price = price_box.text.strip()
 price, currency=price.split(" ")
 price=str.replace(price,'.',"")
 price=int(price)
 price=price/100

 name_box = soup.find('h1')
 name=name_box.text.strip()
 print(name)

 review_box = soup.find('p', attrs={'class':'small semibold font-size-sm text-muted'})
 review = review_box.text.strip()
 print (review)

 rating_box = soup.find('p', attrs={'class':'review-rating-data'})
 rating = rating_box.text.strip()
 print (rating)
 
 discount_box = soup.find ('span', attrs={'class':'product-this-deal'})
 discount = discount_box.text.replace(' ', '')
 discount = discount.replace('(', '').replace(')','').replace('-','')

# save the data in tuple
 data.append((name, price, currency, rating, review, discount)) 

tabel = pd.DataFrame.from_records(data, columns=['nume produs', 'pret', 'moneda', 'rating', 'review','discount'])

import csv
from datetime import datetime

with open('emagscrap.csv','a') as csv_file:
 writer = csv.writer(csv_file)
 writer.writerow(['nume produs', 'pret', 'moneda', 'rating', 'review', 'discount'])
# The for loop
 for name, price, currency, rating, review, discount in data:
  writer.writerow([name, price, currency, rating, review, discount, datetime.now()])
