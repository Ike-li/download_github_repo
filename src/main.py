import os
import subprocess

import requests
from dotenv import load_dotenv

load_dotenv()


# TODO 这个函数名想一下
def github(developer_work_dir, token, proxy):
    url = "https://api.github.com/user/repos?type=all&sort=updated"

    payload = {}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.request("GET", url, headers=headers, data=payload)

    if "message" in response.json():
        raise "Token is expire"

    for repo in response.json():
        repo_name = repo["name"]
        clone_url = repo["clone_url"]

        if os.path.exists(f"{developer_work_dir}/{repo_name}"):
            print(repo_name + " 已存在，即将切换到 master 进行更新")
            _shell(
                f" cd {developer_work_dir}{repo_name} && {proxy} && git switch master && git pull origin master"
            )

            if os.path.exists(f"{developer_work_dir}/{repo_name}/docker"):
                print(repo_name + " 存在 docker 目录，即将启动")
                _shell(
                    f"cd {developer_work_dir}/{repo_name}/docker && docker-compose up -d"
                )
                print(repo_name + " docker 启动完成")
        else:
            print(repo_name + " 不存在， 即将 clone " + clone_url)
            _shell(
                f"cd {developer_work_dir} && {proxy} && git clone {clone_url}")
            # gh repo clone user_name/repo_name 可能会更快


def _shell(cmd):
    print(">", cmd)
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def _seek_developer_work_dir():
    """查找开发者目录"""
    developer_work_dirs = [
        "/Users/crow/project/",
        "/Users/one/project/",
        "/Users/viktor/project/",
        "/Users/leo/PycharmProjects/",
    ]

    for work_dir in developer_work_dirs:
        if os.path.exists(work_dir):
            return work_dir

    raise Exception("Developer work dir not found")


if __name__ == "__main__":
    token = os.getenv("TOKEN")
    proxy = os.getenv("PROXY")
    developer_work_dir = _seek_developer_work_dir()
    github(developer_work_dir, token, proxy)
