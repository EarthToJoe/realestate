# Deploy notes (VPS)

- **Session:** `systemctl status claude-remote@realestate`; terminal: `tmux -L rc-realestate attach` (detach with
  Ctrl-b d). Restart: `systemctl restart claude-remote@realestate`.
- **API billing switch (this session only):** `scripts/secret-set.sh ANTHROPIC_API_KEY` writes
  `/srv/realestate/secrets/claude-code.env` and a drop-in at
  `/etc/systemd/system/claude-remote@realestate.service.d/billing.conf`. `--remove` undoes both. No other
  session or shell sees the key.
- **Disk:** `scripts/disk-check.sh` (exit 1 = warn under 6 GB, 2 = stop under 3 GB).
- **Template unit:** `claude-remote@.service` here is only installed if the VPS does not already have the one
  the other projects use; the setup script prints the installed template's WorkingDirectory to confirm it
  maps `%i` to `/root/projects/%i`.
