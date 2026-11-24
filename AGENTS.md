# Rules for AI models in mobile-shared-activity

Applies to every model (Grok Bot, Codex, Claude, any other), and to any agent that reads `AGENTS.md`.

1. **Read the activity's SPEC first.** It wins over everything else for that activity.
2. **Write only in your lane:** `activities/<activity>/lanes/<your-model>/`, plus one appended row in
   `REGISTER-activity.jsonl`. Never edit or delete another lane, the spec, or `skills/`.
3. **Add, never delete.** A new version is a new file or folder, not an overwrite.
4. **Public repo.** Nothing secret or private: no keys, tokens, cookies, emails, phone numbers, client data or
   local machine paths. Cite public URLs only.
5. **No questions, no waiting.** If blocked, log it (what failed, the error, the fix) and move on.
6. **Everything is auditable:** a checklist, a decisions log and a timed log in your lane. Every script or skill
   you create is saved in `created-tools/` and listed in `TOOLS-<model>.md`.
7. **HTML must be shareable:** one self-contained `index.html` per lane (inline CSS and JS, images inside the lane),
   readable through GitHub Pages without a login.
8. **Hand back = pushed:** a branch `lane/<model>/<activity>` with a pull request, or a direct commit touching only
   your lane. If you can't push, publish a zip of your lane somewhere public and log the link.
9. **File names have two or more chunks** (`RUN-REPORT-codex.md`, not `report.md`). Never name a file
   `claude.md`, `agents.md` or `notes.md`.
