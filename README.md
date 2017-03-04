# Recipe-scraper

## Description
recipe-scraper is a project that uses Scrapy, a Python library, to scrape
various websites for recipes. Spiders (web crawlers written in Scrapy) are used
to output scraped data.

## Contributing
Fork this repository, push to your fork, and submit a pull request.

## Dependencies and Setup
Have the following installed:
- Python
- pip

To set up:
1. Clone the repository
2. If desired, set up a Python virtual environment and activate it.
3. Run the following command to install other dependencies:
```
pip install -r requirements.txt
```

## Running a spider
"Spiders", or Scrapy's web crawlers, are located in recipe_scraper/spiders. To
run one, cd to the top level of the repository and type this in the shell:
```
scrapy crawl [spider_name] -o [output_filename].json
```

where spider_name is the name of a spider (spider_name attribute within each
spider class) and output_filename is the desired filename.

This will run the crawler and output the results in json format.

## Licensing
This software is licensed under the MIT license. It makes use of Scrapy, a
Python library licensed under the BSD-3-Clause license. A copy of Scrapy's
license is included in full on the repository.
