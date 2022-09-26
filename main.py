from urllib.error import HTTPError
import rich
import json
import requests
import sys, os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.traceback import install
from rich.markdown import Markdown
import lang_supported
import tts_voice  # file module 

load_dotenv()  # loads API TOKEN
install()  # traceback for error prompts
console = Console()  # rich console for styling

# get the .env variables
API_TOKEN = os.getenv('API_TOKEN')


# api calling
def api_call(text_converting, to_language):
    url_detect = "https://google-translate78.p.rapidapi.com/language_detect"
    url_translate = "https://google-translate78.p.rapidapi.com/translate"

    payload_detect = {"text": text_converting}

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": API_TOKEN,
        "X-RapidAPI-Host": "google-translate78.p.rapidapi.com"
    }

    response_detect = requests.request(
        "POST", url_detect, json=payload_detect, headers=headers)
    source_language = response_detect.json()["language_detection"]["language"]

    payload_translate = {
        "text": text_converting,
        "source": source_language,
        "target": to_language
    }

    response_translate = requests.request(
        "POST", url_translate, json=payload_translate, headers=headers)
    return response_translate.json()["translations"]["translation"]


# count letters in a string to check if the language is valid
def count_letters(word):
    return len([x for x in word if x.isalpha()])


# ----------------------------- MARKDOWN -------------------------------- #


MARKDOWN = """
# Translator v1.0

This is a simple translator that uses the Google Translate API to translate text from one language to another.

## Usage
1. Enter the text you want to translate.
2. Enter the language you want to translate to.
3. The translated text will be displayed.
##
"""
md = Markdown(MARKDOWN)
console.print(md)

# ----------------------------- main ----------------------------- #

if __name__ == '__main__':

    choice = console.input(
        '[bold yellow]Would you like to see the languages?[/bold yellow] [bold purple](y/n)\n[/bold purple]')
    if choice == 'y' or choice == 'Y':
        lang_supported.langs()

    # variables input
    text_converting = console.input(
        "\n[bold yellow]Enter the text you want to convert: ")
    to_language = console.input(
        "\n[bold yellow]Enter the language you want to convert to: ")

    # check if the language is valid (language cannot have more than 2 chars)
    while ((count_letters(to_language) > 2) or (to_language.isnumeric())):
        console.print(
            "\n[red blink]Invalid language[/red blink], [cyan]use the format [purple]'en'[/purple] for English[/cyan]")
        to_language = console.input(
            "\n[bold yellow]Enter the language you want to convert to: ")

    # output
    try:
        translated_text = api_call(text_converting, to_language)
    except HTTPError as e:
        console.print(f'[red]The following error occured:[/red] [bold red]{e}')
    except Exception as e:
        console.print(f'[bold red]{e}')
    else:
        console.print(
            f'\n[green]The translated text is: [/green][purple]{translated_text}[/purple]')

    # Hear the translation
    hear_choice = console.input(
        "\n[bold yellow]Do you want to hear the translation?[/bold yellow] [purple](y/n)\n[/purple]")
    if hear_choice == 'y' or hear_choice == 'Y':
        try:
            tts_voice.speak(translated_text, to_language)
        except Exception as e:
            console.print(f'[bold red]{e}')
        else:
            sys.exit()
# ----------------------------------------------------------------- #
