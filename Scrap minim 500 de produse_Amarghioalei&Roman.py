'''
Pretul este o variabila numerica extrasa pentru a ajuta la crearea de statistici referitoare
la cel mai mic sau mai mare pret al unui frigider vandut de Emag precum si pentru a vedea 
in ce categorii de pret se incadreaza frigiderele vandute.
Discountul este important pentru a verifica marja de discounturi practicate de companie
Numarul de review-uri pentru produse poate evidentia care sunt produsele cele mai populare in randul frigiderelor
pentru care clientii ce au achizitionat produsul au dorit sa lase un comentariu.
Clasa energetica este importanta pentru a identifica care gama energetica este cea mai des propusa spre vanzare
'''

import urllib.request
from bs4 import BeautifulSoup 
import requests as rq
import re

# crearea url-ului de baza
base_url = 'https://www.emag.ro/frigidere/'
r = rq.get(base_url)

soup = BeautifulSoup(r.text)
# Use regex to isolate only the links of the page numbers, the one you click on.
page_count_links = soup.find_all("a",href=re.compile(r".*javascript:goToPage.*"))
try: # Make sure there are more than one page, otherwise, set to 1.
    num_pages = int(page_count_links[-1].get_text())
except IndexError:
    num_pages = 9

# construirea listei de url-uri conform template-ului EMAG
url_list = ["{}p{}/c".format(base_url, str(page)) for page in range( 1 , num_pages  + 1)]


names=[]
reviews=[]
prices=[]
discounts=[]
classes=[]

for pg in url_list:
   
# interogarea fiecarei pagini cu frigidere
 page = urllib.request.urlopen(pg)
 soup=BeautifulSoup(page, 'html.parser')
 print(soup)
# crearea containerului pentru fiecare din cele 6 pagini cu frigidere
 mv_containers = soup.find_all('div', class_ = 'card-item js-product-data')
 for container in mv_containers:
#extragerea pretului 
  price_box = container.find('p', attrs={'class':'product-new-price'})
  price = price_box.text.strip()
  price, currency = price.split(" ")
  price=str.replace(price,'.',"")
  price=int(price)
  price=price/100
  prices.append(price)
#extragerea numelui
  name_box = container.find('h2', class_='card-body product-title-zone')
  name=name_box.text.strip()
  print(name)
  names.append(name)
#extragerea clasei energetice a frigiderului din cadrul numelui frigiderului
  if name.find("Clasa energetica") is not -1:
    clasa = name.split("Clasa energetica")[1].split()[0]
    clasa = clasa.rstrip(',')
    print(clasa)
    classes.append(clasa)
  elif name.find("Clasa Energetica") is not -1:
    clasa = name.split("Clasa Energetica")[1].split()[0]
    clasa = clasa.rstrip(',')
    print(clasa)
    classes.append(clasa)
  elif name.find("Clasa") is not -1:
   clasa = name.split("Clasa")[1].split()[0]
   clasa = clasa.rstrip(',')
   print(clasa)
   classes.append(clasa)
  elif name.find("clasa") is not -1:
    clasa = name.split("clasa")[1].split()[0]
    clasa = clasa.rstrip(',')
    print(clasa)
    classes.append(clasa)
  elif name.find(", A") is not -1 and name.split(", A")[1] =='+':
    clasa = name.split(", A")[1].split()[0]
    clasa = clasa.rstrip(',')
    clasa = 'A' + clasa
    print(clasa)
    classes.append(clasa)
  else:
    clasa = 'lipsa'
    classes.append(clasa)
#extragerea numarului de reviewuri si transformarea in variabila numerica 
  review_box = container.find('span', attrs={'class':'hidden-xs '})
  review = review_box.text.strip()
  if review.find ("de") is not -1:
   review = review[:3]
  elif review.find('review') is not -1:
   review = review[:2]
  review = int(review)
  print (review)
  reviews.append(review)
#extragerea discountului si transformarea in variabila numerica
  discount_box = soup.find('span', attrs={'class':'product-this-deal'})
  discount=discount_box.text.strip()
  discount = discount.replace('(', '').replace(')','').replace('%','').replace('-','')
  discount=int(discount)
  discount = discount / 100
  print(discount)
  discounts.append(discount)

#crearea data frame-ului cu informatiile extrase
import pandas as pd  
frigidere = pd.DataFrame({'Nume': names, 'Pret': prices,'Clasa': classes, 'Review': reviews, 'Discount': discounts})
print(frigidere.info())

#salvarea in csv
frigidere.to_csv('frigidere.csv')

#afisare tipuri de variabile
print(frigidere.dtypes)

#Analize descriptive

#minimul, maximul si media pretului, discountului si numarului de review-uri
frigidere.describe().loc[['min', 'max', 'mean'], ['Pret', 'Discount', 'Review']]

#frecventa de aparitie pentru variabila categoriala Clasa
frigidere['Clasa'].value_counts()

#creare histograme pt pret, discount si numar review-uri
import matplotlib.pyplot as plt
fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (16,4))
ax1,ax2,ax3 = fig.axes
ax1.hist(frigidere['Pret'], bins = 10, range = (0,13000))
ax1.set_title('Pret')
ax2.hist(frigidere['Discount'], bins = 20, range = (0,0.35))
ax2.set_title('Discount')
ax3.hist(frigidere['Review'], bins = 20, range = (0,172))
ax3.set_title('Review')
for ax in fig.axes:
 ax.spines['top'].set_visible(False)
 ax.spines['right'].set_visible(False)
plt.show()

#creare de pie chart pentru variabila categoriala Clasa
slices_clasa = [200, 199, 118, 20, 3]
categories = ['lipsa', 'A+', 'A++', 'A+++', 'A']
colors = ['r', 'g', 'b', 'y']
plt.pie(slices_clasa , labels=categories, colors=colors, startangle=80)
