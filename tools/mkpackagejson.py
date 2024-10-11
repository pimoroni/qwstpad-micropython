#!/bin/env python

import argparse
import json
from pathlib import Path


def repo_url(repo_url):
    if "git@github.com:" not in repo_url and "https://github.com:" not in repo_url and len(repo_url.split("/")) != 2:
        raise argparse.ArgumentTypeError(f"\"{repo_url}\" is not a valid GitHub URL")
    repo_url = repo_url.replace("git@github.com:", "")
    repo_url = repo_url.replace("https://github.com:", "")
    return repo_url

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--repo", type=repo_url)
parser.add_argument("-v", "--ver")
parser.add_argument("root", type=Path)

args = parser.parse_args()

try:
    data = json.load(open("package.json", "r"))
    print("package.json found: updating!")
except FileNotFoundError:
    data = {}
    print("package.json not found: creating!")

data.update({
    "version": args.ver,
    "urls": [],
})

for path in args.root.rglob("*"):
    if path.is_file():
        relpath = str(path.relative_to(args.root))
        print(f"Adding {relpath} as github:{args.repo}/src/{relpath}")
        data["urls"].append(
            [relpath, f"github:{args.repo}/src/{relpath}"]
        )

open("package.json","w").write(json.dumps(data, indent=True))