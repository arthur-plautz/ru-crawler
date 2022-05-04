import sys
from src.models.scraper import Scraper

if len(sys.argv) > 1:
    meal = sys.argv[1]
else:
    raise Exception('Target Meal is not defined!')

save_img = True if len(sys.argv) > 2 else False
page = 'https://sgpru.sistemas.ufsc.br/agendamento/home.xhtml'

scraper = Scraper(page, meal)
scraper.make_reservation(save_img)