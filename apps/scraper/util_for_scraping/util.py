from apps.scraper.util_for_scraping import clear_dict
from apps.scraper.util_for_scraping import save_to_csv
from . import scraper_for_franco, scraper_for_saks


def crauler_saks(request):
    site = scraper_for_saks.scraper_saks(request)
    save_to_csv.save_to_csv(site, 'saks_shoes')
    clear_dict.clear(site, request)


def crauler_fran(request):
    site = scraper_for_franco.scraper_franco(request)
    save_to_csv.save_to_csv(site, 'franco_shoes')
    clear_dict.clear(site, request)
