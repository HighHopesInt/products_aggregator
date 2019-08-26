from pathlib import Path

from apps.scraper.util_for_scraping import clear_dict
from apps.scraper.util_for_scraping import save_to_csv
from apps.scraper.util_for_scraping import (scraper_for_franco,
                                            scraper_for_saks)
from core.settings import SCRAPER_DIR
from core.celery import app


def crauler_saks():
    site = scraper_for_saks.scraper_saks()
    save_to_csv.save_to_csv(site, str(Path.home()) + SCRAPER_DIR +
                            'saks_shoes.csv')

    clear_dict.clear(site)


def crauler_fran():
    site = scraper_for_franco.scraper_franco()
    save_to_csv.save_to_csv(site, str(Path.home()) + SCRAPER_DIR +
                            'franco_shoes.csv')
    clear_dict.clear(site)


@app.task
def crauler(site_1, site_2):
    if site_1:
        crauler_saks()
    if site_2:
        crauler_fran()
