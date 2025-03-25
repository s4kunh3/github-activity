import sys
import requests
from datetime import datetime

def handle_event(event):
    event_time = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    formatted_time = event_time.strftime("%Y-%m-%d")

    if event['type'] == 'PushEvent':
        print(f'Pushed a commit on {event["repo"]["name"]} on {formatted_time}')
    elif event['type'] == 'ForkEvent':
        print(f'Made a fork at {event["repo"]["name"]} on {formatted_time}')
    elif event['type'] == 'WatchEvent':
        print(f'Starred {event["repo"]["name"]} on {formatted_time}')
    elif event['type'] == 'CreateEvent':
        print(f'Repo {event["repo"]["name"]} was created on {formatted_time}')
    elif event['type'] == 'IssuesEvent':
        print(f'Issue {event["payload"]["issue"]["number"]} created on {formatted_time}')
    elif event['type'] == 'IssueCommentEvent':
        print(f'Made a comment on issue {event["payload"]["issue"]["number"]} on {formatted_time}')
    elif event['type'] == 'PullRequestEvent':
        print(f'Created pull request {event["payload"]["pull_request"]["number"]} on {formatted_time}')
    elif event['type'] == 'PullRequestReviewEvent':
        print(f'Reviewed pull request {event["payload"]["pull_request"]["number"]} on {formatted_time}')
    elif event['type'] == 'PullRequestReviewCommentEvent':
        print(f'Made a comment on pull request {event["payload"]["pull_request"]["number"]} on {formatted_time}')

def get_events(username):
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)
    if response.status_code == 200:
        events = response.json()
        if not events:
            print("No activity on this user")
            return
        for event in events[:10]:
            handle_event(event)
            print()
    elif response.status_code == 404:
        print("Error: User not found")
    elif response.status_code == 403:
        print("Error: Rate limit exceeded. Try again later")
    else:
        print(f'Error: unexpected error (code: {response.status_code})')

def main(username):
    print()
    print('+---------------------+')
    print('|   Github activity   |')
    print('+---------------------+')
    print()
    print('Output: ')
    print()
    get_events(username)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide an username as an argument")
