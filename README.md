# gemini-cli
Python CLI tool to use any Google Gemini model on the command line.

## features
- colorful and easy to use
- use any gemini model available in [Google AI Studio](https://aistudio.google.com)
- uses readline module (windows supported)
- set system instructions
- model's output is streamed
- shows how long the model took to respond, the amount of tokens generated and how fast it generated in tokens/second
- multiline prompt support

![](https://github.com/user-attachments/assets/e3de837a-ba1b-4b98-9b7f-419ca7831a43)

## note
this is just a small project, you are free to use this if you want but don't expect regular updates

you can also contribute by opening a pull request

## how to use some features
## config
edit `config.py`

### multiline prompt
start a prompt with `\(` and you can now type in multiple lines
<br>
use `\)` at the end of the prompt to stop the prompt from being multilined further

### readline module
you can use the up and down arrow keys to navigate the prompts you have typed in the chat

you can use the left and right arrow keys (along with ctrl) to easily edit the prompt if you made any mistakes or need to add something in the current line

you can use `Ctrl + C` when inside multiline to clear the current line's text

### exit
use `Ctrl + C` or type `e`, `exit`, `q` or `quit` (case-sensitive) to exit

if you want to send `e`, `exit`, `q` or `quit` as a message to the model, add a space at the start or end of your message and it will be sent to the model

### error handling
handles any errors encountered while chatting with gemini 

## requirements
- [Python 3.10+](https://python.org)
- [Google AI Studio](https://aistudio.google.com) API Key

### note
your google account needs to be 18+ or made in an available region to use [Google AI Studio](https://aistudio.google.com)

if your country is in the list of available regions and if the page still redirects you to an `ai.google.dev` website and you have an 18+ account, try with https://aistudio.google.com/?authuser=1
<br>
keep increasing the authuser counter for however many accounts you have, 0 means 1st account, 1 means 2nd account, 2 means 3rd account, and so on.

## setup
```sh
git clone https://github.com/sqdnoises/gemini-cli.git
cd gemini-cli
pip install -r requirements.txt
```

create a file called `.env` in the same folder and paste your Google AI Studio API key in it


`.env` structure:
```properties
GOOGLE_API_KEY="your Google AI Studio API key"
```

## run
```sh
python3 main.py
```
or windows users would need to use `py main.py` or `python main.py`

## license
this program comes with the [MIT License](LICENSE)
