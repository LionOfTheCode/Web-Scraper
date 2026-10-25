# Web Scraper

A learning project: a command-line web scraper built with `requests` and `BeautifulSoup`.
It crawls the catalogue of [Books to Scrape](http://books.toscrape.com/), finds books with a given
star rating and saves each book's description to a text file.

## Features

- Scrapes a user-defined number of catalogue pages (`page-1.html`, `page-2.html`, ...).
- Filters books by star rating (`One`, `Two`, `Three`, `Four` or `Five`).
- Saves every matching book description to `Page_<N>/<Book_Title>.txt` (UTF-8).
- Strips punctuation from titles and replaces spaces with underscores to build safe file names.
- Reuses one `requests.Session` for all requests and handles HTTP errors without stopping.

## Requirements

- Python 3.10 or newer (the code uses the walrus operator and the project runs on Python 3.14)
- `requests` and `beautifulsoup4`, which are the packages the scraper imports
- All project dependencies are listed in `requirements.txt`

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Run the scraper from the directory that contains `scraper.py`:

```bash
python scraper.py
```

The program reads two lines from standard input:

1. The number of catalogue pages to scrape.
2. The star rating to look for (`One`, `Two`, `Three`, `Four` or `Five`).

Example input:

```
2
Three
```

Example output:

```
Content saved.
...
Saved books:['Book_Title_1.txt', 'Book_Title_2.txt', ...]
```

## Output

The scraper creates one folder per catalogue page in the current working directory.
Each folder contains one text file per matching book:

```
Page_1/
├── Book_Title_1.txt
└── ...
Page_2/
└── ...
```

These folders and files are generated at runtime and are not part of the project.
If a folder already exists, its creation is skipped and files with the same name are overwritten.

## Project structure

| Path               | Description             |
|--------------------|-------------------------|
| `scraper.py`       | The scraper source code |
| `requirements.txt` | Python dependencies     |

## How it works

1. `retrieve_page` downloads a URL and raises an error on a bad HTTP status.
2. `get_book_links` parses a catalogue page and returns links to books with the requested rating.
3. `save_book_description_to_file` opens a book page, reads its title and description, and writes the description to a file.
4. `main` ties these together: it reads the input, loops over pages and handles errors.

## Future improvements

- **Tests:** write my own automated tests for the scraper functions.
- **Encapsulation:** group the scraping logic into a class or separate modules instead of standalone functions.
- Simplify `save_book_description_to_file` by splitting it into smaller functions.
- Add error handling for file writing.
- Validate the user input (page count and rating).
```