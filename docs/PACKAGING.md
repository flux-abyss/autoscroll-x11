# Packaging

## Debian Layout

```
/usr/bin/autoscroll-x11            ← launcher (debian/bin/autoscroll-x11)
/usr/lib/autoscroll-x11/           ← Python package root
    autoscroll_x11/
        __init__.py
        app.py
        ...
/usr/share/applications/autoscroll-x11.desktop
/etc/xdg/autostart/autoscroll-x11.desktop
/usr/share/icons/hicolor/scalable/apps/autoscroll-x11.svg
/usr/share/icons/hicolor/symbolic/apps/autoscroll-x11-symbolic.svg
/usr/share/man/man1/autoscroll-x11.1.gz
```

The launcher at `/usr/bin/autoscroll-x11` prepends
`/usr/lib/autoscroll-x11` to `sys.path` and calls `autoscroll_x11.app.main()`.
There is no `pip install` or `setup.py`; the install is handled entirely by
`debian/rules` using explicit `install` commands.

## Build

Install build dependencies:

```sh
sudo apt build-dep .
# or manually:
sudo apt install debhelper dh-python python3-all
```

Build the package:

```sh
dpkg-buildpackage -us -uc -b
```

The resulting `.deb` appears in the parent directory.

## Lintian

```sh
lintian --profile debian ../autoscroll-x11_*.deb
```

## Versioning

Version string is maintained in two places:

- `autoscroll_x11/__init__.py` — `__version__`
- `debian/changelog` — first entry

Keep them in sync when cutting a release.
