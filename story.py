#* The imports
import os
import requests
from bs4 import BeautifulSoup
import random
from gtts import gTTS

# Setting the base URL
URL = "https://americanliterature.com/short-short-stories"
# Initializing the headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
          }

#* The main function
def getStory():
    # Getting the page
    page = requests.get(URL, headers=headers)
    # The BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')
    #* The titles
    titles = []
    titlesGot = soup.find_all('a', class_="sslink", href=True)
    for title in titlesGot:
        titles.append(title.text)
    #* The story which is selected
    story = random.choice(titles)
    #* Printing the name
    storyOK = input(f"The story that you will be read is '{story}'. Is that Okay? y/n: ")
    #* Does the user want to continue
    if storyOK == "y":
        #* Getting the story link
        for a in titlesGot:
            if a.text == story:
                storyL = a['href']
        listenStory(storyL)
    elif storyOK == "n":
        titles.clear()
        getStory()

#* Listening to the story
def listenStory(storyLink):
    #* The language for speaking
    lang = 'en'
    #* Getting the story text
    storyL = "https://americanliterature.com/" + storyLink
    # Getting the page
    page = requests.get(storyL, headers=headers)
    # The BeautifulSoup object
    soup = BeautifulSoup(page.content, 'html.parser')
    #* All the paragraphs
    paragraphs = soup.find_all('p')
    #* The story text
    story = ""
    #* Appending
    for para in paragraphs:
        story += str(para.text)
    #* The object
    Speech = gTTS(text=story, lang=lang, slow=False)
    #* Saving the audio
    Speech.save("story.mp3")
    #* Making it speak
    os.system("mpg321 story.mp3")

#* Calling the main function
getStory()