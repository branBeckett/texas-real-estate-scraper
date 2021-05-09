# Texas Real Estate Web Scraper

### Web Scraper for Texas Real Estate Water District and Bond Info

I built this web scraper in October 2020 for a Title company in Austin, Texas. This script is currently used on a weekly basis to scrape data from a table on a website that contains up-to-date real estate, water district, and bond information for the entire state of Texas.

Running this script automatically requests the most up to date table data, and returns that data with formated columns into a comma separated value file (.csv). 
After running the script, you will find the file in your working directory with today’s date in the filename.

This script requires that `pandas`, `beautiful soup`, `requests`, `regex`, and `datetime` be installed within the Python environment.

Note that the URL has been removed. Permission is required to scrape the original website. Feel free to message me if you'd like access to the source URL.
