import os
import requests

GITHUB_API_REF_URL = "https://api.github.com/repos/sympy/sympy_gamma/git/matching-refs/heads/"
GITHUB_API_UPDATE_STATUS_URL = "https://api.github.com/repos/sympy/sympy_gamma/statuses/"


def get_branch_commit_sha(branch_name):
    response = requests.request("GET", GITHUB_API_REF_URL + branch_name)
    if response.status_code == 200:
        response_json = response.json()
    else:
        raise ValueError('Invalid response from github API')
    return response_json[0]['object']['sha']


def update_pr_status_with_deployment(branch_name, commit_sha):
    sympy_bot_token = os.environ.get('SYMPY_BOT_TOKEN')
    payload = {
        "state": "success",
        "target_url": "https://%s-dot-sympy-gamma-hrd.appspot.com" % branch_name,
        "description": "Deployment",
        "context": "PR Deployment"
    }

    headers = {
        'Authorization': 'token %s' % sympy_bot_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", GITHUB_API_UPDATE_STATUS_URL + commit_sha, headers=headers, data=payload)
    print "Response: %s" % response.json()


def main():
    is_on_travis = os.environ.get('TRAVIS')
    if not is_on_travis:
        raise ValueError('This script run only on travis!')
    branch_name = os.environ.get('TRAVIS_BRANCH')
    commit_sha = get_branch_commit_sha(branch_name)
    update_pr_status_with_deployment(branch_name, commit_sha)


if __name__ == '__main__':
    main()
