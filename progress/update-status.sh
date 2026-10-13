#!/bin/bash
# Usage: bash progress/update-status.sh <slug> <agent-name> <message>
# Updates CURRENT, LAST_EVENT, and LAST_UPDATE in progress/<slug>.status
# Called by agents at each progress step so the status line reflects real-time sub-step detail.

SLUG=$1
AGENT=$2
MESSAGE=$3

python3 - "$SLUG" "$AGENT" "$MESSAGE" <<'EOF'
import sys, re
from datetime import datetime

slug, agent, message = sys.argv[1], sys.argv[2], sys.argv[3]
path = f'progress/{slug}.status'
ts = datetime.now().strftime('%H:%M:%S')

try:
    with open(path, 'r') as f:
        content = f.read()
    content = re.sub(r'CURRENT=.*', f'CURRENT={agent}: {message}', content)
    content = re.sub(r'LAST_UPDATE=.*', f'LAST_UPDATE={ts}', content)
    content = re.sub(r'LAST_EVENT=.*', f'LAST_EVENT={agent}: {message}', content)
    with open(path, 'w') as f:
        f.write(content)
except FileNotFoundError:
    pass  # No status file yet — skip silently
EOF
