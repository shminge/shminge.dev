#!/bin/bash
set -e  # Exit on errors

# Ensure dist/ is linked to gh-pages branch
if [ ! -d "dist/.git" ]; then
    echo "Setting up gh-pages worktree..."
    git worktree add dist gh-pages
fi

# Build your site
./build.sh

# Commit and push
cd dist
git add --all
git commit -m "Publish $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit."
git push origin gh-pages
cd ..
