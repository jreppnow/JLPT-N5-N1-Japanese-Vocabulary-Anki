# (Custom fork of) JLPT-N5-N1-Japanese-Vocabulary-Anki

This is a custom fork of the original library we use specifically to generate word lists for our discord wordle bot (https://github.com/Piturnah/jp-wordle-bot). Please refer to the original repository for information. Copyright remains with the original author.

## How to Generate Files

Ensure Python Version 3.X is installed. I would suggest also having pipenv installed (`pip install pipenv`). Then run `pipenv shell` in this folder, then `python createJLPTDeck.py`. Resulting files will be created in the "generated" folder.

### Suggested run arguments

`python createJLPTDeck.py -v` will download and create all JLPT decks and common word deck. The `-v` argument is useful to track process of the script, as it takes a while to complete.

`python createJLPTDeck.py -v --type extended` will create all JLPT decks and common word deck with some words containing audio. This method is a lot slower due to needing to download many more files.

