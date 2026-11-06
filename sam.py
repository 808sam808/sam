#!/usr/bin/env python3
import os
import argparse
import json
import subprocess
import shutil
import textwrap
import urllib.request
import sys
from pathlib import Path

# check if config.json exists
try:
    with open("config.json", "x") as file:
        file.write("{}")
        print('config.json does not exist. Creating file now.')
        # sys.exit()
except FileExistsError:
    pass


# open config.json
with open("config.json", "r") as file:
    loaded_config = json.load(file)


def model_scanner(provider_model_list, temp_api_key):
    req = urllib.request.Request(
            provider_model_list,
            # data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {temp_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            # method="POST",
        )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
    r_d = result["data"]
    return [model["id"] for model in r_d if "id" in model]


# arparse for cli processes
parser = argparse.ArgumentParser()


parser.add_argument("user_question", nargs="?")
parser.add_argument("--config", action="store_true")
parser.add_argument("--status", action="store_true")

args = parser.parse_args()




if args.config:
    print('Hello!')
    print('''Select an API provider

(1) Groq
(2) OpenRouter
(3) OpenAI
(4) Other
        ''')
    api_provider = int(input('Select number 1-4: '))
    if api_provider == 1:
        provider = 'Groq'
        model_list = 'https://api.groq.com/openai/v1/models'
        api_endpoint="https://api.groq.com/openai/v1/chat/completions"
        api_key_name = "GROQ_API_KEY"
    if api_provider == 2:
        provider = 'OpenRouter'
        model_list = 'https://openrouter.ai/api/v1/models'
        api_endpoint="https://openrouter.ai/api/v1/chat/completions"
        api_key_name = "OPENROUTER_API_KEY"
    if api_provider == 3:
        provider = 'OpenAI'
        model_list = 'https://api.openai.com/v1/models'
        api_endpoint="https://api.openai.com/v1/chat/completions"
        api_key_name = "OPENAI_API_KEY"
    if api_provider == 4:
        print('Okay, as long as your api is openai compatible it should work. You will input the provider name, api endpoint, and model manually.')
        provider = input('Provider: ')
        api_endpoint = input('API endpoint: ')
        model = input('Model: ')

    print()
    print('Do you want to store API key in config.json or as an environmental variable?')
    config_or_env = input('in (C)onfig.json or use (E)nvironmental variable: ')
    if config_or_env == 'C':
        api_key = input('Enter API key here: ')
        temp_api_key = api_key
    elif config_or_env == 'E':
        if not os.environ.get(f"{api_key_name}"):
            print(f'It seems that you have not saved your {provider} API key as an environmental variable. If you do not want to do that you can add the API key directly into the script. NOTE: This is considered a poor security practice!')
            sys.exit()
        else:
            temp_api_key = os.environ.get(f"{api_key_name}")
            slice_api_key = temp_api_key[:6]
            print(f'Nice, your api key {slice_api_key}... was found.')
            api_key = 'null'
    else:
        print('that shit is not the letter C or E')
        sys.exit()

    print(f'{provider} selected. Would you like to see available llms from {provider}? ')
    y_or_n = input('(y/n): ')
    if y_or_n == 'y':
        chud = model_scanner(model_list, temp_api_key)
        # response = requests.get(f'{model_list}', headers=headers)
        # r_d = (json.loads(response.text))["data"]
        # chud = [model["id"] for model in r_d if "id" in model]
        x = 0
        for model in chud:
            x = x+1
            print(f'({x}) ', model)
        number_selected = input('Okay, what model do you want to use? (choose number): ')
        model = chud[int(number_selected) - 1]
        print(f'{model} selected!')
    elif y_or_n == 'n':
        model = input('Okay, what model do you want to use?: ')
    else:
        print('Error! enter y or n')

    config = {
        "API key": f"{api_key}",
        "API provider": f"{provider}",
        "API endpoint": f"{api_endpoint}",
        "LLM Model": f"{model}",
        "API key name": f"{api_key_name}"
    }
    with open("config.json","w")as file:
        json.dump(config, file, indent=2)
    print('''
Configuration saved :)''')
    sys.exit()

try:
    api_endpoint = (loaded_config["API endpoint"])
    api_key = (loaded_config["API key"])
    model = (loaded_config["LLM Model"])
    provider = (loaded_config["API provider"])
    api_key_name =(loaded_config["API key name"])
except KeyError:
    print('It seems that your configuration is incomplete. Please run the command: sam --config')
    sys.exit()

groq_api_endpoint="https://api.groq.com/openai/v1/chat/completions"
openrouter_api_endpoint="https://openrouter.ai/api/v1/chat/completions"
openai_api_endpoint="https://api.openai.com/v1/chat/completions"

if api_key == 'null':
    api_key = os.environ.get(f"{api_key_name}")


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def askai(q):
    payload = {
        "model": f"{model}",
        "messages": [
            {"role": "system", "content": "You are a unix terminal assistant. The user will ask questions, and you will reply with a simple short answer. If the answer to a user's question is best solved by a command, place the required command as the very first line of the response and start that line with '► '. If there is a placeholder for some part of the command, start the word of the placeholder with '*'. If multiple commands need to be run, chain them together using &&. Do not use markdown styling, use plain text."},
            {"role": "user", "content": f"{q}"}
        ],
    }

    req = urllib.request.Request(
        api_endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))

    return (result["choices"][0]["message"]["content"])


def border(text):
    size = shutil.get_terminal_size()
    max_length = size.columns

    top_of_border = '╭' + '─' * (max_length-2) + '╮'
    bottom_of_border = '╰' + '─' * (max_length-2) + '╯'

    lines = textwrap.wrap(text, width=(max_length-4))

    if text[0] == '►':
        if max_length < len(command):
            text_wo_command = text.splitlines()
            try:
                actually_wo = text_wo_command[1]
            except IndexError:
                actually_wo = ' '
            actual_command = command.split("/n")
            # print(actual_command)
            broski = actual_command[0]
            bruh = textwrap.wrap(broski, width=(max_length-4))
            otherlines = textwrap.wrap(actually_wo, width=(max_length-4))
            print(top_of_border)
            for line in bruh:
                print(f"│ {line.ljust(max_length-4)} │")
            print(f"│ {' '.ljust(max_length-4)} │")
            for line in otherlines:
                print(f"│ {line.ljust(max_length-4)} │")
        else:
            text_wo_command = text.splitlines()
            try:
                actually_wo = text_wo_command[1]
            except IndexError:
                actually_wo =  ' '
            otherlines = textwrap.wrap(actually_wo, width=(max_length-4))
            print(top_of_border)
            print(f"│ {command.ljust(max_length-4)} │")
            for line in otherlines:
                print(f"│ {line.ljust(max_length-4)} │")

    else:
        print(top_of_border)
        for line in lines:
            print(f"│ {line.ljust(max_length-4)} │")

    return bottom_of_border


if args.user_question:
    prompt = (args.user_question)
    answer = askai(prompt)
    command = answer.partition('\n')[0]
    choppedcommand = command.split()
    goodcommand = choppedcommand[1:]
    print(border(answer))

    if command[0] == '►':
        if '*' in command:
            print("\033[1;36mFill in placeholders and run the command?\033[0m")
            yes_or_no = input("(y/n): ")
            if yes_or_no == "y":
                # answer_list = command.split()
                # print(choppedcommand)
                filled_in_command = []
                for word in choppedcommand:
                    if '*' in word:
                        # print(f"{word} yes")
                        # choppedcommand.remove(word)
                        filled_in_command.append(input(f"{word}: "))
                    else:
                        # print(f"{word} no")
                        filled_in_command.append(word)
                goodcommand = filled_in_command[1:]
                # print(goodcommand)
                subprocess.run(goodcommand)

        else:
            print("\033[1;36mRun the command?\033[0m")
            yes_or_no = input("(y/n): ")
            if yes_or_no == "y":
                # print(goodcommand)
                subprocess.run(goodcommand)

elif args.status:
    print(f"Model: {model}")
    print(f"API endpoint: {api_endpoint}")
    print(f"API provider: {provider}")
