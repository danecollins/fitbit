#!/bin/bash

git fetch origin tested
git co tested
git merge master
git push
git co master

