#!/bin/bash

python3.14 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

cat << 'EOF' > .git/hooks/pre-commit
#!/bin/bash
scripts/pre-commit.sh
EOF

chmod +x gsrc.sh
chmod +x scripts/*.sh
chmod +x .git/hooks/pre-commit
