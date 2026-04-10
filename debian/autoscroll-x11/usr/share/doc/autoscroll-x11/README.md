# autoscroll-x11

Middle-click autoscroll for X11.

Hold the middle mouse button and move the pointer to scroll. Moving above the
click point scrolls up; below scrolls down. Speed is proportional to distance
from the click point. Releasing the button stops scrolling. A quick press and
release without movement is forwarded as a normal middle click.

A tray icon provides an enabled/disabled toggle and quit action.

## Requirements

- X11 display server
- Python 3.9+
- python3-gi (GTK 3)
- python3-xlib
- gir1.2-gtk-3.0

## Quick start (no install)

```sh
bash scripts/run-dev.sh --tray
```

## Local user install

```sh
bash scripts/install-local.sh
autoscroll-x11 --tray &
```

## Debian package install

```sh
bash scripts/build-deb.sh
sudo dpkg -i ../autoscroll-x11_*.deb
```

See [docs/PACKAGING.md](docs/PACKAGING.md) for the full packaging reference.

## Development

Run tests:

```sh
python3 -m pytest tests/ -q
```

Run linter:

```sh
bash scripts/lint.sh
```
