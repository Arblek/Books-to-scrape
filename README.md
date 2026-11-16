# Books to Scrape

A Python web scraper that collects the full catalogue of [books.toscrape.com](https://books.toscrape.com/) (a practice site built for scraping) and saves it as a clean CSV file.

It visits every listing page, opens each book's detail page, extracts the product data, and writes everything to `books.csv`.

## What it extracts

For each of the 1,000 books:

| Column | Description |
| --- | --- |
| `product_type` | Product type from the details table |
| `name` | Book title |
| `price_no_tax` | Price excluding tax (£) |
| `price_tax` | Price including tax (£) |
| `tax` | Tax amount (£) |
| `availability` | Stock text, e.g. "In stock (22 available)" |
| `rating` | Star rating converted to a number, 1 to 5 |
| `reviews_no` | Number of reviews |
| `description` | Book description, or "No description available" |

A ready-made `books.csv` from a full run is included in this repository.

## How it works

1. Reads the pager on the home page to find how many listing pages exist.
2. Collects the link to every book from each listing page.
3. Downloads each book page and parses it with BeautifulSoup.
4. Converts the star rating from its CSS class name ("Three") to a number (3).
5. Saves the results with pandas to `books.csv`.

**Reliability and politeness**
- Waits 0.5 seconds between book requests so the server is not hammered.
- Uses a 10-second timeout on every request.
- If a single page fails, the error is appended to `errors.log` and the scraper moves on, so one bad page does not stop the whole run.

## Requirements

- Python 3.12 or newer
- `requests`, `beautifulsoup4`, `pandas`

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

```bash
python main.py
```

A full run requests about 1,050 pages with a short pause between book pages, so expect it to take around ten minutes. It overwrites `books.csv` when it finishes.

## Project structure

```
main.py     # scraper: pagination, book parsing, CSV export
books.csv   # output from a full run (1,000 books)
```