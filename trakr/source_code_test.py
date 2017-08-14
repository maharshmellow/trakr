import requests
from bs4 import BeautifulSoup
import hashlib

url = "https://www.wix.com/blog/2015/09/how-to-make-sure-your-business-is-found-on-google-2/"
try:
    html = requests.get(url, verify=False).text
except:
    print("Error")
soup = BeautifulSoup(html, "html.parser")

for script in soup(["script", "style"]):
    script.extract()

# get text
text = soup.get_text()
# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)

# print(text)
print(hashlib.md5(text.encode("utf-8")).hexdigest())
