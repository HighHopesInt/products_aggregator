from pathlib import Path

from apps.main.main_utils import save_file
from apps.scraper.util_for_scraping import clear_dict
from apps.scraper.util_for_scraping import save_to_csv
from apps.scraper.util_for_scraping import (scraper_for_franco,
                                            scraper_for_saks)
from core.settings import SCRAPER_DIR
from apps.scraper.models import Site


def crawler_saks():
    url = Site.objects.get(title='Saks').url
    site = scraper_for_saks.scraper_saks(url)
    save_to_csv.save_to_csv(site, str(Path.home()) + SCRAPER_DIR +
                            'saks_shoes.csv')
    clear_dict.clear(site)
    save_file(str(Path.home()) + SCRAPER_DIR + 'saks_shoes.csv')


def crawler_franco():
    url = Site.objects.get(title='Franco Sarto').url
    site = scraper_for_franco.scraper_franco(url)
    save_to_csv.save_to_csv(site, str(Path.home()) + SCRAPER_DIR +
                            'franco_shoes.csv')
    clear_dict.clear(site)
    save_file(str(Path.home()) + SCRAPER_DIR + 'franco_shoes.csv')
