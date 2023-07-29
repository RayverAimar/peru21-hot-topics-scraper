from bs4 import BeautifulSoup
import requests
import json

class Peru21Scraper(object):
    def __init__(self, maximum_units=5, scrape_opinions=False):
        self.__url = "https://peru21.pe"
        self.dict_hot_topics = {}
        self.__maximum_units = maximum_units
        self.__must_not_contain = 'OPINIÓN' if not scrape_opinions else ''
        self.hot_topics_titles = []

    def __get_soup(self, url, parser='lxml'):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, parser)
        return soup
    
    def __get_links_and_titles(self, sections):
        links = []
        self.hot_topics_titles = []
        for section in sections:
            title = section.a.get_text()
            links.append(section.a.get('href'))
            self.hot_topics_titles.append(title)
            if len(links) == self.__maximum_units:
                break
        return links, self.hot_topics_titles
    
    def __get_links_titles_datetime_of_news(self, sections):
        links = []
        titles = []
        datetimes = []
        for section in sections:
            if '21' in section.a.get_text():  # 'La voz del 21' tends to use a different website than what a normal note uses so it is not handeable by the moment
                continue
            datetime = section.find('p', attrs={'class':'story-item__date'}).get_text()
            section = section.find('h2')
            title = section.a.get_text()
            if self.__must_not_contain and self.__must_not_contain.lower() in title.lower():
                continue
            links.append(section.a.get('href'))
            titles.append(title)
            datetimes.append(datetime)
            if len(links) == self.__maximum_units:
                break
        return links, titles, datetimes
    
    def __get_title_subtitle_content_of_news(self, soup):
        title = soup.find('h1').get_text()
        subtitle = soup.find('h2', attrs={'class': 'sht__summary'}).get_text()
        content = soup.find('div', attrs={'class': 'story-contents__content'}).get_text()
        content = content.replace('VIDEO RECOMENDADO', '') # Delete last two words from content
        return title, subtitle, content
    
    def get(self):
        soup = self.__get_soup(self.__url)
        hot_sections = soup.find('ul', attrs={'class':'header__featured'}).find_all('li')[1:] # Section "Lo último" is a mix of non-interesting topics
        hot_sections_links, hot_sections_titles = self.__get_links_and_titles(hot_sections)

        for index, title in enumerate(hot_sections_titles):
            soup_current_topic = self.__get_soup(hot_sections_links[index])
            notes = soup_current_topic.find('div', attrs={'class':'paginated-list paginated-list--default'}).find_all('div', attrs={'class':'story-item__left'})
            notes_links, notes_titles, notes_datetimes = self.__get_links_titles_datetime_of_news(notes)
            notes_links = [self.__url + note for note in notes_links] # Re-Build link as it may be relative

            dict_notes_current_topic = {}

            for index, note_link in enumerate(notes_links):
                dict_current_note = {}
                soup_current_topic = self.__get_soup(note_link)
                dict_current_note['title'], dict_current_note['subtitle'], dict_current_note['content'] = self.__get_title_subtitle_content_of_news(soup_current_topic)
                dict_current_note['datetime'] = notes_datetimes[index]
                dict_notes_current_topic[index] = dict_current_note

            self.dict_hot_topics[title] = dict_notes_current_topic
        return self.dict_hot_topics

    def print_current_hot_topics(self):
        if not self.hot_topics_titles:
            soup = self.__get_soup(self.__url)
            hot_sections = soup.find('ul', attrs={'class':'header__featured'}).find_all('li')[1:] # Section "Lo último" is a mix of non-interesting topics
            self.__get_links_and_titles(hot_sections)
    
        print("Current hot-topics in Peru21 are listed below:")
        for title in self.hot_topics_titles:
            print('\t', title)    
    
    def get_hot_topics_titles(self):
        if not self.hot_topics_titles:
            soup = self.__get_soup(self.__url)
            hot_sections = soup.find('ul', attrs={'class':'header__featured'}).find_all('li')[1:]
            self.__get_links_and_titles(hot_sections)
        return self.hot_topics_titles
    
    def save(self, title="hot_topics_peru21.json"):
        with open(title, "w") as outfile:
            json.dump(self.dict_hot_topics, outfile)
        print(f'Hot-Topics file saved successfully as \'{title}\'')

Scraper = Peru21Scraper(maximum_units=5, scrape_opinions=False)
hot_topics_dict = Scraper.get()
Scraper.save()