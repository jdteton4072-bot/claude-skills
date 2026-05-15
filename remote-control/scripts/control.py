#!/usr/bin/env python3
"""
Unified computer control helper: screenshot, mouse, and keyboard.

Tries pyautogui first, falls back to xdotool/scrot CLI tools.

Usage:
  python3 control.py screenshot --out /tmp/screen.png
  python3 control.py click --x 640 --y 400 [--btn left|right|middle]
  python3 control.py double-click --x 640 --y 400
  python3 control.py move --x 640 --y 400
  python3 control.py drag --x1 100 --y1 200 --x2 400 --y2 200
  python3 control.py scroll --x 640 --y 400 --dy -3
  python3 control.py type --text "Hello"
  python3 control.py key --keys ctrl+c
"""

import argparse
import subprocess
import sys
import time

try:
    import pyautogui
    pyautogui.FAILSAFE = False
    BACKEND = "pyautogui"
except ImportError:
    BACKEND = "xdotool"


def _run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def cmd_screenshot(args):
    out = args.out
    if BACKEND == "pyautogui":
        pyautogui.screenshot(out)
    else:
        # Try scrot, then gnome-screenshot, then import (ImageMagick)
        for tool, cli in [
            ("scrot", f"scrot {out}"),
            ("gnome-screenshot", f"gnome-screenshot -f {out}"),
            ("import", f"import -window root {out}"),
        ]:
            if subprocess.run(f"which {tool}", shell=True, capture_output=True).returncode == 0:
                _run(cli)
                break
        else:
            print("Error: no screenshot tool found (install scrot or gnome-screenshot)", file=sys.stderr)
            sys.exit(1)
    print(f"Screenshot saved to {out}")


def cmd_click(args):
    btn_map = {"left": 1, "middle": 2, "right": 3}
    btn = args.btn if hasattr(args, "btn") and args.btn else "left"
    if BACKEND == "pyautogui":
        pyautogui.click(args.x, args.y, button=btn)
    else:
        _run(f"xdotool mousemove {args.x} {args.y} click {btn_map.get(btn, 1)}")
    print(f"Clicked ({args.x}, {args.y}) with {btn} button")


def cmd_double_click(args):
    if BACKEND == "pyautogui":
        pyautogui.doubleClick(args.x, args.y)
    else:
        _run(f"xdotool mousemove {args.x} {args.y} click --repeat 2 --delay 100 1")
    print(f"Double-clicked ({args.x}, {args.y})")


def cmd_move(args):
    if BACKEND == "pyautogui":
        pyautogui.moveTo(args.x, args.y)
    else:
        _run(f"xdotool mousemove {args.x} {args.y}")
    print(f"Moved to ({args.x}, {args.y})")


def cmd_drag(args):
    if BACKEND == "pyautogui":
        pyautogui.moveTo(args.x1, args.y1)
        pyautogui.dragTo(args.x2, args.y2, duration=0.5, button="left")
    else:
        _run(
            f"xdotool mousemove {args.x1} {args.y1} mousedown 1 "
            f"mousemove {args.x2} {args.y2} mouseup 1"
        )
    print(f"Dragged ({args.x1},{args.y1}) → ({args.x2},{args.y2})")


def cmd_scroll(args):
    dy = args.dy  # negative = scroll down, positive = scroll up
    if BACKEND == "pyautogui":
        pyautogui.scroll(dy, x=args.x, y=args.y)
    else:
        btn = 4 if dy > 0 else 5  # button 4 = up, 5 = down
        clicks = abs(dy)
        _run(f"xdotool mousemove {args.x} {args.y} click --repeat {clicks} {btn}")
    print(f"Scrolled {'up' if dy > 0 else 'down'} {abs(dy)} ticks at ({args.x}, {args.y})")


def cmd_type(args):
    text = args.text
    if BACKEND == "pyautogui":
        pyautogui.typewrite(text, interval=0.05)
    else:
        # Escape single quotes for shell safety
        escaped = text.replace("'", "'\\''")
        _run(f"xdotool type --delay 50 '{escaped}'")
    print(f"Typed: {text!r}")


def _xdotool_key_name(key_combo):
    """Convert ctrl+alt+t style to xdotool format (same, lowercase)."""
    return key_combo.lower().replace(" ", "")


def cmd_key(args):
    keys = args.keys
    if BACKEND == "pyautogui":
        pyautogui.hotkey(*keys.split("+"))
    else:
        _run(f"xdotool key {_xdotool_key_name(keys)}")
    print(f"Pressed key(s): {keys}")


def main():
    parser = argparse.ArgumentParser(description="Computer control helper")
    sub = parser.add_subparsers(dest="command", required=True)

    # screenshot
    p = sub.add_parser("screenshot", help="Capture a screenshot")
    p.add_argument("--out", required=True, help="Output file path (e.g. /tmp/screen.png)")

    # click
    p = sub.add_parser("click", help="Mouse click at (x, y)")
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--btn", choices=["left", "right", "middle"], default="left")

    # double-click
    p = sub.add_parser("double-click", help="Double-click at (x, y)")
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)

    # move
    p = sub.add_parser("move", help="Move mouse to (x, y) without clicking")
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)

    # drag
    p = sub.add_parser("drag", help="Drag from (x1,y1) to (x2,y2)")
    p.add_argument("--x1", type=int, required=True)
    p.add_argument("--y1", type=int, required=True)
    p.add_argument("--x2", type=int, required=True)
    p.add_argument("--y2", type=int, required=True)

    # scroll
    p = sub.add_parser("scroll", help="Scroll at (x, y). Positive dy = up, negative = down.")
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--dy", type=int, required=True, help="Scroll ticks (positive=up, negative=down)")

    # type
    p = sub.add_parser("type", help="Type a text string")
    p.add_argument("--text", required=True)

    # key
    p = sub.add_parser("key", help="Press a key or keyboard shortcut (e.g. ctrl+c, Return)")
    p.add_argument("--keys", required=True)

    args = parser.parse_args()

    dispatch = {
        "screenshot": cmd_screenshot,
        "click": cmd_click,
        "double-click": cmd_double_click,
        "move": cmd_move,
        "drag": cmd_drag,
        "scroll": cmd_scroll,
        "type": cmd_type,
        "key": cmd_key,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
