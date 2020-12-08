#%%
import requests

response = requests.get('https://www.spiced-academy.com/en/program/data-science')

html_string = response.text

print(html_string)

#%%
pip install BeautifulSoup4
#%%
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_string)
#%%
soup.body.find(class_='curriculum-middle').h3.text

#%%
for a in soup.body.find_all('a'):
    print(a.get('href'))

#%%
contact_section = soup.body.find(attrs={'id':'contact-us'})

contact_section