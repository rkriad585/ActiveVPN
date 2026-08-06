# Deployment

Running ActiveVPN on servers and in containers.

## In this guide

- [Install on a server](#install-on-a-server)
- [Continuous monitoring](#continuous-monitoring)
- [Docker](#docker)
- [Notes and caveats](#notes-and-caveats)

## Install on a server

```bash
pip install activevpn
```

Use the exit codes for automation:

```bash
if activevpn --export json > /dev/null 2>&1; then
  echo "exit 0: clean"
fi
```

## Continuous monitoring

Run in watch mode, optionally in the background:

```bash
# As a background job
nohup activevpn --watch 300 > /var/log/activevpn.log 2>&1 &

# As a systemd unit (Linux), e.g. /etc/systemd/system/activevpn.service
[Unit]
Description=ActiveVPN network monitor
After=network-online.target

[Service]
ExecStart=/usr/local/bin/activevpn --watch 300
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Docker

A multi-stage `Dockerfile` is provided. Build and run:

```bash
docker build -t activevpn .
docker run --rm activevpn
```

The image runs the `activevpn` entrypoint as a non-root user (`uid 10001`) with a default command of `--watch 300`. It includes a `HEALTHCHECK` that verifies the CLI starts.

## Notes and caveats

- **`--kill` needs privileges.** In Docker (and many servers) the container runs as a non-root user, so killing host VPN processes is not possible from inside the container. `--kill` is intended for the host shell.
- **Network access.** The IP/DNS checks need outbound internet. Air-gapped hosts will return exit code `2`.
- **History is local.** Scan history lives in the platform data directory (e.g. `~/.local/share/neostore/ActiveVPN/`); mount a volume there if you want to persist it.

---

<a href="../README.md">← Back to README</a>
