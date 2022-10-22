import openai
import os
import aiofiles as aiof
import chronological
from pathlib import Path

# Load your API key from an environment variable or secret management service
openai.api_key = ""
#openai.api_key = keys['OPENAI_API_KEY']
response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)

param_grid = {
    "temperature": [1, .8, .6, .4, .2, 0],
    "top_p": [1, .8, .6, .4, .2, 0],
    "freq_penalty": [2, 1.6, 1.2, .8, .4, 0],
    "pres_penalty":  [2, 1.6, 1.2, .8, .4, 0]  }

def generate_data(param_grid):
    for temp in param_grid["temperature"]:
        for top_p in param_grid["top_p"]:
            for freq_pen in param_grid["freq_penalty"]:
                for pres_pen in param_grid["pres_penalty"]:
                    # (file_name, error) = run_script(script)
                    generate_text(temp, top_p, freq_pen, pres_pen)

def generate_text(temp, top_p, freq_pen, pres_pen):
    script_dir = os.path.dirname(__file__)

    test_output="gridsearch_data/" + str(temp) + "_" + str(top_p) + "_" + str(freq_pen) + "_" + str(pres_pen) + ".txt"
    abs_file_path = os.path.join(script_dir, test_output)

    data_folder = Path("gridsearch_data/")
    asd = str(temp) + "_" + str(top_p) + "_" + str(freq_pen) + "_" + str(pres_pen) + ".txt"
    file_to_open = data_folder / asd

    preprompt = "Write an award-winning 3rd person short-story."
    actualprompt = "The life of a small-town girl only ever seemed to be one of boredom and simplicity. She would wake up each day, do the same things she always did, and go to bed with nothing new having happened. But on this particular day, something was different."
    prompt = preprompt + "\n" + actualprompt
    result = generate(1000, prompt, temp, top_p, freq_pen, pres_pen)
    print(result["choices"][0]["text"])
    print(result)

    f = open(file_to_open, 'w+')
    f.write(actualprompt + "\n" + result["choices"][0]["text"])
    f.close()


def generate(max_tokens=1000, prompt = "", temperature=0.3, top_p=1, frequency_penalty=0.3, presence_penalty = 0, stop=["\n\n"]):
    result =  openai.Completion.create(
  engine="text-davinci-002",
  prompt= prompt,
  max_tokens=750,
  temperature = temperature,
  top_p = top_p,
  frequency_penalty = frequency_penalty,
  presence_penalty = presence_penalty
) 
    return result

generate_data(param_grid)
