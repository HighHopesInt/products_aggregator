from core.celery import app
from apps.scraper.util_for_scraping import craulers


@app.task
def crauler(sites):
    for site in sites:
        getattr(craulers, site)()
    print('Done')
