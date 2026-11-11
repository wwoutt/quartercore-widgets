# Adding a widget

1. Fork this repository.
2. Add a folder `widgets/<id>/` (lowercase letters, digits, `-` and `_`) with at
   least `widget.json` and `widget.html`. How a widget works is described in the
   [widget guide](https://github.com/wwoutt/quartercore/blob/main/docs/WIDGETS.md),
   or generate one with the
   [AI prompt](https://github.com/wwoutt/quartercore/blob/main/docs/WIDGETS.md#ai-prompt).
   AI-generated widgets are welcome; you are responsible for having read and
   tested the code.
3. `widget.json` must contain `name`, `description`, `author`, `license` and
   `version`. The license must be GPL-compatible (SPDX id, e.g. `MIT`,
   `GPL-3.0-or-later`, `Apache-2.0`).
4. Run `python3 tools/build-index.py` and commit the updated `index.json`.
5. Open a pull request. The check must pass before review.

## Rules
- Flat folder: no subfolders or links, at most 30 files, 512 KB per file and
  2 MB in total. Allowed types: `.json .html .css .js .py .sh .png .jpg .jpeg
  .svg .webp .md .txt` and `LICENSE`.
- No secrets in the widget. Ask for them with `settings` in `widget.json`
  (type `secret` for tokens and keys).
- Readable code only: no minified or obfuscated scripts, no downloading and
  running other code.
- Data scripts (`data.py`, `.sh`) only read data and print JSON. They must not
  change the system, need root, or send personal data anywhere.
- Action scripts (`action.py`) check every request against a fixed list of
  allowed operations and only do what the widget is meant to do.
- Describe in `description` which websites a `url` source or script contacts.

## Review checklist (maintainers)
- [ ] `tools/build-index.py --check` passes
- [ ] License is GPL-compatible and the author is credited
- [ ] Script code is readable, read-only (data) or allowlisted (actions), and matches the description
- [ ] Contacted websites match the description, no tracking
- [ ] Works in the kiosk (sandboxed, no network access from the widget itself)
