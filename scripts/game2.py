import chronological
import openai
import os
import time
import aiofiles as aiof
import pandas as pd

# module for command line argument used to specify whether or not you're running game.py for test data generation
import argparse

# command line arguments
parser = argparse.ArgumentParser()
# command line arg for specifying whether or not game.py is being run for test data generation
parser.add_argument('--testData', help="set to true if running game.py for test data generation")
# command line arg for specifying temperature parameter for generate function
parser.add_argument('--temp', type=float, default=0.3, help="set the temperature parameter for generate function (number between 0.0-1.0)")
# command line arg for specifying top_p parameter for generate function
parser.add_argument('--top_p', type=float, default=1, help="set the top_p parameter for generate function (number between 0.0-1.0)")
# command line arg for specifying frequency_penalty parameter for generate function
parser.add_argument('--freq_pen', type=float, default=0.3, help="set the frequency_penalty parameter for generate function (number between -2.0 and 2.0)")

# presence_penalty parameter for generate function
parser.add_argument('--pres_pen', type=float, default=0, help="set the presence_penalty parameter for generate function (number between 0 and 2.0)")
args = parser.parse_args()



#zac running with zac's secret:
import json
def get_keys(path):
    with open(path) as f:
       return json.load(f)

keys = get_keys(r"C:\Users\zac\OneDrive\Documents\GitHub\p-interact\secret.json")


import os
import openai

# Load your API key from an environment variable or secret management service
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = keys['OPENAI_API_KEY']
response = openai.Completion.create(engine="text-davinci-001", prompt="This is a test", max_tokens=5)



print('success')
# Stop Debug Logger Spam
chronological.logger.remove(None)
output = "outputs/story_output" + str(time.time()) + ".txt"

# for writing story output to test_outputs dir instead of outputs dir when testData arg is provided
test_output="test_outputs/story_output" + str(time.time()) + ".txt"

# var to save the current tldr, called in generateStory
current_tldr = ""



# generate summary state of most recently generated story
# take from tldr? maybe add more methods later. Maybe add the table method.
# when updating summary state to get new tldr feed it new input story and old tldr story
# use update_tldr for initial generation as well as updating
# some way of s
# newStory --> str
# firstStory --> bool
# tldrSummary --> str
# added updating current_tldr variable

import string
import random
def random_upper_char():
    #maybe needs to be async defed
    #string.ascii_uppercase
    #print(string.ascii_uppercase)
    random_letter = random.choice(string.ascii_uppercase)
    random_letter = str(random_letter)
    #print("test", str(random_letter))
    return(str(random_letter))
import re
async def gen_table_char_summary_states(max_tokens=300, temperature=0.3, top_p=1, frequency_penalty=0.3, firstStory=True, tldrSummary=""):
    #pre first story
    if firstStory:
        #generating characteristics, parse alive status, setting/scene
        #make gpt-3 do it, prompt design
        #give gpt-3 a blank row and fill it out.
        #this is a list of characters in a fantasy story
        #name alive profession magic_user
        #zac note parse list of characters and save each characters characteristics in a dictionary, so list of dictionaries
        #Entity Recognizer Spacy https://spacy.io/api/entityrecognizer

        table_prompt = "The following table includes characteristics of characters in a fantasy short story. Generate more characters:\r\nname | alive | profession | magic_user | species | gender | age\r\nBob | alive | blacksmith | no | human | man | 19\r\nTom | dead | mage | yes | elf | woman | 38\r\n"+random_upper_char()+"\r\n"+random_upper_char()+"\r\n"+random_upper_char()+"\r\n"+random_upper_char()+"\r\n"+random_upper_char()+"\r\nS"
        table_result = await chronological.cleaned_completion(table_prompt, max_tokens=max_tokens,
                                                    engine="text-davinci-001",
                                                    temperature=temperature,
                                                    top_p=top_p,
                                                    frequency_penalty=frequency_penalty)
        #print(table_result)
        
        #remove two example lines of Bob and Tom from final table
        #something like this, but this over deletes:
        '''
        table_result = re.sub(r"Bob | alive | blacksmith | no | human | man | 19\r\nTom | dead | mage | yes | elf | woman | 38\r\n,", "",table_result)
        '''
        print(table_result)
        return(table_result)
        
        #old pandas dataframe code. maybe still needed?
        '''
        for char in list_of_chars:
            ss_char_table_initial[char] = {'name':[], 'alive':[],'profession':[],'magic_user':[],'species':[],'gender':[], 'age':[]}
            df[char] = pd.Dataframe(data=d)
            df[char]
        '''
        #settings table
        '''
        ss_setting_table_initial = {'past_scene':[],'setting':[],'genre':[]}
        setting_df = pd.Dataframe(data=d)
        '''
    else:
        print('error in gen_table_char_summary_states')




#moving freqneyc penalty from 0.5-->0.3, temp from 0.5-->0.3
async def generate(prompt, max_tokens=100, temperature=1, top_p=1, frequency_penalty=1.6, presence_penalty = 1, stop=["\n\n"]):
    result = await chronological.cleaned_completion(prompt,
                                                    max_tokens=max_tokens,
                                                    engine="text-davinci-001",
                                                    temperature=temperature,
                                                    top_p=top_p,
                                                    frequency_penalty=frequency_penalty,
                                                    presence_penalty = presence_penalty,
                                                    stop=stop)
    return result

table_explain = 'This is a table with characters and their characteristics in a fantasy short story:\r\n'
async def init_story(table_result):
    #Zac 12-3-2021 user input to choose genre
    #I think I forgot/don't understand how the prompt reading is working/I need to change it because its reading text file names, so maybe it needs to load the text file then I add the genre as an additiona line?
    #if genre input use:
    #print('please input your desired genre, if no genre input na')
    #genre_id = input()
    #if no genre input use:

    genre_id = 'na'
    if genre_id.lower() == 'na':
        prompt_id = 'example_prompt'
    else:
        genre_prompt = 'This is the beginning of a '+ genre_id + ' story: ' 
        #improve genre_prompt/general syntax from here: https://docs.google.com/document/d/1SNYITOoTsy_DgvVI-mCg3XucUTSB82n6URmRBwLicQQ/edit


        #probably needs a line break here
        # Default prompt
        prompt_id = ''
        prompt_id = genre_prompt + prompt_id
        print('test', prompt_id)
        #generates a new text file with the prompt id
        file_name = prompt_id+'.txt'
        print(file_name)
        file_path = 'prompts\\'
        completeName = os.path.join(file_path, file_name)
        print(completeName)
        text_file = open(completeName, 'w')
        
    

    # User input to choose prompt

    # you call the Chronology functions, awaiting the ones that are marked await
    # read_prompt() looks in prompts/ directory for a text file. Pass in file name only, not extension.
    # Example: prompts/hello-world.txt -> read_prompt('hello-world')
    prompt = chronological.read_prompt(prompt_id)

    # new method generate its own prompt, ignore the read prompt_id from example_prompt:

    prompt = table_explain+table_result+'\r\nWrite the beginning of a fantasy story with the characters in the table'
    print('table fed story 1')

    # if temp/top_p/frequency_penalty are specified using command line arguments, then those specified values will be passed into 
    # the generate function. If they aren't specified, then the default values for temp/top_p/frequency_penalty  will be passed 
    # into the generate function.
    result = await generate(prompt, temperature=args.temp, top_p=args.top_p, frequency_penalty=args.freq_pen, presence_penalty=args.pres_pen)
    print(result)

    story = prompt + ' ' + result

    # Return Initial Story
    return story

'''
#here for reference
async def options_generator(prompt):
    choices = await options_generator(input_story)
    results = []
    # Generate 4 story options
    for i in range(4):
        #param test moving temp from 0.5 --> .3, and 0.5-->0.3 freqencuy pentalty
        #appears to not generate them
        res_gened = generate(prompt, max_tokens=50, temperature=0.3,
                       frequency_penalty=0.3, stop=["\n\n\n\n\n"])
        print(res_gened)
        results.append(res_gened)
        print(results)
    choices = await chronological.gather(*results)
    return choices
           async with aiof.open(output, mode='a') as f:
                await f.write("input: " + selected_choice)
                await f.write('\n\n\n')
                await f.close()
'''
# David name searching code:
#____________
import spacy
# from spacy.lang.en.examples import sentences 

nlp = spacy.load("en_core_web_sm")
#david file open
#file = open(r"C:\Users\14242\OneDrive\Desktop\p-interact workspace\giftofthemagi.txt", "r")
#zac file open
#file = open(r"C:\Users\zac\OneDrive\Documents\GitHub\p-interact", "r")
# reading the file
#data = file.read()


# -_________________________________________

# print(doc.text)
def pnouns(data):
    appeared = []
    #splitting data along newlines and . 
    sentences = data.replace('\n', ' ').split('.')

    for sentence in sentences:
        doc = nlp(sentence)

        for token in doc:
            if token.pos_ == "PROPN" and token.text not in appeared:
                appeared.append(token.text)
                print(token.text, token.pos_, token.dep_)
    # IMPORTANT: THIS CODE BREAKS BC IT DOESN'T RETURN A TABLE! NOT SURE WHAT THIS IS SUPPOSED TO DO BUT NEED TO BE FIXED
    return data


def show_ents(doc): 
    if doc.ents: 
        for ent in doc.ents: 
            print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_))) 
    else: print('No named entities found.')


def recperson(data):
    #to keep track of entities (people) who have appeared
    appeared = []
    #to keep track of entities (people)
    people = []
    #only splitting data along newlines (one big chunk)
    doc = nlp(data.replace('\n', ' '))

    for ent in doc.ents:
        if ent.label_ == 'PERSON' and (ent.text not in appeared):
            
            appeared.append(ent.text)
            people.append(ent.text)
    
    return people
    print(recperson(data))
    
async def update_table_char_summary_states(table_result, firstStory, max_tokens=100, temperature=0.3, top_p=1, frequency_penalty=0.3, tldrSummary=""):
    #, current_table=table_result):
    if firstStory:
        print('no table update in first story')
    else:
        #intergration with david's code needs work
        old_table = table_result
        print('old table=', old_table)
        # HERE IS WHERE CODE BREAKS
        modified_table = pnouns(old_table)
        print(modified_table)
        modified_table2 = show_ents(old_table)
        print(modified_table2)
        modified_table3 = recperson(old_table)
        print(modified_table3)
        new_table = modified_table 
        return(new_table)
        #update existing table
        #feed david's code in to update if alive status has changed
        #zac finish implementing this



#text summary states instead of table format, test in future
'''
async def gen_text_summary_states(newStory, firstStory = True, tldrSummary=""):
    #same as above but generate text summaries instead of pandas
    #zac finish implementing this
'''
#tldr function, presently commented out and replaced with tables - should be able to make both work together in future.
'''
async def update_tldr(newStory, firstStory=True, tldrSummary=""):

    if firstStory:
        tldrUpdated = openai.Completion.create(
            engine="text-davinci-001",
            prompt=newStory + "\n\n" + "tl;dr:",
            temperature=0.3,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        firstStory = False
        current_tldr = tldrUpdated

    else:

        tldrUpdated = openai.Completion.create(
            engine="text-davinci-001",
            prompt=tldrSummary + "\n\n" + newStory + "\n\n" + "tl;dr:",
            temperature=0.3,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        current_tldr = tldrUpdated

    return tldrUpdated


# separate out the story generation into separate function,     done
# have it take tldr as input,                                   done
# update tldr with function,                                    done   
# and output new tldr iteratively                               done

def generateStory():
    
    # update tldr with update_tldr
    update_tldr(init_story, firstStory=False, tldrSummary=current_tldr)
    
    return current_tldr
'''

async def options_generator(prompt):
    results = []
    # Generate 4 story options
    for i in range(4):
        #param test moving temp from 0.5 --> .3, and 0.5-->0.3 freqencuy pentalty
        #appears to not generate them
        res_gened = generate(prompt, max_tokens=50, temperature=0.3,
                       frequency_penalty=0.3, stop=["\n\n\n\n\n"])
        print(res_gened)
        results.append(res_gened)
        print(results)
    choices = await chronological.gather(*results)
    return choices


async def choose_story(input_story, table_result):
    # display newStory
    print("\n\n" + input_story + "\n\n")

    choices = await options_generator(input_story)
    # print(choices)

    # Present Choices for Next Chapter
    x = 1
    for choice in choices:
        print(str(x) + ". " + choice + "\n")
        x += 1

    # User chooses option
    # selected_choice = whatever they end up picking
    try:
        user_input = int(input("Enter your choice number: "))
        # - 1 because choosing 1 is really choosing 0
        num = user_input - 1
        if num < 0 or num > x:
            raise ValueError
        else:
            selected_choice = choices[num]
            # write choice
            async with aiof.open(output, mode='a') as f:
                await f.write("input: " + selected_choice)
                await f.write('\n\n\n')
                await f.close()
    except ValueError:
        print("Please only input numbers for your choice, between 1 and 4")
    # Generate Chapter
    #moving temperature from 0.7-->0.3, frequency penalty from 0.5--->0.3
    print('table fed 2+')
    result = await generate(table_explain+table_result + input_story + selected_choice, max_tokens=200, temperature=0.3, frequency_penalty=0.3)

    # Return Chapter
    return result


# you can name this function anything you want, the name "logic" is arbitrary
async def game():
    # Initial Story Choice
        firstStory=True
        table = await gen_table_char_summary_states()
        story = await init_story(table)
        async with aiof.open(output, mode='a') as f:
            await f.write(story)
            await f.write('\n\n\n')
            await f.close()
        # if testData command line arg is not provided
        if args.testData is None:
            while True:
                story = await choose_story(story, table)
                # write story to file
                async with aiof.open(output, mode='a') as f:
                    await f.write(story)
                    await f.write('\n\n\n')
                    await f.close()
                table = await update_table_char_summary_states(table, False)
        # if testData command line arg is provided
        else:
            for i in range(3):
                story = await choose_story(story, table)
                # write story to file
                async with aiof.open(test_output, mode='a') as f:
                    await f.write(story)
                    await f.write('\n\n\n')
                    await f.close()
                table = await update_table_char_summary_states(table, False)

# invoke the Chronology main fn to run the async logic
chronological.main(game)
