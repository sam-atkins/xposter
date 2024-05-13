import sys
from pathlib import Path

import tomllib
from pydantic import BaseModel


class Config(BaseModel):
    bluesky_handle: str
    bluesky_password: str
    mastodon_data_file: str
    mastodon_host: str
    mastodon_user: str


def load_config() -> Config:
    home_dir = Path.home()
    config_file = home_dir / ".config" / "xposter" / "config.toml"

    if not config_file.exists():
        sys.exit(
            f"❌  Config file not found: {config_file}. Check the docs to setup the configuration."
        )

    with open(config_file, "rb") as f:
        data = tomllib.load(f)

    return Config(
        bluesky_handle=data["bluesky_handle"],
        bluesky_password=data["bluesky_password"],
        mastodon_data_file=data["mastodon_data_file"],
        mastodon_host=data["mastodon_host"],
        mastodon_user=data["mastodon_user"],
    )
