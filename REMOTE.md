# Remote / continuation info

- Repo (to be created on first push): `pulse-ortho` (public, per user's choice)
- Push command: `bash work/push.sh <username> <token>` (token never stored in repo)
- CONTINUE FLOW (new session, user says "continue"):
  1. If repo URL known: `git clone https://github.com/<user>/pulse-ortho.git` (public → no token needed to read)
  2. Read PROGRESS.md → NEXT chapter
  3. Ask user for that chapter's source PDF part
  4. Pipeline: render → transcribe → data/chNN.json → validate → merge → integrity → commit → `bash work/push.sh <user> <token>`
- NOTE: after first push, also update this file with the final URL.
