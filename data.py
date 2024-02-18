import requests
from bs4 import BeautifulSoup
import re


headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'data.gov.ma',
    'Referer': 'https://data.gov.ma/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_themes():
    theme = requests.get('https://data.gov.ma/data/group', headers=headers)
    th , nbs, links = (), (), ()
    if theme.status_code != 200:
        return th, nbs, links
    soup = BeautifulSoup(theme.text, features="lxml")
    media = soup.find('ul', class_='media-grid')
    thm = media.find_all('li', class_ = 'media-item')
    for m in thm:
        typ = m.find('h2').text
        nbr_donnees = m.find('strong', class_ = 'count').text
        nbr_donnees = re.findall(r'\d+',  nbr_donnees)
        link = m.find('a')['href']
        th, nbs, links = th + (typ,), nbs + (nbr_donnees[0],), links + ('https://data.gov.ma' + link,)
    return th, nbs, links

def get_producteurs():
    producteur = requests.get('https://data.gov.ma/data/organization', headers=headers)
    th , nbs, links = (), (), ()
    if producteur.status_code != 200:
        return th, nbs, links
    
    soup = BeautifulSoup(producteur.text, features="lxml")
    pages = len(soup.find('ul', class_='pagination').find_all('li'))
    if pages == 3:
        pages = 2
    else:
        pages = pages - 2
    for i in range(pages):
        producteur = requests.get(f'https://data.gov.ma/data/fr/organization/?q=&sort=&page={i+1}', headers=headers)
        if producteur.status_code != 200:
            return th, nbs, links
        soup = BeautifulSoup(producteur.text, features="lxml")
        media = soup.find('ul', class_='media-grid')
        thm = media.find_all('li', class_ = 'media-item')
        for m in thm:
            typ = m.find('h2').text
            nbr_donnees = m.find('strong', class_ = 'count').text
            nbr_donnees = re.findall(r'\d+',  nbr_donnees)
            link = m.find('a')['href']
            th, nbs, links = th + (typ,), nbs + (nbr_donnees[0],), links + ('https://data.gov.ma' + link,)
    return th, nbs, links

def verf_theme(theme):
    themes, nbrs, links = get_themes()
    theme = theme.lower()
    themes = [t.lower() for t in themes]
    if theme in themes:
        return True
    return False

def verf_producteur(producteur):
    producteurs, nbrs, links = get_producteurs()
    producteur = producteur.lower()
    producteurs = [t.lower() for t in producteurs]
    if producteur in producteurs:
        return True
    return False

def get_links_th(theme):
    if verf_theme(theme):
        themes, nbrs, links = get_themes()
        theme = theme.lower()
        themes = [t.lower() for t in themes]
        index = themes.index(theme)
        link = links[index]
    else:
        return [], [], [], []
    response = requests.get(link, headers=headers)
    if response.status_code != 200:
        return [], [], [], []
    soup = BeautifulSoup(response.text, features="lxml")
    if not soup.find('ul', class_='pagination'):
        titles, links, typ, description = get_data_link(link)
        return titles, links, typ, description
    pages = len(soup.find('ul', class_='pagination').find_all('li'))
    if pages == 3:
        pages = 2
    else:
        pages = pages - 1
    titles, links, typ, description = [], [], [], []
    for i in range(pages):
        response = requests.get(f'{link}?page={i+1}', headers=headers)
        if response.status_code != 200:
            return titles, links, typ, description
        soup = BeautifulSoup(response.text, features="lxml")
        media = soup.find('ul', class_='dataset-list list-unstyled')
        thm = media.find_all('li', class_ = 'dataset-item')
        for m in thm:
            lk = m.find('a')['href']
            links.append('https://data.gov.ma' + lk)
            title = m.find('h2').text.strip()
            titles.append(title)
            first = m.find('div', class_ = 'dataset-content')
            description.append(first.find('div').text.strip())
            tp = m.find('ul', class_ = 'dataset-resources list-unstyled').find_all('li')
            typ.append([ i.text.strip() for i in tp])
    return titles, links, typ, description
    
def get_data_link(link, titles = [], links = [], typ = [], description = []):
    response = requests.get(f'{link}', headers=headers)
    if response.status_code != 200:
        return titles, links, typ, description
    soup = BeautifulSoup(response.text, features="lxml")
    media = soup.find('ul', class_='dataset-list list-unstyled')
    thm = media.find_all('li', class_ = 'dataset-item')
    for m in thm:
        link = m.find('a')['href']
        links.append('https://data.gov.ma' + link)
        title = m.find('h2').text.strip()  
        titles.append(title)
        first = m.find('div', class_ = 'dataset-content')
        description.append(first.find('div').text.strip())
        tp = m.find('ul', class_ = 'dataset-resources list-unstyled').find_all('li')
        typ.append([ i.text.strip() for i in tp])
    return titles, links, typ, description


def get_links_pr(producteur):
    if verf_producteur(producteur):
        producteurs, nbrs, links = get_producteurs()
        producteur = producteur.lower()
        producteurs = [t.lower() for t in producteurs]
        index = producteurs.index(producteur)
        link = links[index]
    else:
        return [], [], [], []
    response = requests.get(link, headers=headers)
    if response.status_code != 200:
        return [], [], [], []
    soup = BeautifulSoup(response.text, features="lxml")
    if not soup.find('ul', class_='pagination'):
        titles, links, typ, description = get_data_link(link)
        return titles, links, typ, description
    pages = len(soup.find('ul', class_='pagination').find_all('li'))
    if pages == 3:
        pages = 2
    else:
        pages = pages - 1
    titles, links, typ, description = [], [], [], []
    for i in range(pages):
        response = requests.get(f'{link}?page={i+1}', headers=headers)
        if response.status_code != 200:
            return titles, links, typ, description
        soup = BeautifulSoup(response.text, features="lxml")
        media = soup.find('ul', class_='dataset-list list-unstyled')
        thm = media.find_all('li', class_ = 'dataset-item')
        for m in thm:
            lk = m.find('a')['href']
            links.append('https://data.gov.ma' + lk)
            title = m.find('h2').text.strip()
            titles.append(title)
            first = m.find('div', class_ = 'dataset-content')
            description.append(first.find('div').text.strip())
            tp = m.find('ul', class_ = 'dataset-resources list-unstyled').find_all('li')
            typ.append([ i.text.strip() for i in tp])
    return titles, links, typ, description

print(len(get_links_pr('HCP')[0]))