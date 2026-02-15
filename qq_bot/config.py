"""Configuration loading for the QQ bot."""

import os

import yaml


def load_config(path="config.yaml"):
    """Load bot configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        A dict with the parsed configuration.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If required keys are missing.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Config file not found: {path}. "
            "Copy config.yaml.example to config.yaml and fill in your credentials."
        )

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config or "bot" not in config:
        raise ValueError("Config must contain a 'bot' section.")

    bot_cfg = config["bot"]
    for key in ("appid", "secret"):
        if key not in bot_cfg or not bot_cfg[key]:
            raise ValueError(f"Missing required config key: bot.{key}")

    return config
