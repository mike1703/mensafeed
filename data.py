import datetime
import locale
import lxml.html
import lxml.cssselect
from collections import defaultdict

mensa_url = "http://www.studentenwerk-muenchen.de/mensa/speiseplan/speiseplan_422_-de.html"
price_url = "http://www.studentenwerk-muenchen.de/mensa/unsere_preise/"

# returns a list of tupels of the format ("Mealname","Tagesgericht 1","vegetarian")
def get_meals():
	page = lxml.html.parse(mensa_url)
	day_sel = lxml.cssselect.CSSSelector("table.menu")
	date_sel = lxml.cssselect.CSSSelector("strong")
	menu_sel = lxml.cssselect.CSSSelector("td.beschreibung > span")
	price_sel = lxml.cssselect.CSSSelector("td.gericht")

	yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

	prices = get_prices()
	meals = defaultdict(list)
	days = [e.findall("tr") for e in day_sel(page)]
	for day in days: 
		date = datetime.datetime.strptime(date_sel(day[0])[0].text,"%A, %d.%m.%Y")
		if date < yesterday:
			continue

		for menu in day:
			meal = menu_sel(menu)
			meal_price = price_sel(menu)
			if len(meal) == 2:
				meals[date].append((			# date is key
					meal[0].text,			# name
					meal_price[0].text,		# price # TODO: replace pricename with real prices
					meal[1].attrib['title']))	# vegetarian
	return sorted(meals.items(),reverse=True)



# returns a list of tupels of the format ("Tagesgericht 1",["1.00","1.55","1.99"])
def get_prices():
	page = lxml.html.parse(price_url)
	categories_sel = lxml.cssselect.CSSSelector("table.essenspreise > tbody > tr")
	name_sel = lxml.cssselect.CSSSelector("th")
	value_sel = lxml.cssselect.CSSSelector("td")

	prices = {}
	for cat in categories_sel(page):
		name = name_sel(cat)[0].text
		values = value_sel(cat) # 0 -> students, 1 -> workers, 2 -> guests
		if len(values) == 3:
			prices[name] = (values[0].text,values[1].text,values[2].text) # TODO: filter only value of price
	return prices
