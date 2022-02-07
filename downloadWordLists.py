import json
import urllib.request
import urllib.parse
import argparse

# folder to save generated results in
folder_name = "generated"
# For extra print statements
verbose = False


def getJapJs(group, page):
    """Get the results of Jisho.org for the word or search 'e', in JSON form

    Args:
            e (string): Jisho search term

    Returns:
            [type]: [description]
    """

    # add some safe inputs
    url = urllib.parse.quote(
        "https://jisho.org/api/v1/search/words?keyword=#jlpt-" + group.lower() + "&page=" + str(page), safe=":/?=&")

    if verbose:
        print(url)

    response = urllib.request.urlopen(url)

    # returns multiple
    result = json.loads(response.read())

    numResults = len(result['data'])
    if verbose:
        print("Found " + str(numResults))

    return result


def getAllOfGroup(group, fileName=""):
    """SLOW OPERATION. Download all the words for a `group` from Jisho and save into a json file.

    Args:
            group (string): Jisho Category to search for (e.g. N3) or tag (e.g. #common (note # for tag searches))
            fileName (string, optional): filename output to save json data. Defaults to "$(group).json"
    """

    if fileName == "":
        fileName = group + ".json"

    # number of results returned from JSON query for a page
    numResults = 1
    # keep track of pages of results
    pageCounter = 1

    list = {"debug": False, "words": []}

    # Jisho has a limit of 20 results per page/return, so run for multiple pages until no more results
    while (True):
        JSONResults = getJapJs(group, pageCounter)
        numResults = len(JSONResults['data'])

        # jisho.org currently has a limit of 1000 pages
        if(numResults == 0 or pageCounter > 999):
            break

        for resultIndex in range(0, numResults):
            result = JSONResults['data'][resultIndex]
            kana = result['japanese'][0]['reading']
            meaning = {"language": "en",
                       "definitions": result['senses'][0]['english_definitions']}
            entry = None
            if ('word' in result['japanese'][0]):
                entry = [{"word": kana, "additionalInfo": {
                    "alternateSpelling": result['japanese'][0]['word'],
                    "meaning": meaning}}]
            else:
                entry = [{"word": kana, "additionalInfo": {
                    "meaning": meaning}}]

            list['words'] = list['words'] + entry

        # increment page counter
        pageCounter = pageCounter + 1

    if verbose:
        print("Found " + str(pageCounter - 1) + " pages ")

    # Write to a file
    with open(fileName, 'w', encoding='utf-8') as jf:
        json.dump(list, jf, indent=3, ensure_ascii=False)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Download JLPT N5-N1 and common vocabulary from Jisho and output anki-ready csv decks")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print more verbose statements')
    parser.add_argument(
        '-t', '--type', choices=["normal", "extended"], default='normal', help='type of card to generate')
    args = parser.parse_args(argv)
    global verbose
    verbose = args.verbose
    return args


if __name__ == "__main__":
    args = parse_args()

    # Which JLPT grades to get (any combination of N5, N4, N3, N2, N1 and #common)
    JLPT_Grades = ["N5", "N4", "N3", "N2", "N1"]

    for N in JLPT_Grades:
        getAllOfGroup(N)
