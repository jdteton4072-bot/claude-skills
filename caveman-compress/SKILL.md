---
name: caveman-compress
description: Compresses natural-language files (markdown, text) into condensed caveman-speak to reduce token usage while preserving all technical content. This skill should be used when a user invokes /caveman-compress, asks to compress a memory file, shrink CLAUDE.md, or reduce a markdown file's token footprint.
---

# Caveman Compress

Compress `.md`, `.txt`, `.typ`, `.typst`, `.tex`, and extensionless files into terse caveman-speak. Reduce tokens ~65-75%. Never touch code.

## Trigger

```
/caveman-compress <filepath>
```

Or: "compress my CLAUDE.md", "shrink this memory file", "reduce tokens in README".

## What to Compress (Remove)

- Articles: "the", "a", "an"
- Hedging: "it is important to", "please note that", "you should consider"
- Filler transitions: "in order to", "as mentioned above", "at this point in time"
- Passive voice → active voice
- Redundant qualifiers: "very", "quite", "basically", "essentially"
- Verbose phrasing → fragments: "Make sure to run tests" → "Run tests"

## What to Preserve Exactly (Never Touch)

- All code blocks (` ``` ` and inline `` ` ``)
- URLs and file paths
- Shell commands and CLI flags
- Technical terms, proper nouns, library/tool names
- Version numbers and numeric values
- Markdown structure: headers, lists, tables, bold/italic emphasis
- All YAML frontmatter

## Process

1. Read the target file
2. Save backup as `<filename>.original.<ext>` in same directory
3. Compress natural-language sections following rules above
4. Write compressed version to original path
5. Report: original token estimate → compressed token estimate → % reduction

## Scope Limits

- Only process: `.md`, `.txt`, `.typ`, `.typst`, `.tex`, extensionless files
- Never process: `.py`, `.js`, `.ts`, `.go`, `.rs`, `.json`, `.yaml`, or any source code
- Mixed files (code + prose): compress only prose sections; skip code blocks entirely

## Compression Examples

**Before**: "In order to ensure that your tests pass before pushing, it is important that you run the full test suite."

**After**: "Run full test suite before push."

---

**Before**: "The authentication module is responsible for handling user login and token refresh operations."

**After**: "Auth: handles login + token refresh."

## Output

After compressing, report:
```
Compressed: path/to/file.md
Backup:     path/to/file.original.md
Before:     ~1240 tokens
After:      ~380 tokens
Saved:      ~69%
```
