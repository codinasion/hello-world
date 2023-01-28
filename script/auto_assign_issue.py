# Auto assign 'good first issue' issues to user
# When they comment '!assign' on the issue

import os
import sys

import requests
import time

OWNER = "codinasion"
REPO = "hello-world"

# Get arguments from command line
if len(sys.argv) > 1:
    REPO_TOKEN = sys.argv[1]
    if len(sys.argv) > 2:
        ISSUE_NUMBER = sys.argv[2]
        if len(sys.argv) > 3:
            USERNAME = sys.argv[3]
        else:
            print(
                "USERNAME is required !!! \n\nUsage: python auto_assign_issue.py <REPO_TOKEN> <ISSUE_NUMBER> <USERNAME>"
            )
    else:
        print(
            "ISSUE_NUMBER is required !!! \n\nUsage: python auto_assign_issue.py <REPO_TOKEN> <ISSUE_NUMBER> <USERNAME>"
        )
else:
    print(
        "REPO_TOKEN is required !!! \n\nUsage: python auto_assign_issue.py <REPO_TOKEN> <ISSUE_NUMBER> <USERNAME>"
    )
    sys.exit(1)

# Get issue data
URL = "https://api.github.com/repos/{}/{}/issues/{}".format(
    OWNER, REPO, ISSUE_NUMBER)
issue_data_request = requests.get(
    URL,
    headers={
        "Authorization": "Token " + REPO_TOKEN,
        "Content-Type": "application/json",
    },
)

if issue_data_request.status_code == 200:
    print("Issue data fetched successfully")
else:
    print("==>> Issue data fetch failed :( !!!")
    print(issue_data_request.json())
    sys.exit(1)

# Get issue labels
labels = [label["name"] for label in issue_data_request.json()["labels"]]
print(labels)

# Check if issue contains "good first issue" label
if "good first issue" in labels:
    print("Issue contains 'good first issue' label")

    # Check if issue is assigned to anyone
    if issue_data_request.json()["assignee"] is None:
        print("Issue is not assigned to anyone")

        # Assign issue to user
        URL = "https://api.github.com/repos/{}/{}/issues/{}/assignees".format(
            OWNER, REPO, ISSUE_NUMBER
        )
        assign_issue_request = requests.post(
            URL,
            headers={
                "Authorization": "Token " + REPO_TOKEN,
                "Content-Type": "application/json",
            },
            json={"assignees": [USERNAME]},
        )

        if assign_issue_request.status_code == 201:
            print("Issue assigned successfully")
        else:
            print("==>> Issue assignment failed :( !!!")
            print(assign_issue_request.json())
    else:
        # Check if issue is assigned to user
        if issue_data_request.json()["assignee"]["login"] == USERNAME:
            print("Issue is assigned to user")
        else:
            print("Issue is assigned to someone else")

            # Create comment
            URL = "https://api.github.com/repos/{}/{}/issues/{}/comments".format(
                OWNER, REPO, ISSUE_NUMBER
            )
            create_comment_request = requests.post(
                URL,
                headers={
                    "Authorization": "Token " + REPO_TOKEN,
                    "Content-Type": "application/json",
                },
                json={
                    "body": """Hey @{}, this issue is already assigned to someone else.

Please choose another issue.

Thanks for your interest in contributing to this project.""".format(
                        USERNAME
                    )
                },
            )
