<img
  width="400"
  src="sam_logo.svg"
  alt="logo"
/>
# Sam 
Sam is a simple command line tool which lets you ask an llm questions. The cli tool aims to be as minimal as possible; it only requires python to work, and there are no external libraries. Currently the tool is still a work in progress, so there are few features and there may be bugs.
The tool should support any openai api endpoint (I use groq with gpt-oss-120b). 

## Installation
**Linux/MacOS**
```bash
# Install for all users
sudo mkdir /opt/sam
sudo curl -L -o /opt/sam/sam "https://raw.githubusercontent.com/808sam808/sam/refs/heads/main/sam.py"
sudo chmod +x /opt/sam/sam
sudo ln -s /opt/sam/sam /usr/local/bin/sam
```

## Usage
```bash
# Configuration
sam --config

# Asking a question
sam 'your question here'
```

## To-do
- ~~[ ] Bash script for installation~~
- [x] migrate from requests library
- [x] Store API key as env variable and have script access it
- [x] Have script using environment variables from config.json
  - [x] Have script check for existence of config.json
- [x] Configuration via command line
  - [x] Create the `--config` flag
  - [x] write changes to config.json
- [ ] help command
- [ ] Update status command
- [ ] Support other api keys
  - [x] Groq
  - [x] OpenRouter
  - [ ] OpenAI
  - [ ] Claude
  - [ ] Other
- [ ] Exception handling
- [ ] Write install instructions for linux + macos
- [ ] Add a loading bar/spinner
- [x] **Replacing placeholders in commands**
- [ ] **Way to continue conversation**
- [ ] Aesthetics
- [ ] Fix weird behavior when ask "command to move to different directory"
