# Add .{extension} label to all issues

import sys

import requests
import time

OWNER = "codinasion"
REPO = "hello-world"

# Get arguments from command line
if len(sys.argv) > 1:
    REPO_TOKEN = sys.argv[1]
else:
    print("REPO_TOKEN is required !!! \n\nUsage: python add_issue_extension.py <REPO_TOKEN>")
    sys.exit(1)


def Main():
    # Get all issues
    GET_ISSUE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    GET_ISSUE_PAGE = 1

    while True:
        get_issue_request = requests.get(
            GET_ISSUE_URL+"?per_page=100&page="+str(GET_ISSUE_PAGE),
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

                    # Get .{extension} from issue body
                    issue_extension = issue_body.split(
                        "` inside the `hello-world` folder")[0].split("Save `hello-world")[1]
                    print(issue_extension)

                    issue_labels = [label["name"] for label in issue["labels"]]
                    print(issue_labels)

                    if issue_extension not in issue_labels:
                        # Add .{extension} label to issue
                        issue_labels.append(issue_extension)

                        print("Updated issue labels: ", issue_labels)

                        # Update issue labels
                        update_issue_request = requests.post(
                            issue["url"]+"/labels",
                            headers={
                                "Authorization": "Token " + REPO_TOKEN,
                                "Content-Type": "application/json",
                            },
                            json={
                                "labels": issue_labels
                            }
                        )

                        if update_issue_request.status_code == 200:
                            print("Issue updated successfully")
                        else:
                            print("==>> Issue update failed :( !!!")
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
