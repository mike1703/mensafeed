#!/usr/bin/env python
import data
import datetime
import lxml.objectify
import lxml.etree

def create_feed(meals):
	E = lxml.objectify.ElementMaker(annotate=False)
	channel = E.channel(
			E.title("Mensa-RSS-Feed"),
			E.description("Was gibt es in der Mensa im Garchinger Forschungszentrum zu Essen?"),
			E.link("")
		)

	for (date,day_meals) in meals:
		item = E.item(
			E.title(datetime.datetime.strftime(date,"%d.%m: ") + ", ".join([name for (name,_,_) in day_meals])),
			E.description("; ".join([price + ": " + name for (name,price,_) in day_meals])),
			E.pubDate(date)
			)
		channel.append(item)

	rss = (E.rss(channel, version='2.0'))

	return lxml.etree.tostring(rss, xml_declaration=True, encoding="UTF-8")

def main():
	meals = data.get_meals()
	print create_feed(meals)

if __name__ == '__main__':
	main()
