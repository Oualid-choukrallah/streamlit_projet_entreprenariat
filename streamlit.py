import random
import re

import streamlit as st
import scrapetube
import openai
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup
from pytube import YouTube
import requests
from PIL import Image
import numpy as np
import pandas as pd

openai.api_key = "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"
st.set_page_config(layout="wide")


#Functions
HEADER = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
}

Titles = []
liste = []
images = []


def videos_channels(Id):
    videos = scrapetube.get_channel(Id)
    url = "https://www.youtube.com/watch?v="

    for video in videos:
        url1 = url + str(video["videoId"]) + "/videos"
        response = requests.get(url1, headers=HEADER)
        soup = BeautifulSoup(response.text, "html.parser")

        thumbSoupMeta = soup.find("meta", property="og:image")
        videoImage = thumbSoupMeta["content"] if thumbSoupMeta else "NotFound"
        videoImage = '<img src="' + videoImage + '" width="60" >'

        yt = YouTube(url1)
        Titles.append(yt.title)
        liste.append(url1)
        images.append(videoImage)
        data1 = pd.DataFrame({'Titres': Titles[:10]})
    return(data1)




##Left sidebar menu

with st.sidebar:
    image = Image.open('logo.png')
    st.image(image)
    choose = option_menu("Café innatendu", ["Rechercher", "Home", "Idée sauvegardées", "mes analyse", "Paramètres"],
                         icons=['search', 'house', 'joystick', 'graph-up', 'gear-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                             "icon": {"color": "orange", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         }

                         )
    analyse = st.button('+ Nouvelle Analyse', key=None, help=None, on_click=None, args=None, kwargs=None,
              disabled=False)

if choose == "Home":
    st.title("Nouvelle Analyse")
    id_title = st.text_input("Nom de l'analyse :")
    id_channel = st.text_input("ID de la chaîne")
    id_video = st.text_input("URL de vidéo","http://youtu.be/...")
    id_tags = st.text_input("Tags","Ajouter un mot clé")

id_title = "Ma prochaine vidéo"
id_channel = "UCejCKksK_riq-2Q3rqTnqAA"




if id_title :
    if id_channel :
        a = id_channel
        data = videos_channels(a)
        prompt = "donne moi 12 idées de vidéos similaires :"
        prompt_2 = ""
        for i in range (1,len(data)) :
            prompt_2 = prompt_2 + f"\n{i}.{data['Titres'][i]}"

        prompt_final = prompt + f"\n" + prompt_2
        response = openai.Completion.create(engine="text-davinci-001", prompt=prompt_final, max_tokens=200)
        response_ideas = response["choices"][0]["text"]
        ideas = {"Ideas": [],"Similar":[],"Interest":[],"Concurence":[]}
        split_ideas = re.split(r"\d\.",response_ideas)
        for i in range(1,len(split_ideas)) :
            ideas["Ideas"].append(split_ideas[i])
            ideas["Similar"].append(random.randrange(2,10,1))
            ideas["Interest"].append(f"{random.randrange(10,80,3)}%")
            ideas["Concurence"].append(f"{random.randrange(3,9,1)}/10")
        df_ideas = pd.DataFrame(ideas)
        if choose == "mes analyse":
            st.subheader(f"📚 Mes analyses/{id_title}")
            st.title(f"{id_title}")
            st.header(f"💡 Idée générées")
            col1, col2, col3, col4 = st.columns(4)
            with col1 :
                st.write("Idées sauvgardées")
                for i in range(len(df_ideas)):
                    st.checkbox(df_ideas["Ideas"][i])
            with col2 :
                st.write("Nb vidéo similaire")
                for i in range(len(df_ideas)):
                    st.write(df_ideas["Similar"][i])
            with col3:
                st.write("Score d'intérêt")
                for i in range(len(df_ideas)):
                    st.write(df_ideas["Interest"][i])
            with col4:
                st.write("Score Conccurentiel")
                for i in range(len(df_ideas)):
                    st.write(df_ideas["Concurence"][i])


























