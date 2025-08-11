#!/bin/bash
git subtree split --prefix=builder -b builder-branch
git push https://github.com/shminge/builder.git builder-branch:main --force
git branch -D builder-branch
