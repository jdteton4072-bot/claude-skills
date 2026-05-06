#!/usr/bin/env python3
"""Search YouTube and return structured results using yt-dlp."""

import argparse
import json
import subprocess
import sys


def ensure_ytdlp():
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "yt-dlp"])


def search_youtube(query: str, max_results: int = 10, sort_by: str = "relevance") -> list[dict]:
    ensure_ytdlp()
    import yt_dlp

    search_query = f"ytsearch{max_results}:{query}"

    # yt-dlp doesn't natively sort by upload date in search, but we can post-sort
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)

    entries = info.get("entries", [])

    results = []
    for entry in entries:
        if not entry:
            continue
        results.append({
            "title": entry.get("title", "Unknown"),
            "url": f"https://www.youtube.com/watch?v={entry.get('id', '')}",
            "channel": entry.get("channel") or entry.get("uploader", "Unknown"),
            "duration_seconds": entry.get("duration"),
            "duration": _format_duration(entry.get("duration")),
            "view_count": entry.get("view_count"),
            "upload_date": entry.get("upload_date"),
            "description": (entry.get("description") or "")[:200],
        })

    if sort_by == "date" and results:
        results.sort(key=lambda x: x.get("upload_date") or "", reverse=True)
    elif sort_by == "views" and results:
        results.sort(key=lambda x: x.get("view_count") or 0, reverse=True)

    return results


def _format_duration(seconds) -> str:
    if not seconds:
        return "Unknown"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Search YouTube videos")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-n", "--max-results", type=int, default=10,
                        help="Maximum number of results (default: 10)")
    parser.add_argument("--sort", choices=["relevance", "date", "views"],
                        default="relevance", help="Sort order (default: relevance)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    results = search_youtube(args.query, args.max_results, args.sort)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No results found.")
        return

    print(f"\nSearch results for: \"{args.query}\"\n")
    print(f"{'#':<3} {'Title':<55} {'Channel':<25} {'Duration':<10} {'Views'}")
    print("-" * 110)
    for i, r in enumerate(results, 1):
        title = r["title"][:54]
        channel = r["channel"][:24]
        views = f"{r['view_count']:,}" if r["view_count"] else "N/A"
        print(f"{i:<3} {title:<55} {channel:<25} {r['duration']:<10} {views}")
        print(f"    {r['url']}")
        if r["description"]:
            print(f"    {r['description'][:100]}...")
        print()


if __name__ == "__main__":
    main()
