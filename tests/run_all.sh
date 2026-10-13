#!/bin/sh
# Run every topic's tests (each folder separately: several define a module called `main`).
# Prints every test with its status, then a per-folder summary table.
cd "$(dirname "$0")" || exit 1
rc=0
summary=""
for d in */; do
  echo "== $d"
  out=$(python3 -m unittest discover -s "$d" -p 'test.py' -v 2>&1)
  status=$?
  echo "$out" | grep -E '\.\.\. |^Ran|^OK|^FAILED|^FAIL:|^ERROR:'
  [ $status -ne 0 ] && rc=1
  ran=$(echo "$out" | sed -n 's/^Ran \([0-9]*\) tests.*/\1/p')
  cases=$(ls "$d"*.in 2>/dev/null | wc -l | tr -d ' ')
  summary="$summary$(printf '%-24s %6s tests  %3s cases  %s' "$d" "$ran" "$cases" "$([ $status -eq 0 ] && echo PASS || echo FAIL)")
"
done
echo
echo "========== SUMMARY =========="
printf '%s' "$summary"
[ $rc -eq 0 ] && echo "ALL PASSED" || echo "SOME FAILED"
exit $rc
