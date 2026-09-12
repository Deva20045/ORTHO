#!/usr/bin/env bash
# Push this project to GitHub. Usage:
#   bash work/push.sh <username> <token> [repo-name]   (creates repo if missing, then pushes)
# Example:
#   bash work/push.sh ravi ghp_xxxx pulse-ortho
set -e
USER="${1:?usage: push.sh <username> <token> [repo-name]}"
TOKEN="${2:?usage: push.sh <username> <token> [repo-name]}"
REPO="${3:-ORTHO}"
cd "$(dirname "$0")/.."

# does the repo exist?
CODE=$(curl -s -o /tmp/ghrepo.json -w "%{http_code}" \
  -H "Authorization: token $TOKEN" "https://api.github.com/repos/$USER/$REPO")
if [ "$CODE" = "404" ]; then
  echo "creating repo $USER/$REPO ..."
  CODE=$(curl -s -o /tmp/ghrepo.json -w "%{http_code}" -X POST \
    -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \
    -d "{\"name\":\"$REPO\",\"private\":false,\"description\":\"PULSE Orthopaedics quiz app - Marrow E8 companion (in progress)\"}" \
    https://api.github.com/repos)
fi
[ "$CODE" = "200" ] || [ "$CODE" = "201" ] || { echo "GitHub API error $CODE:"; cat /tmp/ghrepo.json; exit 1; }

git remote remove origin 2>/dev/null || true
git remote add origin "https://$TOKEN@github.com/$USER/$REPO.git"
git push -u origin main
echo "---- pushed to https://github.com/$USER/$REPO ----"
echo "https://$USER.github.io/$REPO/pulse-ortho-complete.html  <- will work after GitHub Pages is enabled (repo Settings -> Pages -> main branch)"
