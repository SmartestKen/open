#!/bin/bash

clean_repo() {

cd $1
cp .git/config /tmp/config
rm -rf .git
git init
cp /tmp/config .git/config


ignore_files=`find . -type f -size +75M -not -path '*/\.git/*'`
if [[ $ignore_files != "" ]]
then
	sed 's|^\./||g' >"$1"/.git/info/exclude <<< "$ignore_files"
	echo "$ignore_files" | xargs git rm --cached 2>/dev/null
fi
git add .
git commit -m "$2"
git push -f origin master

}

pkill sync.sh
index=`tail -c 2 /etc/hostname`
clean_repo /home/ken/open laptop$index
clean_repo /home/ken/private laptop$index
clean_repo /home/ken/clips laptop$index
