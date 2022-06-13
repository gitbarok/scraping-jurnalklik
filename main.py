# Load the package
from unittest import result
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def scrape_jurnal_klik(name_output):
    # declare url target
    url = 'http://klik.ulm.ac.id/index.php/klik/issue/archive'

    #
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='issues')

    # get all link from the archive and stored in links as a list
    links = []
    archive_links = results.find_all('a')
    for element in archive_links:
        links.append(element.get('href'))

    paper = {
        'title': [],
        'author': [],
        'link': [],
    }

    for link in tqdm(links):
        page_a = requests.get(link)
        results_a = BeautifulSoup(page_a.content, 'html.parser')
        allArticle = results_a.find_all('table', class_='tocArticle')
        # allAuthors =  allArticle.find_all('td', class_='tocArticleTitleAuthors')

        for content in tqdm(allArticle):
            #using try except to handle diff element in links[18]
            try:
                paper_title = content.find('div', class_='tocTitle').text
                paper_author = content.find('div', class_='tocAuthors').text.strip()
                paper_link = content.find('a').get('href')
                paper['title'].append(paper_title.replace('\n', ''))
                paper['author'].append(paper_author.replace('\t', ''))
                paper['link'].append(paper_link)
            except:
                pass


    df = pd.DataFrame.from_dict(paper)

    df.to_csv(name_output, index= False)

if __name__ == '__main__':
    scrape_jurnal_klik('result.csv')