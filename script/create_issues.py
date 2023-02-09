# Create all 'hello world' issues
# Should only be used once !!!

import sys

import requests
import time

# load json file
import json

from random import shuffle

OWNER = "codinasion"
REPO = "hello-world"

# Get arguments from command line
if len(sys.argv) > 1:
    REPO_TOKEN = sys.argv[1]
else:
    print("REPO_TOKEN is required !!! \n\nUsage: python create_issues.py <REPO_TOKEN>")
    sys.exit(1)

languages_json_file = open("data/languages.json", "r")

languages = json.load(languages_json_file)

# randomize the languages, just for fun :)
shuffle(languages)


def CreateIssue(ISSUE_DATA):
    # create issue
    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    issue_create_request = requests.post(
        URL,
        headers={
            "Authorization": "Token " + REPO_TOKEN,
            "Content-Type": "application/json",
        },
        json=ISSUE_DATA,
    )

    if issue_create_request.status_code == 201:
        print("Issue created successfully")
    else:
        print("==>> Issue creation failed :( !!!")
        print(issue_create_request.json())

    # Wait few seconds ( to prevent Github API secondary rate limit !!! )
    # In this case, the action will run for a very long time.
    # So, it's better to keep the wait time high.
    time.sleep(25)


counter = 0
for language in languages:
    if language["type"] == "programming":

        print(language["name"])

        if "extensions" in language:

            for extension in language["extensions"]:

                issue_data = {
                    "title": f"Write a {language['name']} program to print \"Hello World\"",
                    "body": f"""### Description

Write a {language['name']} program to print \"Hello World\"

> **Note** Save `hello-world{extension}` inside the `hello-world` folder""",
                    "labels": [
                        language["name"],
                        "good first issue",
                        f"hello world",
                    ],
                }

                CreateIssue(issue_data)
                counter += 1

print("Total issues created: ", counter)
