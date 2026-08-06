# Accessibility

ActiveVPN is a terminal tool, so accessibility focuses on output that works
across terminals, screen readers, and low-vision setups.

## What we do

- **Color is never the only signal.** The overall verdict is always printed as
  a text label (`CLEAN`, `SUSPICIOUS`, `LIKELY VPN/PROXY`, `VPN DETECTED`) plus
  a numeric confidence score, not just a color.
- **ASCII-safe rendering.** The confidence bar uses `#` and `-` characters, so
  it renders correctly on legacy consoles and screen readers.
- **Keyboard only.** The tool is fully operable from the command line; no
  mouse, pointer, or GUI interaction is required.
- **No reliance on system sound or notifications.**
- **Plain-text output.** `activevpn --export txt` and `--history` produce
  plain text that reflows cleanly and can be fed to other tools.
- **Configurable colors.** All UI colors are constants in `config.py` and can
  be overridden to improve contrast for individual needs. See
  [docs/configuration.md](docs/configuration.md).

## Terminal guidance

- Prefer a modern terminal (Windows Terminal, iTerm2, GNOME Terminal, etc.)
  for the best rendering.
- On legacy Windows consoles, run `chcp 65001` if symbols appear garbled.
- The default palette uses high-contrast colors on a dark background.

## Reporting issues

If something is hard to read or use, open an issue and mention the terminal,
OS, and color settings you are using.

---

<a href="README.md">← Back to README</a>
