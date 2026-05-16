#!/usr/bin/env bash

set +e

COMMIT=$(git rev-parse HEAD)

source dev.sh
dev test > ci/tests/test.log 2>&1
result=$?

test_stats=$(cat <<EOF
Tests completed for commit $COMMIT
\`\`\`yml
$(cat ci/tests/test.log | grep "Tests Results:" -A 10000)
\`\`\`
EOF
)

if [ $result -ne 0 ]; then
  body=$(cat <<EOF
❌ Tests failed for commit \`$COMMIT\`.

$test_stats
EOF
)

  gh pr comment "$PR_NUMBER" --repo "$REPO" --body "$body"
  exit 1
fi

