from core.celery import app
from apps.scraper.util_for_scraping import crawlers


@app.task
def crauler(sites):
    for site in sites:
        getattr(crawlers, site)()
    print('Done')
