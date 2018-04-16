# Beer Advocate Scrapper

## Overview

First attempt at creating a python web scraper script. Used on beeradvocate to scrap for local breweries and each
breweries beers and stored them in a SQL database for use in a Baltimore brewery tour web app.

## Modules

- **Beautiful Soup 4** - Used to parse webpages and get contents
- **Urllib2** - A backup parser, used when the default `html.parser` was not parsing all contents
- **PyMySQL** - Used to insert scrapped data into SQL database