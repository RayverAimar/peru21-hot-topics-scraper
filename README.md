# Peru21 Hot-Topics Scraper
This project aims to scrape [Peru21](https://peru21.pe) current hot-topics notes and export themm in a json file if wanted.

## Usage
One cloned, make a Peru21Scraper instance and get the current hot-topics notes with .get method, which will return a dictionary type.

## Export
You can export the hot-topics notes in a JSON file with the .save method, which by default will create the 'hot_topics_peru21.json' file in the current directory.

## Manipulate
The general layout of both the JSON file and the dictionary is as follows:

| Hot-Topics Titles                           | Notes           | Part of note                       |
| ------------------------------------------- | --------------- |----------------------------------- |
| Available at .get_hot_topics_titles method  | 0-maximum_units | title, subtitle, content, datetime |

For more information about Hot-Topics Titles it is recommended to call .get_hot_topics_titles and save it in a list for later use.

You can also copy-paste the generated JSON file in some JSON formatter websites to see its layout like [bodurov](http://www.bodurov.com/JsonFormatter/) or [curiousconcept.com](https://jsonformatter.curiousconcept.com/#).


## Example

The following code uses a configuration for scraping Peru21 website with a maximum of 5 notes per topic and not considering opinions as they may be not as important as real notes.

```python
Scraper = Peru21Scraper(maximum_units=5, scrape_opinions=False)
hot_topics_dict = Scraper.get()
hot_topics_titles = Scraper.get_hot_topics_titles()
Scraper.save()
```

```bash
$ python .\peru21.scraper.py
['Adelanto de elecciones', 'Dina Boluarte', 'Protestas en Perú', 'Congreso', 'Bloqueo de vías']
Hot-Topics file saved successfully as 'hot_topics_peru21.json'
```