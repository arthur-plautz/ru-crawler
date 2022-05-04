import sys
from src.models.scraper import Scraper

page = 'https://sgpru.sistemas.ufsc.br/agendamento/home.xhtml'
meal = sys.argv[1]
save_img = True if len(sys.argv) > 2 else False

scraper = Scraper(page, meal)
scraper.make_reservation(save_img)