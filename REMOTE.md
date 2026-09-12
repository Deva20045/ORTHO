# Remote / continuation info

- Repo: **https://github.com/Deva20045/ORTHO** (public, branch `main`)
- Owner GitHub username: `Deva20045`
- Push command: `bash work/push.sh Deva20045 <token> ORTHO` (token never stored in repo files)
- CONTINUE FLOW (new session, user says "continue"):
  1. `git clone https://github.com/Deva20045/ORTHO.git` (public → no token needed to read)
  2. Read PROGRESS.md → NEXT chapter (currently ch16)
  3. Ask user for that chapter's source PDF part (needs uploads/Orthopedics Marrow E8-101-204.pdf)
  4. Pipeline: render → transcribe → data/chNN.json → validate → merge → integrity → commit → `bash work/push.sh Deva20045 <token> ORTHO`
- App preview (if Pages enabled): https://deva20045.github.io/ORTHO/pulse-ortho-complete.html
