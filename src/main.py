import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()


def _shell(cmd):
    print(">", cmd)
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def _cd(work_dir):
    os.chdir(work_dir)


def _seek_developer_work_dir():
    """查找开发者目录"""
    developer_work_dirs = [
        "/Users/crow/project/",
        "/Users/one/project/",
        "/Users/viktor/project/",
        "/Users/lee/PycharmProjects/",
        '/Users/johnnyli/project/',
        "/Users/johnnyli/Documents/GitHub/",
        "/Users/philkruppa/project/"
    ]

    for work_dir in developer_work_dirs:
        if os.path.exists(work_dir):
            return work_dir

    raise Exception("Developer work dir not found")


def github(developer_work_dir, token, proxy=None):
    url = "https://api.github.com/user/repos"

    headers = {"Authorization": f"Bearer {token}"}

    # Fetch all repositories by handling pagination
    all_repos = []
    page = 1
    per_page = 100  # Adjust the number of repos per page as per GitHub's API limit

    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            repos = response.json()
            if len(repos) == 0:
                break
            all_repos.extend(repos)
            page += 1
        else:
            error_message = f"Failed to fetch repositories: {response.json()}. Status code: {response.status_code}"
            raise Exception(error_message)

    for repo in all_repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        if repo_name in ["code", "diagnosis", "health_care"]:
            # 跳过大文件
            continue

        if os.path.exists(f"{developer_work_dir}/{repo_name}"):
            print(repo_name + " 已存在，即将切换到 master 进行更新")
            _cd(f"{developer_work_dir}/{repo_name}")
            _shell(
                f"{proxy} && git switch master && git pull origin master" if proxy else "git switch master && git pull origin master")
        else:
            print(repo_name + " 不存在， 即将 clone " + clone_url)
            if proxy:
                _shell(f"cd {developer_work_dir} && {proxy} && git clone {clone_url}")
            else:
                _shell(f"cd {developer_work_dir} && git clone {clone_url}")


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        raise Exception("Environment variable TOKEN is not set")

    proxy = os.getenv("PROXY")

    developer_work_dir = _seek_developer_work_dir()
    github(developer_work_dir, token, proxy)
