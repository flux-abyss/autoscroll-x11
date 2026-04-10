## Low-latency, motion-activated autoscroll for X11.

Hold the middle mouse button and move the pointer to scroll. Moving above the
click point scrolls up; below scrolls down, with speed proportional to distance.
Horizontal and diagonal scrolling are supported. Releasing the button stops
scrolling.

Normal middle-click behavior is fully preserved. A quick press and release is
forwarded as a standard middle click, including Primary Selection paste (middle-click
paste from the X11 primary buffer).

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
## License

GPL-3.0-or-later

```
