+++
title = "My Git Handbook"
date = 2023-09-01
tags = ["git"]
+++

My git handbook covering some of the commands which I use every other day.

- Ignore files only for you without using .gitignore - add the patterns to exclude in `.git/info/exclude` file
- Get summary of stashes: `git stash list --stat`
- Checkout a branch from remote: `git pull <remote> <remote-branch-name>; git checkout -b <local-name> <remote>/<remote-branch-name>`.
Ex: `git checkout -b test upstream/test`

- Pull and rebase: `git pull upstream main --rebase`

- Git checkout a pull request from github: `git fetch upstream pull/$ID/head:$branchname` 

- Git show files changed in commit: `git show commit-id --name-only`
- Git show files changed between commits: `git show commit-id1..commit-id2 --name-only`
- Get permalink from github cli: Ex: `gh browse README.md:3-5 --no-browser --commit=$(git rev-parse HEAD)`

- Git reset local to upstream: `git fetch upstream; git reset --hard upstream/main`

- Git view a file history: `git log --follow <filename>`

- Checkout changes from a file from a different branch: `git checkout myotherbranch <filename>`

- Delete a remote branch: `git push -d origin <branch-name>`

- Git rebase interactive example: `git rebase -i HEAD~5`
