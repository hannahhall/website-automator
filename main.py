"""Quick practice with the Github API to create and deploy a class website from a template"""
import json
import os
from time import sleep
import requests


def create_repo_from_template(cohort_org, repo_name):
    """Creates a github repo within the cohorts organization

    Args:
        cohort_org (string): the cohort's github org
        repo_name (string): the name of the new repo

    Returns:
        boolean: was the request succesfull
    """
    template = "nashville-software-school/Class-Website"
    url = f"https://api.github.com/repos/{template}/generate"

    payload = json.dumps({
        "owner": cohort_org,
        "name": repo_name,
        "description": "The class website",
        "include_all_branches": False,
        "private": False
    })
    headers = {
        'Authorization': f'Basic {os.environ.get("BASIC_AUTH_TOKEN")}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.ok


def deploy_site(cohort_org, repo_name):
    """Deploy the class website with github pages

    Args:
        cohort_org (string): the cohort's github organization
        repo_name (string): the repo name

    Returns:
        boolean: was the request successfull
    """
    url = f"https://api.github.com/repos/{cohort_org}/{repo_name}/deployments"

    payload = json.dumps({
        "ref": 'master',
        'required_contexts': []
    })
    headers = {
        'Authorization': f'Basic {os.environ.get("BASIC_AUTH_TOKEN")}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.ok


def main():
    """Set up the github org and repo name
        Create the repo
        sleep for 10 seconds
        then deploy the website
    """
    github_org = "nss-day-cohort-test"

    repo_name = f'{github_org}.github.io'

    create_repo_from_template(github_org, repo_name)
    sleep(10)
    deploy_site(github_org, repo_name)


if __name__ == "__main__":
    main()
