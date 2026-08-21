import os
import string
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def retrieve_page(session, url):
    """Retrieve a page from a given URL."""
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response


def save_book_description_to_file(session, full_link_to_book, destination_folder):
    """Save a book description to a file to a specified folder.
    Takes a path to book as arguments and path to the destination folder.
       Returns the name of the book content file"""

    # TODO: Too complex. Simplify, cut into smaller functions.

    book_desc_page = retrieve_page(session, full_link_to_book)
    book_soup = BeautifulSoup(book_desc_page.content, "html.parser")
    book_title_tag = book_soup.find("h1")
    if not book_title_tag:
        return None

    book_title = book_title_tag.text.strip()

    book_content = ""

    if description_header := book_soup.find("div", id="product_description"):
        if p_tag := description_header.find_next_sibling("p"):
            book_content = p_tag.text

    for punctuation in string.punctuation:
        book_title = book_title.replace(punctuation, "")

    book_title = book_title.replace(" ", "_")
    file_path = os.path.join(destination_folder, f"{book_title}.txt")

    # TODO: Add error handling for file writing.
    with open(file_path, "wb") as file:
        file.write(book_content.encode("utf-8"))
        print("Content saved.")
        return f"{book_title}.txt"


def get_book_links(page, book_rating):
    """ Function scrapes description of a book. Function takes a page and book rating as arguments.
        Returns a list of links"""
    soup = BeautifulSoup(page.content, "html.parser")
    books_list = soup.find_all("article", class_="product_pod")

    links_list = []

    for book in books_list:
        if not book.find("p", class_=f"star-rating {book_rating}"):
            continue

        tag_with_link = book.select_one("h3 a")
        if tag_with_link and tag_with_link.get("href"):
            links_list.append(tag_with_link.get("href"))

    return links_list


def main():
    BASE_PATH = r"http://books.toscrape.com/catalogue/"

    pages_to_scrape = int(input())
    rating_to_scrape = input()

    # TODO: Implement request.Session() and improve usage. Better error handling.
    with requests.Session() as session:
        for page_number in range(1, pages_to_scrape + 1):
            page_url = urljoin(BASE_PATH, f"page-{page_number}.html")

            try:
                page = retrieve_page(session, page_url)
            except requests.HTTPError:
                print(f"Error retrieving page {page_url}.")
                continue

            books_links = get_book_links(page, rating_to_scrape)
            saved_books = []

            destination_folder = f"./Page_{page_number}"
            try:
                os.mkdir(destination_folder)
            except FileExistsError:
                print(f"Folder {destination_folder} already exists. Skipping creation.")

            for book_link in books_links:
                try:
                    saved_books.append(
                        save_book_description_to_file(session, urljoin(BASE_PATH, book_link), destination_folder))
                except requests.HTTPError:
                    print(f"Error saving book description for {book_link}.")
                    continue
            print(f"Saved books:{saved_books}")


if __name__ == "__main__":
    main()
