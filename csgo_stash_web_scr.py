import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request

my_url ='https://csgostash.com/weapon/AK-47'
req = Request(my_url,headers={'User-Agent':'Mozilla/5.0'})
uClient = uReq(req)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser") #does my html parsing
containers = page_soup.findAll("div",{"class":"col-lg-4 col-md-6 col-widen text-center"}) #grabs all the items/product

filename = "AK_skins.csv"
f = open(filename,"w")

headers = "title,rarity,star_availability,normal_price_range,st_price_range,case\n"

f.write(headers)

for container in containers:

    title = container.h3.text
    
    
    try:
        rarity_p = container.findAll("a", {"class": "nounderline"})
        rarity = rarity_p[0].div.p.text.strip()
    except IndexError as e:
        rarity = "not found"
    
    try:
        star = container.findAll("div", {"class": "stattrak"})
        star_availability = star[0].p.text
    except IndexError as e:
        star_availability = "No startrek available"
    

    price = container.findAll("div", {"class": "price"})
    try:
        normal_price_range = price[0].p.a["title"]
    except IndexError as e:
        normal_price_range="default"

    try:
        st_price_range = price[1].p.a["title"]
    except TypeError as e:
        st_price_range = "No startrek available"
    except IndexError as e:
        st_price_range = "No startrek available"
    case_f = container.findAll("div", {"class":"collection"})
    try:
        case = case_f[0].p.a.text
    except IndexError as e:
        case= "default"

    f.write(title + "," + rarity + "," + star_availability + "," + normal_price_range + "," + st_price_range + "," + case + "\n" )

    #if there was , occuring in some result then use result.replace(",", "|" )

f.close()
