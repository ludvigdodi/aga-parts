import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from main_page_parser import brands_list


URL = "https://www.aga-parts.com"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
}
items_links =[]


for page in brands_list:
    page_url = f'{page[1]}-parts'


    # RESPONCE FROM PAGE
    def get_page_html(page_url):
        res = requests.get(page_url, headers=HEADERS)
        return res


    # CHECK IS THE CONTENT ON PAGE
    def check_content(page_html):
        soup = BeautifulSoup(page_html.content, 'html.parser')
        page_cont = soup.find('div', class_="view-content row")
        return page_cont
    

    # PARSING PAGES
    def get_page_content(page_html):        
        soup = BeautifulSoup(page_html.content, "html.parser")
        items_list = soup.find_all('span', class_="field-content")
        for item in items_list:
            item_link = item.find('a').get('href')
            items_links.append(f'{URL}{item_link}')
            print(items_links)
        return items_links


    # WRITE TO CSV FILE
    def save_page_doc(items_links):
        with open("list_of_brands_items.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["PAGE LINK"])
            for item in items_links:
                writer.writerow([item])


    # START PROGRAM
    def parser():
        for p in range(0, 100000):
            page_html = get_page_html(f'{page_url}?page={p}')
            is_content = check_content(page_html)
            print(f"Parsing - {p} page")
            sleep(2)

            if is_content:              
                get_page_content(page_html)
                save_page_doc(items_links)
                sleep(2)
            else:
                break


    if __name__=='__main__':
        parser()