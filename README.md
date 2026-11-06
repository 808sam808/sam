# (WIP) Command Line Helper
A super simple command line tool which lets you ask an llm questions. Each question uses only one llm api request. A single python script with no external libraries. Currently the tool is still a work in progress, so there are few features and there may be bugs.
The tool should support any openai api endpoint (I use groq with gpt-oss-120b). Currently you need to paste your api key and endpoint yourself.  

## Installation
```bash
# Note: On first launch the script will create the config.json file in the same directory
mkdir ./sam
cd sam
curl scriptlocation.com
symlink to executable directory
```

## Usage
```bash
# Asking a question
sam 'your question here'

# Configuration
sam --config
```

## To-do
~~[] Bash script for installation~~
[x] migrate from requests library
[x] Store API key as env variable and have script access it
[x] Have script using environment variables from config.json
  [x] Have script check for existence of config.json
[x] Configuration via command line
  [x] Create the `--config` flag
  [x] write changes to config.json
[] help command
[] Update status command
[] Support other api keys
  [x] Groq
  [x] OpenRouter
  [] OpenAI
  [] Claude
  [] Other
[] Exception handling
[] Write install instructions for linux + macos
[] Add a loading bar/spinner
[x] **Replacing placeholders in commands**
[] **Way to continue conversation**
[] Aesthetics

## Bugs
[x] Border does not render
```bash
sam@hpserver:~/cliproject$ python3 samlite_v6.py 'command to list all files in a directory'
Traceback (most recent call last):
  File "/home/sam/cliproject/samlite_v6.py", line 220, in <module>
    print(border(answer))
          ~~~~~~^^^^^^^^
  File "/home/sam/cliproject/samlite_v6.py", line 199, in border
    text_wo_command = text.split('\n', 1)[1]
                      ~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
```

[x] Text pierces through box
```bash
sam@hpserver:~/cliproject$ python3 samlite_v6.py 'command to start a docker container'
╭──────────────────────────────────────────────────╮
│ ► docker run -d --name *container_name *image_name │
│ This starts the specified image as a detached    │
│ container with the given name.                   │
╰──────────────────────────────────────────────────╯
```

[] weird behavior when ask "command to move to different directory"
