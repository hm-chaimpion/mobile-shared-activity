# Rules for AI models in mobile-shared-activity

Applies to every model (Grok Bot, Codex, Claude, any other), and to any agent that reads `AGENTS.md`.

1. **Read the activity's SPEC first.** It wins over everything else for that activity.
2. **Write only in your lane:** `activities/<activity>/lanes/<your-model>/`, plus one appended row in
   `REGISTER-activity.jsonl`. Never edit or delete another lane, the spec, or `skills/`.
3. **Add, never delete.** A new version is a new file or folder, not an overwrite.
4. **Public repo: secrets block, the rest gets noted.** Never commit keys, tokens, passwords, cookies or
   credentials: that blocks the push. Names, emails, local paths and client or company mentions are allowed;
   list any you include under "Privacy notes" in your run report.
5. **No questions, no waiting.** If blocked, log it (what failed, the error, the fix) and move on.
6. **Everything is auditable:** a checklist, a decisions log and a timed log in your lane. Every script or skill
   you create is saved in `created-tools/` and listed in `TOOLS-<model>.md`.
7. **HTML must be shareable:** one self-contained `index.html` per lane (inline CSS and JS, images inside the lane),
   readable through GitHub Pages without a login.
8. **Hand back = pushed:** a branch `lane/<model>/<activity>` with a pull request, or a direct commit touching only
   your lane. If you can't push, publish a zip of your lane somewhere public and log the link.
9. **End on mobile with a copyable hand-back.** The owner reads your reply on a phone. Your last message must be
   (a) a short plain list of what you did and what the owner needs to do next, then (b) **one fenced code block** with
   the full hand-back: lane, status (done/blocked counts), first-answer and end times, page URL, lane URL, the commit,
   the top 3 blocks or doubts, and the questions or decisions for the owner. Nothing that needs copying sits outside
   that block. The owner copies that block across to other models and to review.
10. **Every HTML or hosted artifact is replicable from the repo.** Its full source (HTML, CSS, JS, data, images) is
   committed in your lane, so anyone can rebuild it without your platform. If you also host it elsewhere (your own
   pages, canvas or artifact link), commit the same source too, check that link opens with no login, and record the
   result (URL, HTTP status, time) in your run report.
11. **File names have two or more chunks** (`RUN-REPORT-codex.md`, not `report.md`). Never name a file
   `claude.md`, `agents.md` or `notes.md`.
12. **Always point back to the creator.** When you process someone's video, post or talk, every output (ANSWER,
   page, method card, derivatives) names the creator and channel and links the original: the video, with timestamps for quotes,
   and their own sources. We process their work and always show where it came from; credit is one click from anything we make.
