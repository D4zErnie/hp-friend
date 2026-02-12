#!/bin/bash
set -e

# This script fetches remote history and identifies branches that are merged into the main branch.
# It then generates the commands to delete these branches from the remote (closing the associated PRs).
#
# Usage: ./scripts/generate_cleanup_commands.sh
#
# Note: This script only prints the commands. You must run them manually.
# Note: This script uses 'git branch --merged', so it may not detect branches merged via 'Squash and Merge'
#       unless the commit message or content is identical.

MAIN_BRANCH="origin/main"

echo "Fetching latest history (depth=1000)..."
git fetch origin --depth=1000

echo "Identifying merged branches..."
# We exclude HEAD and main/master
# The regex ensures we only exclude lines ending with /main or /master or HEAD -> ...
# We add '|| true' to prevent script exit if grep finds nothing (which means no merged branches found)
MERGED_BRANCHES=$(git branch -r --merged $MAIN_BRANCH | grep -vE 'HEAD ->|origin/main$|origin/master$' || true)

if [ -z "$MERGED_BRANCHES" ]; then
    echo "No merged branches found."
else
    echo "The following branches are merged into $MAIN_BRANCH:"
    echo "$MERGED_BRANCHES"
    echo ""
    echo "----------------------------------------------------------------"
    echo "To close these Pull Requests and delete the remote branches, run:"
    echo "----------------------------------------------------------------"

    echo "$MERGED_BRANCHES" | while read branch; do
        clean_branch=$(echo "$branch" | sed 's/^[[:space:]]*//' | sed 's/^origin\///')

        if [ -n "$clean_branch" ]; then
            echo "git push origin --delete $clean_branch"
        fi
    done

    echo "----------------------------------------------------------------"
    echo "Note: Ensure you have push permissions before running these commands."
fi
