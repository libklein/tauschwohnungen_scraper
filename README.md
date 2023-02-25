# Tauschwohnung Scraper

A simple scrapy-based scraper for [tauschwohnungen.com](https://tauschwohnungen.com).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Go to [tauschwohnungen.com](https://www.tauschwohnung.com/search) and configure your search. Then hit "search" and copy the URL. 

```bash
scrapy runspider scrape_tauschwohnung.py -a url="<pasted url>" --output tauschwohnungen.json:json
```

This will save all listings into `tauschwohnungen.json`. See `scrapy runspider -h` for supported command line arguments.
