# Ledu — Implementation Playbook

---

## 0  Purpose of this Document

You will use this file as a **living checklist** while turning the Ledu
skeleton into a working Markdown → Notion converter.  Read from top to bottom;
complete each numbered task; check ☑︎ items off in Git commits; push early and
often.

---

## 1  Repository Layout Recap

````text
src/ledu/
├── cli.py                # entry‑point → `ledu` CLI script
├── config.py             # global settings + converter registry
│
├── parser/               # Markdown   →  internal tokens
│   ├── markdown_parser.py
│   └── rich_text.py      # inline splitter
│
├── blocks/               # one converter class per Notion block‑type
│   ├── base.py           # BlockConverter ABC + ConversionContext
│   ├── paragraph.py      # paragraph_open               (Phase 1)
│   ├── heading.py        # heading_open *(h1–h3)*        (Phase 2)
│   ├── list_item.py      # list_item_open               (Phase 3)
│   ├── code.py           # fenced ` ``` `               (Phase 4)
│   ├── table.py          # table_open                   (Phase 5)
│   ├── media.py          # image / video / audio        (Phase 6)
│   └── advanced.py       # toggle / columns / …         (Phase 7)
│
├── builder/
│   └── page_builder.py   # orchestrates token walk
│
├── notion/
│   ├── client.py         # thin wrapper around notion‑client SDK
│   └── upload.py         # convenience helpers (optional)
│
└── utils/                # tiny shared helpers (typing, enums, errors)
````

Orange   = **edit most often** • Green   = rarely touched once stable.

---

## 2  Installation & First Smoke Test (☑︎ **Task 0**)

```bash
poetry install          # installs markdown‑it‑py, notion‑client, pytest …
pytest -q               # should show 2 passed, 1 skipped
ledu --help             # CLI prints usage (dry‑run)
```

If any step fails, fix imports **before** writing new code.

---

## 3  Implementation Road‑map

> **Rule of thumb**: one feature, one commit, one new green test.

| Phase  | Goal                        | Main files you touch                                                 | New tests to add                    |
| ------ | --------------------------- | -------------------------------------------------------------------- | ----------------------------------- |
| **1**  | Inline splitter + paragraph | `parser/rich_text.py`, `blocks/paragraph.py`, `tests/test_blocks.py` | *paragraph\_basic.md/expected.json* |
| **2**  | Headings (H1‑H3)            | `blocks/heading.py`                                                  | *heading\_h1.md*                    |
| **3**  | Lists (bulleted/numbered)   | `blocks/list_item.py`, extend `ConversionContext`                    | *nested\_lists.md*                  |
| **4**  | Fenced code blocks          | `blocks/code.py`                                                     | *code\_python.md*                   |
| **5**  | Simple tables (2×2)         | `blocks/table.py`                                                    | *table\_basic.md*                   |
| **6**  | Images/Video/Audio          | `blocks/media.py`                                                    | remote URL fixture                  |
| **7**  | Toggles + Columns           | `blocks/advanced.py`                                                 | toggle fixture                      |
| **8**  | CLI upload flag             | `cli.py`, `notion/client.py`                                         | record HTTP with `pytest‑vcr`       |
| **9**  | Config from ENV             | `config.py`                                                          | unit‑test settings override         |
| **10** | Documentation & Release     | `README.md`, `CHANGELOG.md`                                          | –                                   |

Each phase builds on the previous; **do not** jump ahead.

---

## 4  Per‑File Responsibilities

### 4.1  `parser`

* **`markdown_parser.MardownParser`**  — wraps *markdown‑it‑py*.  Rarely
  changes after you enable required extensions (`table`, `strikethrough`).
* **`rich_text.RichTextSegmenter`**    — *heart of inline fidelity*; converts a
  raw string like `"**States ($S$):**"` into a list of `RichTextRun`s with
  correct `annotations` & optional `equation` field.  Start with bold/italic ‑→
  add code, then LaTeX, then links.

### 4.2  `blocks`

Every module defines **one `BlockConverter` subclass**.

```python
class ParagraphConverter(BlockConverter):
    token_types = ("paragraph_open",)

    def to_notion(self, token, tokens, idx, context):
        # build and return [paragraph_dict]
```

* You may look‑ahead in *tokens* to read until the matching `_close` token.
* Always `return List[JSONDict]` even if it (currently) has one item.
* If you consume additional tokens, PageBuilder can later be taught to advance
  `idx` by more than 1 via `context` — keep it simple initially.

### 4.3  `builder.page_builder.PageBuilder`

*Walks* the token stream, dispatches to converters.  After lists/columns work
it might need smarter depth bookkeeping, but for now a simple `while` loop is
fine.

### 4.4  `notion`

* `client.py` — wrap `notion_client.Client` so the rest of the code never
  imports the SDK directly (easy to mock in tests).
* `upload.py` — optional convenience for *future* live syncs; ignore until core
  conversion passes all local tests.

### 4.5  `cli.py`

* Parses `--dry` vs real upload.
* Reads token from `config.settings` (later from `NOTION_TOKEN`).

---

## 5  Testing Strategy

1. **Unit fixtures**   — Markdown snippet in `tests/fixtures/*.md` + expected
   Notion JSON in `*.json`.  Use small, isolated cases.
2. **Integration**     — `test_roundtrip.py` (currently skipped) converts a
   multi‑block document once all converters exist.
3. **Live smoke**      — only after Phase 8: push to a real Notion page when
   `LIVE_NOTION_TOKEN` env var is present; mark with `@pytest.mark.live`.

*(json fixtures are best hand‑written first, then regenerated via a script once
you trust the converter.)*

---

## 6  Daily Workflow Checklist

1. Pull latest `main` → create *feature branch* `feat/phase‑X‑paragraph`.
2. Write failing test in `tests/fixtures/` + update `tests/test_blocks.py`.
3. Implement code until `pytest -q` is green.
4. Run `ruff format && ruff check` (optional lint).
5. Commit with message `feat: paragraph converter`.
6. Open PR, merge; bump version if API visible.

Rinse‑and‑repeat for each phase.

---

## 7  FAQ / Tips

* **Where do I debug token streams?**  Add `print(token.type, token.meta)` in
  `tests/manual_token_inspect.py` or use `rich` to pretty‑print.
* **Performance** is fine; markdown‑it‑py parses 1 MB in <50 ms.  Optimise
  only if profiling shows bottleneck.
* **Notion API limits** — 100 blocks per call.  For large docs add batching
  logic later.
* **Colour mapping** — use `utils.enums.Color` enum when you wire callouts.

---

## 8  Done‑for‑now Roadmap ©

Once Phase 10 ships you will have:

* End‑to‑end Markdown ➜ Notion page creation.
* 90 % block‑type coverage (everything listed in original spec).
* Configurable via `.env` or `settings.toml`.

Beyond that you can explore **reverse conversion**, **watch‑mode auto‑sync**,
and **diagram rendering (Mermaid → SVG)**.

> Happy coding – stay incremental, keep tests green.

