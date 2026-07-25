---
name: remote-control
description: Controls a local or remote computer using screenshots and keyboard/mouse automation. This skill should be used when a user asks Claude to operate a GUI application, click buttons, fill forms, navigate a browser, automate desktop workflows, or otherwise interact with a screen-based interface as if Claude were sitting at the keyboard.
---

# Remote Control

Enable Claude to observe and interact with a computer's graphical interface using screenshot capture and keyboard/mouse automation tools.

## Overview

To control a computer, follow an **observe → plan → act → verify** loop:

1. **Observe** – Take a screenshot to see the current screen state
2. **Plan** – Identify what to click, type, or press based on what's visible
3. **Act** – Execute one or more input actions
4. **Verify** – Take a follow-up screenshot to confirm the result

Repeat until the goal is achieved.

## Tool Availability Decision Tree

```
Need to control the computer?
│
├─ Are Python libraries available?
│   └─ Yes → Use scripts/control.py (preferred)
│
├─ Is xdotool installed? (check: which xdotool)
│   └─ Yes → Use xdotool CLI commands
│
└─ Fallback → Use xdg-open, wmctrl, or xclip for limited control
```

To detect available tools:
```bash
which scrot gnome-screenshot import xdotool wmctrl 2>/dev/null
python3 -c "import pyautogui; print('pyautogui OK')" 2>/dev/null
```

## Taking Screenshots (Observe)

Always take a screenshot before acting so you know the current UI state.

**Using the helper script (recommended):**
```bash
python3 scripts/control.py screenshot --out /tmp/screen.png
```

**Using scrot:**
```bash
scrot /tmp/screen.png                        # full screen
scrot -u /tmp/screen.png                     # active window only
```

**Using gnome-screenshot:**
```bash
gnome-screenshot -f /tmp/screen.png          # full screen
gnome-screenshot -w -f /tmp/screen.png       # active window
```

After capturing, use the Read tool to view the image and analyze the UI state before acting.

## Mouse Actions (Click, Move, Drag)

**Using the helper script:**
```bash
python3 scripts/control.py click --x 640 --y 400              # left click
python3 scripts/control.py click --x 640 --y 400 --btn right  # right click
python3 scripts/control.py double-click --x 640 --y 400
python3 scripts/control.py move --x 640 --y 400               # move without clicking
python3 scripts/control.py drag --x1 100 --y1 200 --x2 400 --y2 200  # drag
python3 scripts/control.py scroll --x 640 --y 400 --dy -3     # scroll up 3 ticks
```

**Using xdotool:**
```bash
xdotool mousemove 640 400
xdotool click 1                              # 1=left, 2=middle, 3=right
xdotool click --repeat 2 --delay 100 1      # double-click
xdotool mousedown 1 && xdotool mousemove 400 200 && xdotool mouseup 1  # drag
```

## Keyboard Actions (Type, Press, Shortcut)

**Using the helper script:**
```bash
python3 scripts/control.py type --text "Hello, World!"     # type a string
python3 scripts/control.py key --keys ctrl+c               # keyboard shortcut
python3 scripts/control.py key --keys Return               # press Enter
python3 scripts/control.py key --keys Tab                  # press Tab
python3 scripts/control.py key --keys "ctrl+alt+t"         # open terminal
```

**Using xdotool:**
```bash
xdotool type --delay 50 "Hello, World!"    # type text (50ms delay between chars)
xdotool key ctrl+c                         # keyboard shortcut
xdotool key Return                         # press Enter
xdotool key super                          # press Super/Windows key
```

**Common key names:**
`Return`, `Escape`, `Tab`, `BackSpace`, `Delete`, `Home`, `End`, `Prior` (PageUp), `Next` (PageDown), `Up`, `Down`, `Left`, `Right`, `F1`–`F12`, `super`, `alt`, `ctrl`, `shift`

## Window Management

```bash
wmctrl -l                                   # list open windows
wmctrl -a "Firefox"                         # focus window by name
wmctrl -r "Firefox" -e 0,100,100,1280,720  # resize/move window
xdotool search --name "Terminal"            # search window by title
xdotool getactivewindow                     # get active window ID
```

## Clipboard Operations

```bash
echo "text to paste" | xclip -selection clipboard   # copy to clipboard
xclip -selection clipboard -o                        # read clipboard
xdotool key ctrl+v                                   # paste
```

## Common Workflows

### Open an Application
```bash
# By keyboard shortcut (most reliable on GNOME/KDE)
python3 scripts/control.py key --keys "ctrl+alt+t"   # open terminal

# Launch directly
DISPLAY=:0 nohup firefox &                 # launch browser in background
xdg-open /path/to/file                     # open file with default app
```

### Fill a Web Form
```bash
# 1. Screenshot to find field positions
python3 scripts/control.py screenshot --out /tmp/form.png
# 2. Click on a field
python3 scripts/control.py click --x 500 --y 300
# 3. Clear existing content and type new value
python3 scripts/control.py key --keys ctrl+a
python3 scripts/control.py type --text "user@example.com"
# 4. Tab to next field
python3 scripts/control.py key --keys Tab
```

### Navigate a Browser
```bash
# Focus address bar, type URL, navigate
python3 scripts/control.py key --keys ctrl+l
python3 scripts/control.py type --text "https://example.com"
python3 scripts/control.py key --keys Return
sleep 2 && python3 scripts/control.py screenshot --out /tmp/page.png
```

### Scroll to Find Content
```bash
python3 scripts/control.py scroll --x 640 --y 400 --dy -5   # scroll down
python3 scripts/control.py screenshot --out /tmp/after_scroll.png
```

## Coordinate Strategy

Screen coordinates are zero-based from the top-left corner (x increases right, y increases down).

To find where to click:
1. Take a full screenshot and read it
2. Visually identify the target element
3. Estimate (x, y) based on the element's position in the image
4. Click, then take a follow-up screenshot to verify

To get screen resolution:
```bash
xrandr | grep '*'
```

## Error Recovery

- **Click missed target**: Screenshot, re-estimate coordinates, retry
- **Text in wrong field**: Press `Ctrl+Z` to undo, click correct field, retype
- **App unresponsive**: Screenshot to assess; use `wmctrl` or `xdotool` to focus/close
- **No DISPLAY**: Prefix commands with `DISPLAY=:0 xdotool ...`

## Resources

- `scripts/control.py` – Unified Python helper wrapping pyautogui and xdotool for screenshot capture and all mouse/keyboard control operations
