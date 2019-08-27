from core.celery import app
from apps.scraper.util_for_scraping import craulers


@app.task
def crauler(sites):
    if sites:
        for site in sites:
            getattr(craulers, site)()
    else:
        return 'Site not choice'
