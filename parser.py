import requests
import re
from bs4 import BeautifulSoup

url = "https://city4people.ru/posts/tag/%D0%BF%D0%B5%D1%88%D0%B5%D1%85%D0%BE%D0%B4%D1%8B"
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
urls = []

for row in soup.find_all("div", class_="col-lg-6"):
    try:
        urls.append({
            "title": row.find("div", class_="project-item").h3.a.get_text(),
            "url": row.find("div", class_="project-item").h3.a.get("href")
        })
    except:
        pass

for row in soup.find_all("div", class_="col-lg-4"):
    try:
        urls.append({
            "title": row.find("div", class_="project-item").h3.a.get_text(),
            "url": row.find("div", class_="project-item").h3.a.get("href")
        })
    except:
        pass

# for row in soup.find_all("div", class_="col-lg-6"):
#     # print(row.find_all("div", class_="project-item"))
#     try:
#         urls.append({
#             "url": row.find("div", class_="project-item").find("div", class_="project-img").a.get("href")
#         })
#     except:
#         pass

# for row in soup.find_all("div", class_="col-lg-4"):
#     try:
#         urls.append({
#             "url": row.find("div", class_="project-item").find("div", class_="project-img").a.get("href")
#         })
#     except:
#         pass

print(urls)

# print(soup.find("div", {"class": "row"})[0].div["col-lg-6"][0].project-item.h3.a.get("href"))

