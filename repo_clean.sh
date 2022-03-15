#!/bin/bash



while IFS= read -r repo
do
	cd $repo
	mv .git/config /tmp/config
	mv .git/info/attributes /tmp/attributes
	rm -rf .git
	git init
	mv /tmp/config .git/config
	mv /tmp/attributes .git/info/attributes 

	# ignore_files=`find . -type f -size +75M -not -path '*/\.git/*'`
	# if [[ $ignore_files != "" ]]
	# then
		# sed 's|^\./||g' >"$1"/.git/info/exclude <<< "$ignore_files"
		# echo "$ignore_files" | xargs git rm --cached 2>/dev/null
	# fi
	git add .
	git commit -m "$device"
	git push -f origin master

done <<<"$repo_locations"
