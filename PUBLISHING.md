# Describe → edit → preview → commit → approve → publish

This is a plain HTML/CSS site hosted on GitHub Pages. There is no JavaScript
framework, database or build step. A commit saves a version; publishing changes
what visitors see. They are separate actions.

## Where things live

| File or HTML | What it controls |
| --- | --- |
| `index.html` | Homepage text, featured cards, About, Contact and LinkedIn link |
| `insights.html` | Published Insights index |
| `essays/why-ai-adoption-is-a-management-problem.html` | The first article; its existing URL stays valid |
| `insights/your-slug.html` | Location for new approved articles |
| `styles.css` | Shared colours, fonts, layout, spacing and mobile rules |
| `AGENTS.md` | Entry-point instructions for agents working in this repository |
| `WRITING.md` | Voice, zero-em-dash rule and sentence-pattern editing |
| `EDITORIAL.md` | Evidence, input contract and editorial approval checks |
| `_templates/article.html` | Copyable article structure; not a published article |
| `essays.html` | Compatibility redirect to Insights; keep it for old links |
| `<a href="/insights.html">Insights</a>` | `href` is the destination; the text between tags is the label |
| `<link rel="stylesheet" href="../styles.css">` | Loads the shared CSS from one folder up |
| `<title>` and `<meta>` inside `<head>` | Browser/search/sharing information, not the visible article body |

In `styles.css`, `:root` holds the colour variables. `body` sets the font family
and default line height. `.article-body` controls reading width and paragraph
typography. `padding`, `margin` and `gap` control spacing. The `@media` rules
adapt the layout below 800px and 520px. Keep [DESIGN.md](DESIGN.md) as the visual brief.

## 1. Describe and branch

Name the desired result, affected page, text to use, things to preserve and how
you will check it. Example: “Change the second homepage card to the approved
meeting-preparation playbook; keep the buying-window card third and preserve
the typography. Prepare a preview; do not publish.”

Read `AGENTS.md` and its linked guides first. With a GitHub-only connector, fetch
them explicitly; do not assume a website URL loads repository instructions.

Use a fresh working branch based on the latest `main`. The original foundation
PR used `system/insights-publishing` and is now merged. Use branches such as
`system/writing-guidance` or `content/meeting-preparation` for later changes.
Do not edit `main` directly during review.

Important: this repository and its branches are public. Store voice transcripts,
drafts, private metrics and customer notes in a separate private location.
A draft pull request is a review state, not a privacy control.

## 2. Edit approved material

Copy `_templates/article.html` to `insights/your-slug.html` and replace every
`{{TOKEN}}`. Use a lowercase, hyphen-separated slug. Keep the original article
at its existing `/essays/` path; there is no need to rename a working URL.

Set the title, short description, deck, format, subject, publication date and
reading estimate. Update repeated title/description fields in `<head>`, then
add a linked entry to `insights.html` and update the relevant homepage card.
Dates should reflect actual publication, not drafting. Escape `&` as `&amp;`
and quotation marks inside attribute values as `&quot;`.

Upcoming cards stay unlinked and say “Coming soon” until the actual article is ready.
For now, metadata is repeated manually so the HTML is easy to inspect. Revisit
a small static generator after the first three posts establish a stable template.

## 3. Check and preview before saving a revision

From the downloaded or cloned repository folder, with Python 3 installed:

```sh
python3 scripts/check_site.py
python3 -m http.server 8000 --bind 127.0.0.1
```

On Windows, use `py -3` instead of `python3` if needed. Open
`http://localhost:8000` in your browser; press Ctrl+C in the terminal to stop.
Do not simply double-click HTML files: links starting with `/` expect a web server.
This preview runs on your computer; it is not a public deployment.

- Open Home → Insights → the article → All insights.
- Check that `/essays.html` redirects to Insights and the original article URL works.
- Confirm the LinkedIn button points to Alex's profile.
- Use right-click → Inspect. In Elements, find a heading, its `href` and stylesheet link.
- In Styles, try changing a margin or colour. Browser edits are temporary; refresh resets them.
- Toggle the device toolbar and inspect widths around 390px and 1440px, plus a narrow 320px screen.
- Check navigation, wrapping, horizontal scrolling, article reading width and keyboard focus.
- Record actual results; automated checks do not establish visual correctness.

GitHub's **Files changed** tab is a code diff, not a rendered website preview.
GitHub Pages does not automatically provide a separate preview URL for each PR.
No preview hosting service is installed by this workflow. A separate hosted
preview needs a deliberate future setup; local review works without one.

## 4. Save/commit and open a pull request

Review the diff for unexpected changes, then commit only the intended files on
the working branch. Push it and open a draft pull request into `main`. Include:

- What changed and why.
- The previewed revision and commands/checks run.
- Desktop/mobile review results or an explicit “not yet checked”.
- Anything still missing and a clear “Do not merge until Alex approves”.

The included GitHub Actions workflow runs the local checker on pull requests
and on `main`. It checks structure, local links, shared CSS, sharing metadata and
the zero-em-dash rule for public HTML, the template and project writing guides;
it does not publish. The check is not enforced unless branch protection is
configured separately. No protection or repository settings are changed here.

## 5. Approve, then publish

Alex approves the exact reviewed revision. Approval of an earlier version does
not cover later edits. Mark the PR ready and merge only after approval.
Before merging, confirm in **Settings → Pages** that `main` is the publishing
source, or inspect the configured deployment workflow. With Pages publishing
from `main`, merging starts deployment. Wait for deployment to finish, then
open the live homepage, index and article; test old URLs too.

Run the published URL through LinkedIn's Post Inspector if a preview is stale:
https://www.linkedin.com/post-inspector/ . Sharing services may cache cards.
Open Graph and X metadata specify title/description/URL. No share image is
provided yet, and the platforms decide the final presentation.

### Planned social-sharing image setup

After the article's title and description are approved, prepare one reusable
landscape title-card design, approximately 1200 by 630 pixels. Match DESIGN.md:
warm off-white, charcoal text, one dark-green accent and no generic AI imagery.
Export a title-specific PNG or JPEG into `assets/images/` and inspect its text
and legibility at a small preview size. Keep its headline consistent with the article.

In the article's `<head>`, add `og:image`, `og:image:alt`, image dimensions and
`twitter:image` with absolute public image URLs; change `twitter:card` to
`summary_large_image` only when that page has a real, accessible image. Add
`twitter:image:alt` too. Extend the checker and tests to accept image cards only
with valid image metadata. Do not switch unrelated pages to large-image cards.

Preview the image and metadata in the PR, obtain approval, publish, then check
the live image and LinkedIn Post Inspector. Preview caches may need refreshing.
No image or automated card generator has been created by these instructions.
Manual X distribution does not require a paid connector.

Do not claim “published” based only on a successful commit. If the live check
fails, report it and fix on a new branch. Reverting a merged PR creates a
traceable undo commit; avoid force-pushing or deleting history.

## What remains deliberately separate

- Private Obsidian vault setup and device syncing.
- The installable Alex GTM Content System skill.
- Article 2 evidence/interview and article 3 experiment.
- Analytics connections, engagement collection and scheduled reminders.
- A static generator after the first three posts; no framework migration needed.
