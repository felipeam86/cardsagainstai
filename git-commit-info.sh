#!/bin/bash

output_file="commits.json"
csv_file="commits.csv"

echo "[" > "$output_file"

first=true

git log --all --format=format:"%H" | while read -r commit_hash; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$output_file"
    fi

    full_message=$(git log -1 --pretty=format:"%B" $commit_hash)
    
    # Extract author and type emojis
    first_line=$(echo "$full_message" | head -n1)
    author=$(echo "$first_line" | grep -oE '^[^:]+' | tr -d ' ')
    type=$(echo "$first_line" | grep -oE ':[^-]+' | tr -d ' :')

    # Extract tools, prompts, and corrections
    tools=$(echo "$full_message" | sed -n 's/^tools: //p' | tr -d '\n')
    prompts=$(echo "$full_message" | grep -oE 'prompts: [0-9]+' | grep -oE '[0-9]+')
    corrections=$(echo "$full_message" | grep -oE 'corrections: [0-9]+' | grep -oE '[0-9]+')

    # Process the message: keep only the first line and trim initial emojis and dash
    message=$(echo "$first_line" | sed 's/^[^-]*- //' | sed 's/"/\\"/g')
    
    date=$(git log -1 --pretty=format:"%cd" --date=format:"%Y-%m-%d %H:%M:%S" $commit_hash)
    branch=$(git name-rev --name-only --refs="refs/heads/*" $commit_hash 2>/dev/null)

    if [[ $branch == "undefined" || -z $branch ]]; then
        branch=$(git rev-parse --short $commit_hash)
        commit_distance=""
    else
        # Extract commit distance from branch name
        if [[ $branch =~ ~([0-9]+)$ ]]; then
            commit_distance="${BASH_REMATCH[1]}"
            branch="${branch%~*}"
        else
            commit_distance="0"
        fi
    fi

    # Get the number of lines added and removed
    stats=$(git show --numstat --format="" $commit_hash | awk '{added+=$1; removed+=$2} END {print added, removed}')
    read lines_added lines_removed <<< "$stats"

    # Get the number of files changed
    files_changed=$(git show --stat --format="" $commit_hash | tail -n1 | grep -oE '[0-9]+ file[s]? changed' | grep -oE '[0-9]+')

    # Count the number of files in the codebase at this commit
    total_files=$(git ls-tree -r $commit_hash | wc -l)

    printf '  {\n' >> "$output_file"
    printf '    "commit_hash": "%s",\n' "$commit_hash" >> "$output_file"
    printf '    "author": "%s",\n' "$author" >> "$output_file"
    printf '    "type": "%s",\n' "$type" >> "$output_file"
    printf '    "message": "%s",\n' "$message" >> "$output_file"
    printf '    "date": "%s",\n' "$date" >> "$output_file"
    printf '    "branch": "%s",\n' "$branch" >> "$output_file"
    printf '    "commit_distance": %s,\n' "${commit_distance:-null}" >> "$output_file"
    printf '    "lines_added": %s,\n' "$lines_added" >> "$output_file"
    printf '    "lines_removed": %s,\n' "$lines_removed" >> "$output_file"
    printf '    "files_changed": %s,\n' "${files_changed:-0}" >> "$output_file"
    printf '    "total_files": %s,\n' "$total_files" >> "$output_file"
    printf '    "tools": "%s",\n' "$tools" >> "$output_file"
    printf '    "prompts": %s,\n' "${prompts:-null}" >> "$output_file"
    printf '    "corrections": %s\n' "${corrections:-null}" >> "$output_file"
    printf '  }' >> "$output_file"
done

echo -e "\n]" >> "$output_file"

echo "JSON output has been saved to $output_file"

# Convert JSON to CSV
jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.] | tostring)) as $rows | $cols, $rows[] | @csv' "$output_file" > "$csv_file"

echo "CSV output has been saved to $csv_file"