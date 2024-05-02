import requests
import argparse
import os
from dotenv import load_dotenv

load_dotenv()



def change_repo_organization(repo, owner, new_organization, new_name):
    url = f"https://api.github.com/repos/{owner}/{repo}/transfer"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    payload = {
        "new_owner": new_organization,
        new_name: new_name
    }
  
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 202:
        print(f"Transfer initiated for repository {repo} from {owner} to {new_organization}")
    else:
        print(f"Failed to initiate transfer for repository {repo}", response.json())


def check_repo_exists(name, owner):
    url = f"https://api.github.com/repos/{owner}/{name}"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"Failed to check existence of {name}", response.json())
        return False

def change_repo_name(name, owner, new_name):
    url = f"https://api.github.com/repos/{owner}/{name}"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": new_name
    }
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Successfully changed name of {name} to {new_name}")
    else:
        print(f"Failed to change name of {name}", response.json())

def change_repo_owner(repo, old_owner, new_owner):
    url = f"https://api.github.com/repos/{old_owner}/{repo}"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "new_owner": new_owner
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Successfully changed owner of {repo} from {old_owner} to {new_owner}")
    else:
        print(f"Failed to change owner of {repo}", response.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change repository owner on GitHub")
    parser.add_argument("--old_owner", help="Current owner of the repositories")
    parser.add_argument("--new_owner", help="New owner of the repositories")
    parser.add_argument("--change_name", type=bool, default=False, help="Whether to change the repository name or not")

    args = parser.parse_args()
    old_owner = args.old_owner
    new_owner = args.new_owner
    change_name = args.change_name
    
    if old_owner is None or new_owner is None:
        print("Please provide both old_owner and new_owner")
        exit(1)

    with open('repositories.txt', 'r') as file:
        repos = file.read().splitlines()

    for repo in repos:
        
        if change_name:
            name = f"{old_owner}-{repo}"
        else:
            name = repo
              
        print(f"Checking {name}...")
        if not check_repo_exists(name, new_owner) and check_repo_exists(repo, old_owner):
            
            print(f"Repository {repo} exists under {old_owner}. Changing owner to {new_owner} ...")
            #change_repo_owner(repo, old_owner, new_owner)
            change_repo_organization(repo, old_owner, new_owner, name)
            print("Owner changed \n")

        else:
            print(f"Repository {repo} does exist under {old_owner} Skipping...")
        print("Finished \n")
