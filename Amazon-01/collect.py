from bs4 import BeautifulSoup
import os
import pandas as pd

d = {'title': [], 'price': [], 'link': []}

for file in os.listdir("data"):
    try:
        with open(f"data/{file}", encoding="utf-8") as f:
            html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, "html.parser")
        t = soup.find("h2")
        title = t.get_text() if t else ""
        
        l = t.find("a") if t else None
        link = "https://amazon.in" + l["href"] if l and "href" in l.attrs else ""
        
        p = soup.find("span", attrs={"class": "a-price-whole"})
        price = p.get_text() if p else ""
        
        d['title'].append(title)
        d['price'].append(price)
        d['link'].append(link)
        
    except Exception as e:
        print(e)

df = pd.DataFrame(data=d)
df.to_csv("data.csv", index=False)