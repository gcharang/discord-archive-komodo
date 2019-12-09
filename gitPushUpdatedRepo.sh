#!/bin/bash

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI - gcharang"
}

commit() {
  git add -f docs
  git commit --message "[skip ci] Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote rm origin
  git remote add origin https://gcharang:${GH_TOKEN}@github.com/gcharang/discord-archive-komodo.git > /dev/null 2>&1
  git push --quiet --set-upstream origin master 
}

setup_git
commit
upload_files
