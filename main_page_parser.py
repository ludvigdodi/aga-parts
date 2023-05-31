import requests
from bs4 import BeautifulSoup
import csv


brands_list = []
URL = "https://www.aga-parts.com"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
}


# RESPONSE FROM PAGE
def get_html(url):
    res = requests.get(f'{URL}/brands/', headers=HEADERS)
    return res


# PARSING PAGES
def get_content(html):
    soup = BeautifulSoup(html.content, "html.parser")
    brands = soup.find_all("div", class_="aga-w-100")

    for brand in brands:
        title = brand.find('img').get('title')
        link = brand.find('a').get('href')
        brands_list.append([title, f'{URL}{link[:-1]}'])
        # print(brands_list)
    return brands_list


# WRITE TO CSV FILE
def save_doc(brands_list):
    with open("list_of_brands.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["BRAND", "PAGE LINK"])
        for item in brands_list:
            writer.writerow([item[0], item[1]])


# START PARSER
def parser():
    html = get_html(URL)
    get_content(html)
    save_doc(brands_list)
  
parser()
