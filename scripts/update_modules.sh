#!/bin/bash


cd `dirname $0`
cd ..
git submodule foreach git pull origin master
git add source/vendor/choppy
git commit -m 'gitmodule choppy updated'

# TODO: multi module support
# git_modules=(
#     'source/vendor/choppy'
# )
