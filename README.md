# xposter

A cross poster from Mastodon to Bluesky.

## Install

Via the Taskfile using [uv](https://github.com/astral-sh/uv)

```bash
task install
```

### Configuration

Config is stored in `~/.config/xposter`.

If this directory does not exist then create it

```bash
mkdir -p ~/.config/xposter
```

Create the two files you need:

```bash
touch ~/.config/xposter/mstd.json
```

```bash
echo 'bluesky_handle="your_bluesky_handle"
bluesky_password="your_bluesky_password"
mastodon_data_file="/Users/<username>/.config/xposter/mstd.json"
mastodon_host="your_mastodon_host"
mastodon_user="your_mastodon_user"' > ~/.config/xposter/config.toml
```

With this, you should be ready to run the script.

## Usage

To run the script, use the task

```bash
task run
```

## Cron

Here's how to setup a cronjob on a Mac. Run this to open the cron editor:

```
crontab -e
```

Then add a cron job e.g. this one runs every 5th minute. Change the {vars} to your own setup and the path to `task` if not installed using homebrew.

```
*/5 * * * * cd /Users/{userName}/{parentDir}/xposter && /opt/homebrew/bin/task run
```

## Useful Documentation

Bluesky Python SDK: https://atproto.blue/en/latest/

Helpful Cron reminder: https://crontab.guru/
