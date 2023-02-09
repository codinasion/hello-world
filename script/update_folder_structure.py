# Update folder structure to all issues

import sys

import requests
import time

OWNER = "codinasion"
REPO = "hello-world"

# Get arguments from command line
if len(sys.argv) > 1:
    REPO_TOKEN = sys.argv[1]
else:
    print(
        "REPO_TOKEN is required !!! \n\nUsage: python add_issue_extension.py <REPO_TOKEN>"
    )
    sys.exit(1)


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
                "Authorization": "Token " + REPO_TOKEN,
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
                    language = language.replace(" ", "-").lower()
                    print(language)

                    # Get .{extension} from issue body
                    extension = issue_body.split("` inside the `")[0].split(
                        "Save `hello-world."
                    )[1]
                    print(extension)

                    # Update issue body
                    issue_body = issue_body.split("\n\n> **Note** Save")[0]
                    issue_body = (
                        issue_body
                        + f"\n\n> **Note** Save the file as `hello-world.{extension}` inside the [`hello-world/{language}/`](https://github.com/codinasion/hello-world/tree/master/hello-world/{language}) folder"
                    )
                    print(issue_body)

                    # Update issue body
                    update_issue_request = requests.patch(
                        issue["url"],
                        headers={
                            "Authorization": "Token " + REPO_TOKEN,
                            "Content-Type": "application/json",
                        },
                        json={
                            "body": issue_body,
                        },
                    )

                    if update_issue_request.status_code == 200:
                        print("Issue body updated successfully")
                    else:
                        print("==>> Issue body update failed :( !!!")
                        print(update_issue_request.json())
                        sys.exit(1)

                    time.sleep(1)

            GET_ISSUE_PAGE += 1

            if len(get_issue_request.json()) < 100:
                print("No more issues to process (<100)")
                break

            time.sleep(1)

        else:
            print("==>> Issues fetch failed :( !!!")
            print(get_issue_request.json())
            sys.exit(1)


# Driver Function
Main()
