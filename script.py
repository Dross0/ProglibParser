import requests
from bs4 import BeautifulSoup
import csv


themes = {'C#': 'csharp',
          'C++': 'cpp',
          'Data science': 'data-science',
          'Hacking': 'hacking',
          'Java': 'java',
          'Linux': 'linux',
          'Mobile': 'mobile',
          'Python': 'pytnon',
          'Web': 'web',
          'Algoritms': 'algoritms',
          'Beginner': 'novice',
          'Common': 'common',
          'Other': 'miscellaneous',
          'Game development': 'gamedev',
          'Work': 'work'}

print('Список команд:')
for name in themes.keys():
    print(name)

user_command = input('Введите команду: ')
if user_command in themes.keys():
    user_input = themes[user_command]
else:
    print('\nПерезапустите программу и введите команду из списка!')
    exit(1)

url = 'https://proglib.io/p/tag/{}/'.format(user_input)



def get_html(url):
    r = requests.get(url)
    return r.text

def get_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup

def get_number_of_pages(soup):
    page_nav = soup.find('div', class_='page-nav td-pb-padding-side')
    if page_nav != None:
        number_of_last_page = page_nav.find_all('a')[-2].get('title')
        return int(number_of_last_page)
    return 0


def get_list_of_articles(soup):
    all_content = soup.find('div', class_='td-ss-main-content')
    articles = all_content.find_all('div', class_='item-details')
    return articles


def parsing_of_each_page(number_of_last_page):
    articles_on_non_first_page = []
    for page in range(2, number_of_last_page + 1):
        URL = url + 'page/{}/'.format(page)
        html = get_html(URL)
        soup = get_soup(html)
        articles_on_non_first_page.extend(get_list_of_articles(soup))
    return articles_on_non_first_page


def get_links_list(articles):
    links = []
    for article_link in articles:
        links.append(article_link.find('a').get('href'))
    return links

def get_titles_list(articles):
    titles = []
    for article_title in articles:
        titles.append(article_title.find('a').get('title'))
    return titles

def get_description_list(articles):
    descriptions = []
    for article_descr in articles:
        decsr = article_descr.find('div', class_='td-excerpt').string.strip().replace(u'\xa0', u' ')
        descriptions.append(decsr)
    return descriptions


def write_csv(titles, links, descriptions):
    with open('articles.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = ['',user_input.upper(), '']
        writer.writerow(row)
        row = ['Заголовок', 'Описание', 'Ссылка']
        writer.writerow(row)
        for article in range(len(titles)):
            row = []
            row.append(str(titles[article]))
            row.append(str(descriptions[article]))
            row.append(str(links[article]))
            writer.writerow(row)



def main():
    html = get_html(url)
    soup = get_soup(html)
    number_of_last_page = get_number_of_pages(soup)   #if 0 -- only one page
    articles = get_list_of_articles(soup)  #first page

    if number_of_last_page != 0:
        articles.extend(parsing_of_each_page(number_of_last_page))

    titles = get_titles_list(articles)
    links = get_links_list(articles)
    descriptions = get_description_list(articles)
    write_csv(titles, links, descriptions)




if __name__ == '__main__':
    main()