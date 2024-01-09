from datetime import datetime
import requests
import csv
import bs4

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
     'Accept-Language': 'en-US, en;q=0.5',
    
}

def get_page_html(url):
    res = requests.get(url=url,headers=REQUEST_HEADER)
    return res.content

def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay' 
    })
    price_spans = main_price_span.findALL('span')
    for span in price_spans:
        price = span.text.strip().replace('$','').replace(',', '')
        try:
            return float(price)
        except ValueError:
            print("Value Obtained for Price Could Not be Parsed")
            exit()

def extract_product_info(url):
    product_info = {}
    print('Scraping URL: {url}')
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    print(product_info)

if __name__ == "__main__":
   with open('amazon_products_urls.csv', newline='') as csvfile:
       reader = csv.reader(csvfile, delimiter=',')
       for row in reader:
           url = row[0]
           print(extract_product_info(url))    
   