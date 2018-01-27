import requests
from bs4 import BeautifulSoup
import pandas

def dataToArray(df, key):
    arr= []
    for i in range(0,len(df[key])):
        arr.append(df.iloc[i])
    return arr
    
#uses quick sort to sort values
def sortByKey(array, key):
    if len(array[:]) < 2:
        return array
    else:
        pivot= float(array[0][key])
        less = [i for i in array[1:] if float(i[key]) <= pivot]
        greater = [i for i in array[1:] if float(i[key]) > pivot]

        return sortByKey(greater,key) + [array[0]] + sortByKey(less,key)

r = requests.get("https://www.ebay.com/deals")
c= r.content
soup = BeautifulSoup(c, "html.parser")

#the individual items on thee page
all = soup.find_all("div",{"itemscope":"itemscope"})

#getting prices for each item
prices=[]
for item in all:
    it = (item.find("span",{"itemprop":"price"}))
    if it != None:
        prices.append(float(it.text[1:].replace(",","")))
    else:
        prices.append("N/A")

#getting discount percent
percent=[]
for item in all:
    it = (item.find("span",{"class":"itemtile-price-bold"}))
    if it != None:
        percent.append(it.text)
    else:
        percent.append("N/A")

#getting price difference
orig_price=[]
for item in all:
    it = (item.find("span",{"class":"itemtile-price-strikethrough"}))
    if it !=None:
        orig_price.append(float(it.text[1:].replace(",","")))
    else:
        orig_price.append("N/A")

#getting names of products
names=[]
for item in all:
    it = (item.find("span",{"itemprop":"name"}))
    if it != None:
        names.append(it.text)
    else:
        names.append("N/A")

#getting images
images =[]
for item in all:
    it = (item.find("img"))
    if it != None:
        src=it["src"]
        images.append(src)
    else:
        images.append("N/A")

urls=[]
for item in all:
    it = (item.find("a",{"itemprop":"url"}))
    if it != None:
        link=it["href"]
        urls.append(link)
    else:
        urls.append("N/A")

#image url, price, original price and percent off
df1 = pandas.DataFrame(names, columns=["Name"])
df1["Image URL"]=images
df1["URL"]=urls
df1["Price"]=prices
df1["Original Price"] = orig_price
df1["Percent Off"] = percent

#remove undiscounted items
i=len(df1)-1
while(i>=0):
    if df1.iloc[i]["Percent Off"]==("N/A") or df1.iloc[i]["Original Price"]==("N/A"):
        df1 = df1.drop(df1.index[i],0)
    i=i-1

#the money off and names
df1["Money Off"] =df1["Original Price"]- df1["Price"]

#make indexes
counter=0
indexes=[]
for item in df1["Price"]:
    indexes.append(counter)
    counter=counter+1
df1["ID"]=indexes

#make the better DataFrame
df2= pandas.DataFrame(indexes,columns= ["ID"])

#put in names
names=[]
for name in df1["Name"]:
    if name!= None:
        names.append(name)
df2["Name"]= names

#put in images
images=[]
for image in df1["Image URL"]:
    if image!= None:
        images.append(image)
df2["Image URL"]= images

#put in urls
urls= []
for url in df1["URL"]:
    if url != None:
        urls.append(url)
df2["URL"]= urls

#put in prices
prices=[]
for price in df1["Price"]:
    if price != None:
        entry = ("%.2f" % price)
        prices.append(entry)
df2["Price"] = prices

#put in original price
orig_prices=[]
for orig in df1["Original Price"]:
    if orig != None:
        entry = ("%.2f" % orig)
        orig_prices.append(entry)
df2["Original Price"] = orig_prices

#put in percent Off
percents=[]
for percent in df1["Percent Off"]:
    if percent != None:
        entry = percent
        entry = entry.replace("%","").replace(" ","").replace("off","")
        percents.append(entry)
df2["Percent Off"] = percents

#put in money Off
money_off=[]
for money in df1["Money Off"]:
    if money != None:
        entry = ("%.2f" % money)
        money_off.append(entry)
df2["Money Off"] = money_off

df2.to_csv("Discount.csv")
