import requests
from bs4 import BeautifulSoup


def getPosts(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'html.parser')
    item_list = []

    for row in soup.find_all("div", class_="col-lg-6"):
        try:
            item_list.append({
                "title": row.find("div", class_="project-item").h3.a.get_text(),
                "url": row.find("div", class_="project-item").h3.a.get("href")
            })
        except:
            pass

    for row in soup.find_all("div", class_="col-lg-4"):
        try:
            item_list.append({
                "title": row.find("div", class_="project-item").h3.a.get_text(),
                "url": row.find("div", class_="project-item").h3.a.get("href")
            })
        except:
            pass

    return item_list
