---
name: youtube-search
description: Search YouTube for videos and return structured results with titles, URLs, channels, durations, and view counts. Use this skill when the user wants to find YouTube videos, search for tutorials, look up content creators, or research a topic on YouTube. No API key required.
---

# YouTube Search

Search YouTube and get structured results — titles, URLs, channels, durations, view counts — without needing a YouTube API key.

## Quick Start

```bash
python scripts/search_youtube.py "your search query"
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-n`, `--max-results` | `10` | Number of results to return (1–50) |
| `--sort` | `relevance` | Sort by: `relevance`, `date`, or `views` |
| `--json` | off | Output raw JSON instead of formatted table |

## Examples

### Basic search
```bash
python scripts/search_youtube.py "python async tutorial"
```

### Get more results
```bash
python scripts/search_youtube.py "machine learning" -n 20
```

### Sort by newest
```bash
python scripts/search_youtube.py "anthropic claude" --sort date
```

### Sort by most viewed
```bash
python scripts/search_youtube.py "react hooks" --sort views -n 5
```

### JSON output (for piping or further processing)
```bash
python scripts/search_youtube.py "docker kubernetes" --json
```

## Output Format

Each result includes:
- **Title** — video title
- **URL** — direct YouTube link (`https://www.youtube.com/watch?v=...`)
- **Channel** — uploader/channel name
- **Duration** — formatted as `M:SS` or `H:MM:SS`
- **View count** — total views
- **Description** — first 200 characters of description
- **Upload date** — `YYYYMMDD` format (available in JSON output)

## How It Works

Uses `yt-dlp`'s `ytsearch` prefix to query YouTube's search directly — the same approach as searching in your browser, no API key or authentication required. `yt-dlp` is installed automatically if not present.

## Prerequisites

Python 3.8+. `yt-dlp` is auto-installed on first run.

To install manually:
```bash
pip install yt-dlp
```

## Troubleshooting

- **No results** → Try a broader query or fewer words
- **Rate limited** → Wait a few minutes; YouTube throttles rapid searches
- **Slow first run** → `yt-dlp` is being installed; subsequent runs are fast

## Notes for Claude

When the user asks to search YouTube:
1. Run `python scripts/search_youtube.py "<query>"` with their search terms
2. Present results clearly with titles and URLs
3. If they want to download a result, hand off to the `youtube-downloader` skill
4. For playlist or channel searches, append "playlist" or "channel" to the query
