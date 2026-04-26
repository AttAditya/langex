#!/bin/bash
set -e

git fetch origin main:main

BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT=$(git rev-parse HEAD)
REPO_URL=$(git config --get remote.origin.url)

DIFF=$(git diff main HEAD)

TEMPLATE=$(cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "")

CONTENT=$(cat <<EOF
You are a PR summarizer.

Rules:
- Use ONLY the provided template structure
- Do NOT add explanations, headings, or metadata outside the template
- Keep output strictly concise and PR-ready
- No extra text outside the final filled template

Template:
$TEMPLATE

Git Diff:
$DIFF
EOF
)

AI_RESPONSE=$(curl -sS "$URL" \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": $(echo "$CONTENT" | jq -Rs .),
    \"repo\": \"$REPO_URL\",
    \"branch\": \"$BRANCH\",
    \"commit\": \"$COMMIT\"
  }" | jq -r '.content')

BODY=$(cat <<EOF
## Summary

$AI_RESPONSE
EOF
)

gh pr edit "$PR_NUMBER" --repo "$REPO" --body "$BODY"

