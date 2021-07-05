#!/usr/bin/env bash

git_branch=$(git rev-parse --abbrev-ref HEAD | tr /: _)
git_commit=$(git rev-parse HEAD)
git diff-index --quiet HEAD

if [[ $?  == 0 ]]; then
  suffix='-dev'
else
  suffix=''
fi
docker build ../ -f ./Dockerfile  -t cwl-airflow:${git_branch}-${git_commit}${suffix}
