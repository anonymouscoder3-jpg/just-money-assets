# Just Money Playbook (Facebook image + text posts)

Trigger: Aastha says "run the Just Money playbook" (or similar) and attaches reference screenshots. Do NOT ask for computer/folder access. Everything needed lives in this Project and the GitHub repo.

## 0. Setup (every new session)
1. `project_read assets/README-avatar.md` and `assets/aastha-headshot.jpg.b64`, decode, verify sha256 `f0e8af61aff7bab22548b2e23a777d80be3ef5af48a562c15eca99c7c3182dfe`.
2. `add_repo anonymouscoder3-jpg/just-money-assets` (access: push), clone it. The renderer lives at `tools/render.py`, Montserrat fonts in `tools/fonts/`, Post Planner sheet builder at `tools/build_xlsx.py`.
3. Copy the headshot to `tools/headshot.jpg` (never commit it; it is in .gitignore).

## 1. Batch shape
- Default batch: 36 IMAGE posts + 27 TEXT posts, all for Facebook.
- One image post per reference screenshot Aastha uploads. Skip references outside personal finance/work/economy (for example, religious posts) and say so.
- Text posts are generated only after Aastha finishes sending text examples.
- Number batches: batch-01, batch-02, ... Check `posts/` in the repo for the next number.

## 2. Writing rules (card text)
- Slight variation of the reference: same hook, structure, length, CAPS style, concrete examples. Nudge numbers/ages a little; keep math consistent.
- NO first person (I, me, my, we, our, us, let's) in card or caption. Quoted speech from a form or a third party is ok sparingly.
- NO em dashes or en dashes. NO cursing or crude words (swap "screwed" to "squeezed", "dumb" to "makes zero sense").
- Facebook monetization safe: no fake news framing ("BREAKING" claims that aren't true), no engagement bait ("comment YES", "tag a friend", "share if"), no misleading stats, no graphic content.
- Fact-check every number with a current source (web search). Fix wrong or exaggerated claims and note the fix.
- No emoji on cards (font can't render them).
- Theme: dark card if the reference is dark; photo-meme references become dark cards.

## 3. Writing rules (long Facebook captions for image posts)
- 120 to 220 words. Goal: make people tap "See more".
- Line 1 to 2 = the hook, under ~120 characters, a tension or surprising number. Then a blank line.
- Short lines, one idea each, blank lines between blocks. Use "•" bullets and "1." numbered steps.
- Structure: hook, the problem in numbers, the twist or "what nobody tells you", 3 to 5 practical steps, one genuine question at the end, then 3 hashtags.
- Same voice rules: second person / general, no first person, no em dashes, no cursing.

## 4. Text posts (Facebook large-text style)
- Under 80 characters so Facebook shows big text. Bite-size, punchy, same voice rules.
- Go in their own Post Planner file (never mixed with image posts).

## 5. Render cards
- `python3 tools/render.py posts.json` produces 1080x1350 PNGs: avatar circle, "Just Money" + blue verified badge, "@JustMoney", bold Montserrat text auto-sized to fit; white or black theme.
- posts.json fields: n, slug, theme (light/dark), card, caption, optional max_size, file = `jm-bNN-XX-slug.png`.
- Look at a contact sheet of every card before shipping.

## 6. Host on GitHub
- Copy PNGs to `posts/batch-NN/` in the repo, commit, push to `main`.
- Public URL format: `https://raw.githubusercontent.com/anonymouscoder3-jpg/just-money-assets/main/posts/batch-NN/<file>.png`
- curl every URL and confirm HTTP 200 before building the sheet.

## 7. Post Planner bulk upload files
- `python3 tools/build_xlsx.py posts.json batch-NN image` (or `text`).
- Filenames: `justmoney_image_posts_<YYYY-MM-DD>.xlsx`, `justmoney_text_posts_<YYYY-MM-DD>.xlsx`.
- Sheet1, B1 = `BULK UPLOAD VERSION 3.1`, rows 1-4 are `##` header rows, posts start row 5.
- Columns: A POSTING TIME (empty = Posting Plan queue) | B CAPTION | C LINK | D MEDIA (raw GitHub URL) | E TITLE | F FIRST COMMENT | G FIRST COMMENT DELAY | H TOBI BACKGROUND | I REEL OR STORY.
- If Aastha re-sends her original template file, commit it to `templates/` and fill that copy instead.

## 8. Deliver
- Send the xlsx file(s) and a short review doc (what changed per post + sources).
- Commit posts.json to `posts/batch-NN/posts.json` as the record.
- Final message: what was made, anything skipped and why, next step.
