from bs4 import BeautifulSoup
import requests

# Our Web scraper
def webScrape(query):
    #url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=2013+Panini+Prizm+Giannis+Antetokounmpo+Rookie+Card+graded&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_PrefLoc=3&_sop=13&_osacat=0&_odkw=2013+Panini+Prizm+Giannis+Antetokounmpo+Rookie+Card&rt=nc&_dcat=214&LH_Sold=1&_oaa=1"
    #url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=2007+Patrick+Kane+Upper+Deck+Young+Guns+Rookie+Card+mint&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_PrefLoc=3&_sop=13&_osacat=0&_odkw=2007+Patrick+Kane+Upper+Deck+Young+Guns+Rookie+Card+min&LH_Sold=1"
    #short_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=Patrick+Kane+Young+Guns+Rookie+Card+Mint+2007&LH_Sold=1"

    url = (f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw={query}+-lot&LH_Sold=1')
    #print(url)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # prints the html page
    # print(soup.prettify())

    listings = soup.find_all(class_='s-item__wrapper')

    avg_price = 0.00

    listing_list = []

    # count number of listings that are used in pricing
    count = 0

    if len(listings)<3:
        print('not enough data')

    else:    
        for listing in listings[0:10]:
            try:
                #print(listing)
                #title = soup.find(class_='s-item__title').get_text()
                date = listing.find(class_='s-item__title--tagblock__COMPLETED').find(class_='POSITIVE').get_text()
                #print(date)
                
                title = listing.find(class_='s-item__title--has-tags').get_text()
                #print(title)
                
                link = listing.find(class_='s-item__link')['href']
                #print(link)

                price = listing.find(class_='s-item__price').get_text()
                price = price.replace("$", "")
                price = price.replace(",", "")
                #print(price)
                price = float(price)

                shipping = listing.find(class_='s-item__shipping').get_text()
                if shipping == "Free shipping":
                    shipping = 0.00
                else:
                    shipping = shipping.replace("+$", "")
                    shipping = shipping.replace(" shipping", "")
                    shipping = float(shipping)
                
                # to go from thumnail to large img remove 'thumbs/' and remplace '225' w/ '500
                # https://i.ebayimg.com/thumbs/images/g/JzgAAOSwcwRextIc/s-l225.jpg
                img = listing.find(class_='s-item__image-img')['src']
                img_url = img.replace("thumbs/", "")
                img_url = img_url.replace("225", "500")
                
                count+=1
                avg_price += price
                avg_price += shipping

                list_price = price+shipping
                listing_list.append([img_url, "{:.2f}".format(float(list_price)), date, title, link])

            except:
                print('error: problem parsing listing')

        avg_price = float(avg_price/count)
        avg_price = round(avg_price, 2)
        avg_price = "{:.2f}".format(float(avg_price))
        avg_price = "{:,}".format(float(avg_price))
        #print(avg_price)

        return [img_url, avg_price, listing_list]