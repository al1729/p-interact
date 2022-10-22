import asyncio
import streamlit as st 
import chronological
import openai
import os
import time
import aiofiles as aiof
from PIL import Image
import sys
import random
sys.path.append('/Users/andyliu/develop/p-interact')
# img = Image.open("p-interact-group.jpg")

# game.py imports
from game_for_streamlit import generate, init_story, options_generator, choose_story


#zac running with zac's secret:
import json


import os
import openai

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
#openai.api_key = ""
response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)

print('success')
# Stop Debug Logger Spam
chronological.logger.remove(None)
output = "outputs/story_output" + str(time.time()) + ".txt"

# var to save the current tldr, called in generateStory
current_tldr = ""


# you can name this function anything you want, the name "logic" is arbitrary
async def game_logic():
    header = st.container()

    dataset = st.container()
    features = st.container()
    modelTraining = st.container()


    my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3'])

    if my_page == 'page 1':
        with header:
            title_one = st.title("Welcome to our PAI project")
            # st.image(img, caption='Meet the team: Nolan, Maymuunah, Andy, David, and Zac')
            #st.markdown('The goal of our project is...')
            
    if my_page == 'page 2':
        st.title('Let\'s Play')
        old_text = ""

        

        story = await init_story() # we took out await
        # - FOR ANDY stuck on await
        st.markdown("<p style=font-size:18px><b>" + story + "</b></p>", unsafe_allow_html = True)
        count = 0
        #st.button("Begin Game", key=None, help=None, on_click=None, args=None, kwargs=None)
       # while count < 10:
        while True:
            st.markdown("<p style=font-size:18px><b>" + str(count) + "</b></p>", unsafe_allow_html = True)
            count += 1
               
            choices = await options_generator(story) # we took out await

            x = 1
            for choice in choices:
                st.markdown(str(x) + ". " + choice + "\n")
                x += 1

            try:
                # NOTE: getting streamlit to work with user_input is difficult b/c streamlit automatically 
                # reruns the entire script from the beginning after receiving input from a widget, e.g., user_input.
                # Have not been able to find a workaround for this issue yet, so that's why user input is currently
                # hard-coded
               # user_input = int(st.text_input("Enter your choice number: ", key=count))
               # time.sleep(5)
               # if user_input == '':
               #     time.sleep(5)
                user_input = random.choice([1,2,3,4])
                num = user_input - 1
                if num < 0 or num > x:
                    selected_choice = 1 # override
                else:
                    selected_choice = choices[num]
            except ValueError:
               # selected_choice = 1
                print("Please only input numbers for your choice, between 1 and 4")
                # Generate Chapter
                # moving temperature from 0.7-->0.3, frequency penalty from 0.5--->0.3
            result = await generate(story + selected_choice, max_tokens=200, temperature=0.3, frequency_penalty=0.3) # we took out await
               # # Return Chapter
            story += result
            st.markdown( "<p style=font-size:18px><b>" + story + "</b></p>", unsafe_allow_html = True)
    if my_page == 'page 3':
        st.title("Thank you for visting our PAI Project!")
        st.markdown('To learn more about PAI (Project AI) please check out https://www.p-ai.org/')

# invoke the Chronology main fn to run the async logic
chronological.main(game_logic)

