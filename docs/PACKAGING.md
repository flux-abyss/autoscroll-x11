# Packaging

## Debian layout

```
/usr/bin/autoscroll-x11
/usr/lib/autoscroll-x11/autoscroll_x11/
/usr/share/applications/autoscroll-x11.desktop
/etc/xdg/autostart/autoscroll-x11.desktop
/usr/share/icons/hicolor/scalable/apps/autoscroll-x11.svg
/usr/share/icons/hicolor/symbolic/apps/autoscroll-x11-symbolic.svg
/usr/share/man/man1/autoscroll-x11.1.gz
```

The launcher at `/usr/bin/autoscroll-x11` prepends `/usr/lib/autoscroll-x11`
to `sys.path` and calls `autoscroll_x11.app.main()`.

There is no `pip install` or `setup.py`. Install is handled entirely by
`debian/rules` using explicit `install` commands.

## Building the package

Install build dependencies:

```sh
sudo apt build-dep .
```

Build and install:

```sh
bash scripts/build-deb.sh
sudo dpkg -i ../autoscroll-x11_*.deb
```

After `dpkg -i` you may see a message about deferred triggers. This is
normal. The triggers (icon cache, desktop database) are processed by the
system in the background. To complete them immediately:

```sh
sudo dpkg --configure -a
```

Do not run `dpkg-trigger` manually. It is not part of the install workflow.

## Rapid local iteration (no root, no .deb)

For fast edit-test cycles during development, install directly under
`~/.local` from the source tree:

```sh
bash scripts/install-local.sh
```

Re-run after any source change. This replaces the previous installed copy
cleanly. No build step is needed. The launcher picks up the updated source
immediately.

To run without installing at all, use:

```sh
bash scripts/run-dev.sh --tray
```

This sets `PYTHONPATH` to the source root and runs directly.

## Why the install may feel slow

When installing via dpkg, the hicolor icon theme trigger runs
`gtk-update-icon-cache` and the desktop file trigger runs
`update-desktop-database`. These are registered by other packages
(hicolor-icon-theme, desktop-file-utils) and run after every package
install that touches those directories.

They are not a bug in this package. They are normal system triggers.
The `scripts/install-local.sh` path avoids them entirely.

## Versioning

Version string is maintained in two places:

- `autoscroll_x11/__init__.py` — `__version__`
- `debian/changelog` — first entry

Keep them in sync when cutting a release.

## Lintian

```sh
lintian --profile debian ../autoscroll-x11_*.deb
```
