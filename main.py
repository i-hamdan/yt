import re
from apiclient.discovery import build
import streamlit as st

libraries = 'sudo pip install --upgrade google-api-python-client'
st.title('YouTube Affiliate Extractor')
st.header('WebApp by Hamdan Iftikhar')

key = 'AIzaSyAQ2rv87fYjYHD1v1ZTUBjcvcEu2cJqCzQ'


st.write('')
st.write('')
def getDes(url):
  pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
  temp = re.search(pattern, url)
  if temp:
    id = temp.groups()[0]
  youtube = build('youtube', 'v3', developerKey=key)
  results = youtube.videos().list(id=id, part='snippet').execute()
  for result in results.get('items', []):
    return(result['snippet']['description'])

def getLinks(desc):
  links = []
  linesWithLinks = []
  lines = desc.splitlines()
  for line in lines:
    link_obj = re.search("(?P<url>https?://[^\s]+)", line)
    if(link_obj):
      link = link_obj.group("url")
      if 'youtu' not in link:
        if 'twit' not in link:
          if 'inst' not in link:
            if 'face' not in link:
              linesWithLinks.append(line)
              links.append(link)
  return links, linesWithLinks


url = st.text_input('Please enter the video URL',
                      'https://www.youtube.com/watch?v=-EZ_3Tq9a8c')

desc = getDes(url)
links, linesWithLinks = getLinks(desc)

col1, col2 = st.columns(2)

with col2:
  st.header("Descriptive links:")
  b1 = st.button('Print', key = 1)
  if b1:
    for link in linesWithLinks:
      st.write(link)

with col1:
  st.header("Extracted links")
  b2 = st.button('Print', key = 2)
  if b2:
    for link in links:
      st.write(link)

st.write()
