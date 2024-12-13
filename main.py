import os
import time
import config
import readline
from typing     import Any, Literal
from dotenv     import load_dotenv
from termcolors import *

if __name__ == "__main__":
    print(f"{italic}{blue}{dim}Setting up {reset}{italic}{blue}google.generativeai{dim}...{reset}", end="", flush=True)

import google.generativeai       as genai
from   google.generativeai.types import (
    HarmCategory, HarmBlockThreshold
)

load_dotenv()
genai.configure()

model = genai.GenerativeModel(
    config.MODEL,
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
    },
    system_instruction = config.SYSTEM_INSTRUCTIONS
)

token_counter = genai.GenerativeModel(
    config.MODEL,
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT:        HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH:       HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
    }
)

def clearln():
    print("\r" + (" "*os.get_terminal_size().columns), end="\r", flush=True)

def back(characters: int):
    print(f"\033[{characters}D", end="", flush=True)

def slow_print(
    txt: Any,
    *,
    delay: int | float | None = None,
    mode: Literal["character", "word"] = "character",
    end: Any = "\n"
):
    if delay is None:
        print(txt, end=end, flush=True)
        return
    
    text: str = str(txt)
    if mode == "character":
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
    elif mode == "word":
        words = text.split(" ")
        for i, word in enumerate(words):
            print(word, end="" if i == len(words) - 1 else " ", flush=True)
            time.sleep(delay)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    print(end=end, flush=True)

def main():
    chat = model.start_chat()
    
    clearln()
    print(f"{italic}{blue}{dim}Model:{reset} {italic}{blue}{config.MODEL}{reset}")
    if config.SYSTEM_INSTRUCTIONS and config.PRINT_SYSTEM_INSTRUCTIONS:
        print(f"{italic}{blue}{dim}System Instructions:{reset} {italic}{yellow}{config.SYSTEM_INSTRUCTIONS}{reset}")
    
    try:
        while True:
            prompt = ""
            multiline = False
            while True:
                if not multiline:
                    inp = input(f"{green}You:{reset} ")
                else:
                    try:
                        inp = input(f"{green}....{reset} ")
                    except KeyboardInterrupt:
                        clearln()
                        continue
                
                if not multiline and inp.strip().startswith("\\("):
                    prompt += inp[2:]+"\n"
                    multiline = True
                    continue
                elif not multiline and inp.strip().startswith("\\\\("):
                    prompt += inp[1:]
                    break
                elif multiline and inp.strip().endswith("\\\\)"):
                    prompt += inp[:-3]+"\\)\n"
                    continue
                elif multiline and inp.strip().endswith("\\)"):
                    prompt += inp[:-2]+"\n"
                    break
                elif multiline:
                    prompt += inp+"\n"
                    continue
                else:
                    prompt += inp
                    break
            
            if prompt == "e" \
               or prompt == "q" \
               or prompt == "exit" \
               or prompt == "quit":
                break
            
            if not prompt:
                prompt = " "
            elif prompt and prompt.strip() == "":
                pass
            else:
                prompt = prompt.strip()
            
            print(f"{magenta}Model:{reset} {italic}{yellow}{dim}Connecting to server...{reset}", end="", flush=True)
            
            start = None
            try:
                response = chat.send_message(prompt, stream=True)
                for chunk in response:
                    if start is None:
                        start = time.monotonic()
                        clearln()
                        print(f"{magenta}Model:{reset} {white}", end="", flush=True)
                    
                    slow_print(
                        chunk.text,
                        delay = config.PRINT_SPEED,
                        mode = config.PRINT_MODE,
                        end = ""
                    )
                else:
                    time_taken = time.monotonic() - start if start is not None else 0
                    token_count = token_counter.count_tokens(response.text).total_tokens
                    print(end=reset)
                    print(f"{italic}{yellow}Model took {green}{round(time_taken, 2)}s{yellow} to generate {green}{token_count:,}{yellow} tokens ({green}{round(token_count/time_taken, 2)}{yellow} tokens/s){reset}")
            
            except Exception as e:
                if hasattr(e, "__module__"): module_class = f"{e.__module__}.{e.__class__.__name__}"
                else:                        module_class = e.__class__.__name__
                clearln()
                print(f"{red}[ERROR]{reset} {bold}{red}{module_class}{reset}"+(f"{red}: {e}{reset}" if str(e) else ""), flush=True)
    
    except KeyboardInterrupt:
        print(f"{dim}^C{reset}", flush=True)
    
    print(f"{italic}{blue}Sayonara!{reset}")

if __name__ == "__main__":
    main()