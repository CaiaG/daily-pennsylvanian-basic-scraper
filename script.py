"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    # req = requests.get("https://www.thedp.com")
    headers = {
        "User-Agent": "cis3500-scraper"
    }
    # req = requests.get("https://www.thedp.com", headers=headers)
    req = requests.get("https://www.thedp.com/section/news", headers=headers)

    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # my stuff!
        # articles = soup.find_all('h3', class_='standard-link')

        # extracted_data = []
        # for article in articles:
        #     link = article.find('a')
        #     if link:
        #         article_text = link.get_text(strip=True)
        #         article_url = link['href']
        #         extracted_data.append({"title": article_text, "url": article_url})

        # for data in extracted_data:
        #     loguru.logger.info(f"Title: {data['title']} | URL: {data['url']}")

        # return extracted_data     
        # target_element = soup.find("a", class_="frontpage-link")
        # data_point = "" if target_element is None else target_element.text
        # loguru.logger.info(f"Data point: {data_point}")

        # for cont. integration - extracting first headline from news page
        first_article = soup.find("h3", class_="headline")

        if first_article:
            headline_text = first_article.get_text(strip=True)
            loguru.logger.info(f"Scraped Headline: {headline_text}")
            return headline_text
        return ""


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
        loguru.logger.info("made data directory check")

    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
