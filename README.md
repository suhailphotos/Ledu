# Notion Markdown Converter (Python)
_A toolkit to convert Markdown content into Notion API block structures with high-fidelity formatting and block-type mapping._

---

## **Project Objective**

Develop a Python package that parses Markdown and outputs a list of Notion API-compatible block objects, faithfully preserving:

- All supported Notion block types (basic, media, advanced, etc.)
- Rich text formatting (bold, italic, code, links, color, equations)
- Inline and block equations (LaTeX)
- Nested structures (lists, toggles, columns, etc.)
- Annotation context splitting (bold + inline math, code in list items, etc.)

---

## **Core Features**

### 1. **Markdown to Notion Block Conversion**

- **Parse Markdown** and generate an ordered list of Notion API blocks (`dict` format).
- **Preserve structure and nesting** as per Markdown input.

### 2. **Rich Text Segmentation**

- **Segment text runs** by formatting boundary:  
  - Bold, italic, underline, code, color
  - Inline equations (`$...$`)
  - Inline code (`` `...` ``)
- **Mixing formats:**  
  - Example: `**States ($S$):** All possible situations...`  
    - Must become:  
      - `"States ("` (bold)  
      - `"S"` (equation + bold)  
      - `"):"` (bold)  
      - `" All possible situations..."` (normal)

### 3. **Block Type Coverage**

**Support the following block types (with example input → output mapping):**

#### **Basic Blocks**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `Text`           | `paragraph`      | |
| `# Heading 1`    | `heading_1`      | |
| `## Heading 2`   | `heading_2`      | |
| `### Heading 3`  | `heading_3`      | |
| `- List item`    | `bulleted_list_item` | |
| `1. List item`   | `numbered_list_item` | |

#### **Toggle Blocks**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `<details><summary>Summary</summary>Content</details>` or `??? Toggle` | `toggle` | Toggle heading 1/2/3, Toggle list |

#### **Quote / Callout**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `> Quote`        | `quote`          | |
| `> [!NOTE] Callout` | `callout`     | Custom icon/color support |

#### **Dividers and Tables**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `---`            | `divider`        | |
| Markdown Table   | `table`          | |

#### **Media Blocks**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `![Alt](url)`    | `image`          | |
| `[video](url)`   | `video`          | |
| `[audio](url)`   | `audio`          | |
| `[File](url)`    | `file`           | |
| `[Bookmark](url)`| `bookmark`       | Web bookmarks |

#### **Code**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| ```` ```python ... ``` ```` | `code` | Language support, code caption |
| `` `inline code` `` | Inline `text` | `annotations.code = true` |

#### **Equations**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `$$ ... $$`      | `equation` (block) | |
| `$...$` (inline) | Inline equation   | Must be in `.text` array with context |

#### **Columns**
| Markdown Example | Notion Block Type | Notes |
|------------------|------------------|-------|
| `:::columns ... :::` | `column_list`  | Nested blocks as column children |

#### **Synced, Breadcrumb, Button, Table of Contents, AI Block**
- Allow simple syntax or special markers for:
    - Synced block (`:::synced`)
    - Breadcrumb (`:::breadcrumb`)
    - Button (`[Button](action)`)
    - Table of Contents (`[TOC]`)
    - AI Block (`:::ai-block`)
    - Mermaid code block for diagrams

---

## **Rich Text Handling and Edge Cases**

- **Split any block into multiple `text` runs as needed:**
    - Example:  
      Markdown: `**States ($S$):** ...`  
      Notion:  
      ```json
      [
        {"type": "text", "text": {"content": "States ("}, "annotations": {"bold": true}},
        {"type": "equation", "equation": {"expression": "S"}, "annotations": {"bold": true}},
        {"type": "text", "text": {"content": "):"}, "annotations": {"bold": true}},
        {"type": "text", "text": {"content": " All possible situations..."}, "annotations": {"bold": false}}
      ]
      ```
- **Handle multiple annotations (bold+italic+code) per segment.**
- **Support hyperlinks, mentions (with special markdown syntax or tag).**

---

## **Nested & Complex Structures**

- **Nested lists:**  
  Markdown’s nested lists → children in Notion block structure
- **Toggle blocks, column blocks, table blocks**:  
  Parse and create nested children lists as per Notion API.

---

## **Examples for Each Block**

### **Paragraph with Mixed Content**
Markdown:
- States ($S$): All possible situations…
Output:
- `bulleted_list_item` with 4 `text` segments, including inline equation.

### **Heading with Inline Equation**
Markdown:
**Policy ($\pi$)**
Output:
- `heading_2` with rich text: `"Policy ("`, equation `"\\pi"`, `")"`

### **Code Block**
Markdown:
    ```python
    print("Hello")
    ```
Output:
- `code` block, language = python, content = print("Hello")

### **Image**
Markdown:
    ![Alt](https://example.com/img.png)
Output:
- `image` block with external URL

### **Table**
Markdown:
    | A | B |
    |---|---|
    | 1 | 2 |
Output:
- `table` block, rows/columns parsed accordingly

### **Inline Code**
Markdown:
    Here is `inline code`.
Output:
- `paragraph` with text run (normal), text run (code), text run (normal)

---

## **Advanced Features**

- **Customizable mapping:**  
  Allow user to define/extend block type mapping or handle unknown blocks gracefully.
- **Extensible:**  
  Support for new Notion block types as Notion updates API.

---

## **Non-Goals**

- Does not attempt to round-trip Notion → Markdown (unless explicitly developed for this).
- Does not handle Notion database pages (just blocks/pages for content).

---

## **Summary**

This package should serve as a **high-fidelity Markdown-to-Notion converter** with fine-grained control over rich text and block types, designed for programmatic page building via the Notion API. All text formatting, equations, code, lists, tables, and advanced block types (AI, Mermaid, columns, etc.) are supported.

---

# Ledu — Development Guide

> **Purpose:** This document walks you (the implementer) through the recommended build order, core responsibilities, and testing rhythm for each module in the Ledu Markdown → Notion toolkit.

---

## 1  High‑Level Architecture

```text
Markdown (raw string)
    │  (1)
    ▼
MarkdownParser  ──►  Token list (markdown‑it‑py)
    │  (2)
    ▼
PageBuilder  ──►  BlockConverter registry  ──►  Notion‑style JSON blocks
    │  (3)                             ▲
    │                                   │
    └──► NotionClient (optional upload) ─┘
```

1. **MarkdownParser**   — Converts raw Markdown into a stable token stream.
2. **PageBuilder**      — Walks the token stream, dispatching each token to the correct **BlockConverter** subclass (paragraph, heading, list, …).
3. **BlockConverters**  — Transform tokens into **Notion‑ready block dictionaries**; rely on **RichTextSegmenter** for inline splitting.

All singletons (settings, registry) live in **`config.py`** so the rest of the code stays stateless.

---

## 2  Implementation Milestones

| Phase | Goal                                              | Key modules                                  | Tests to add                        |
| ----- | ------------------------------------------------- | -------------------------------------------- | ----------------------------------- |
| **0** | Skeleton compiles                                 | all `__init__.py`, utils.typing              | just `pytest -q` smoke test         |
| **1** | Paragraph & Heading blocks                        | `rich_text.py`, `paragraph.py`, `heading.py` | inline mix fixture, heading fixture |
| **2** | Lists (bulleted/numbered) & nested depth handling | `list_item.py`, expand **ConversionContext** | deep‑nest fixture                   |
| **3** | Code & Quote/Callout blocks                       | `code.py`, `advanced.py` (partial)           | code block language, caption        |
| **4** | Tables & Divider                                  | `table.py`                                   | simple table fixture                |
| **5** | Media (image/audio/video/file/bookmark)           | `media.py`                                   | remote vs. data‑url fixture         |
| **6** | Toggles, Columns, Synced, TOC                     | `advanced.py` (full)                         | toggle inside list fixture          |
| **7** | CLI upload path                                   | `cli.py`, `notion/client.py`                 | record HTTP calls with `pytest‑vcr` |
| **8** | Extension hooks + config overrides                | entry‑point loading, `config.py`             | plugin test package                 |

*Complete each phase before moving forward—small PRs keep the mental load low.*

---

## 3  Coding Rhythm

1. **Write a failing fixture** in `tests/fixtures/` (e.g. `paragraph.md` + expected JSON).
2. Implement the minimal logic to pass that fixture.
3. Run `pytest -q`; commit.
4. Refactor if needed (🐥 → 🐓).

> **Why fixtures?** They double as living documentation; future Notion API changes will surface as diff failures.

---

## 4  Rich‑Text Gotchas

* Inline equations: treat `$...$` **before** other annotations to avoid `$\pi$` appearing inside `**bold**` regex hits.
* Overlapping styles: split into smallest non‑overlapping segments **left → right**.
* Mentions & links: decide on a custom Markdown extension (e.g. `@user` or `<mention:page‑id>`).

---

## 5  Testing Strategy

* **Unit** – each converter’s `to_notion` on controlled token lists.
* **Integration** – end‑to‑end `PageBuilder.convert` against full‑page fixtures.
* **Live smoke** – optional: flag‐guarded test that pushes to a dummy Notion page when `NOTION_TOKEN` env var is set.

---

## 6  Release & Distribution

* Bump version in `pyproject.toml` → `poetry build` → `poetry publish`.
* Git tag using `vX.Y.Z` (semver).
* Draft a GitHub release that links the **CHANGELOG.md** (generate via `towncrier` once repo stabilises).

---

## 7  Future Ideas

* **Round‑trip support** (Notion → Markdown) using reversible AST annotations.
* **Mermaid preview**: detect \`\`\`mermaid blocks and upload rendered SVG via Notion image block.
* **Watch mode**: CLI subcommand that watches a Markdown file for changes and syncs automatically.

---

*Happy building!*

