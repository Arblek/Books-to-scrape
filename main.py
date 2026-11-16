from bs4 import BeautifulSoup
import requests
import pandas
import time

URL = "https://books.toscrape.com/"

rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}



def scrape_book(book_link, books_list):
    book_info = {"product_type": None,
                 "name": None, 
                 "price_no_tax": None,
                 "price_tax": None,
                 "tax": None,
                 "availability": None,
                 "rating": None,
                 "reviews_no": None,
                 "description": None
                 }

    book_page = requests.get(book_link, timeout=10)

    book_soup = BeautifulSoup(book_page.text, "html.parser")

    book_info["name"] = book_soup.find("div", class_="product_main").find("h1").text.strip()
    book_info["rating"] = rating_dict.get(book_soup.find("div", class_="product_main").find("p", class_="star-rating").get("class")[1])
    book_info["product_type"] = book_soup.find("table", class_="table").find("th", string="Product Type").find_next_sibling("td").text.strip()
    book_info["price_no_tax"] = book_soup.find("table", class_="table").find("th", string="Price (excl. tax)").find_next_sibling("td").text.strip()[1:]
    book_info["price_tax"] = book_soup.find("table", class_="table").find("th", string="Price (incl. tax)").find_next_sibling("td").text.strip()[1:]
    book_info["tax"] = book_soup.find("table", class_="table").find("th", string="Tax").find_next_sibling("td").text.strip()[1:]
    book_info["availability"] = book_soup.find("table", class_="table").find("th", string="Availability").find_next_sibling("td").text.strip()
    book_info["reviews_no"] = book_soup.find("table", class_="table").find("th", string="Number of reviews").find_next_sibling("td").text.strip()
    desc_div = book_soup.find("div", id="product_description")

    if desc_div:
        book_info["description"] = desc_div.find_next_sibling("p").text
    else:
        book_info["description"] = "No description available"

    books_list.append(book_info)

def get_no_pages(url):
    request = requests.get(url, timeout=10)
    soup = BeautifulSoup(request.text, "html.parser")

    return int(soup.find("ul", class_="pager").find("li", class_="current").text.split()[-1])


def get_all_the_link(number_of_pages):
    links = []
    for num in range(1, number_of_pages+1):
        request = requests.get(f"{URL}catalogue/page-{num}.html", timeout=10)
        soup = BeautifulSoup(request.text, "html.parser")
        list_holder = soup.find("ol", class_="row")
        element_list = list_holder.find_all("li")

        for element in element_list:
            links.append(f"{URL}catalogue/{element.find("h3").find("a").get("href")}")
    return links

def main():
    books = []
    number = get_no_pages(URL)
    links = get_all_the_link(number)
    for link in links:
        try:
            scrape_book(link, books)
            time.sleep(0.5)
        except Exception as e:
            with open("errors.log", "a", encoding="utf-8") as file:
                file.write(f"Error on page {link}. {type(e).__name__}")

    df = pandas.DataFrame(books)
    df.to_csv("books.csv", index=False)

main()