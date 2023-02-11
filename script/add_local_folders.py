# Add saperate folders for each language (locally)

import os
import sys

import requests
import time

OWNER = "codinasion"
REPO = "hello-world"


def Main():
    # Get all issues
    GET_ISSUE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    GET_ISSUE_PAGE = 1

    while True:
        get_issue_request = requests.get(
            GET_ISSUE_URL
            + "?labels=good%20first%20issue&per_page=100&page="
            + str(GET_ISSUE_PAGE),
            headers={
                # "Authorization": "Token " + REPO_TOKEN,
                "Content-Type": "application/json",
            },
        )

        if get_issue_request.status_code == 200:
            print("Issues fetched successfully")

            if len(get_issue_request.json()) == 0:
                print("No more issues to process")
                break

            issues = get_issue_request.json()

            for issue in issues:
                # If issue is not a pull request
                if not f"https://github.com/{OWNER}/{REPO}/pull/" in issue["html_url"]:
                    issue_body = issue["body"]

                    # Get Programming language from issue body
                    language = issue_body.split(' program to print "Hello World"')[
                        0
                    ].split("Write a ")[1]
                    folder_name = language.replace(" ", "-").lower()
                    # print(folder_name)

                    # Create folder, if not exists
                    folder_path = "../hello-world/" + folder_name
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                        # Create a README.md file
                        with open(folder_path + "/README.md", "w") as f:
                            f.write(
                                f"""# {language}

This folder contains `{language}` programs to print `Hello World`

> **Note** You can find more issues related to {language} [here](https://github.com/codinasion/hello-world/issues?q=is%3Aissue+is%3Aopen+{folder_name})

<div align="center">
    <img src="https://raw.githubusercontent.com/codinasion/.github/master/assets/rainbow-hr.png" alt="rainbow hr" width="100%" height="70%">
</div>

<br>

<table>
    <tr>
        <td>
            <img align="left" src="https://raw.githubusercontent.com/codinasion/.github/master/assets/octocat.png" width="190">
            <h3>Thanks for contributing :purple_heart:</h3>
            <ul>
                <li>Thanks for all your contributions and efforts</li>
                <li>We thank you being part of our :sparkles: commUnity :sparkles: !</li>
            </ul>
            <img width="900" height="0">
        </td>
    </tr>
</table>

<div align="center">
    <img src="https://raw.githubusercontent.com/codinasion/.github/master/assets/rainbow-hr.png" alt="rainbow hr" width="100%" height="70%">
</div>
"""
                            )
                        print(
                            f"{folder_path.replace('../hello-world/', '')}/README.md created successfully"
                        )
                        time.sleep(1)
                    else:
                        print("Folder already exists")

            GET_ISSUE_PAGE += 1

            if len(get_issue_request.json()) < 100:
                print("No more issues to process (<100)")
                break

            time.sleep(5)

        else:
            print("==>> Issues fetch failed :( !!!")
            print(get_issue_request.json())
            sys.exit(1)


# Driver Function
Main()
