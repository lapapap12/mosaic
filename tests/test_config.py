"""Tests for the configuration loader."""

import os
import tempfile

import pytest
import yaml

from qq_bot.config import load_config


def _write_config(path, data):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f)


def test_load_config_valid():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        yaml.dump({"bot": {"appid": "123", "secret": "abc"}}, f)
        f.flush()
        config = load_config(f.name)
    os.unlink(f.name)
    assert config["bot"]["appid"] == "123"
    assert config["bot"]["secret"] == "abc"


def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")


def test_load_config_missing_bot_section():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        yaml.dump({"other": "value"}, f)
        f.flush()
    with pytest.raises(ValueError, match="'bot' section"):
        load_config(f.name)
    os.unlink(f.name)


def test_load_config_missing_appid():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        yaml.dump({"bot": {"secret": "abc"}}, f)
        f.flush()
    with pytest.raises(ValueError, match="bot.appid"):
        load_config(f.name)
    os.unlink(f.name)


def test_load_config_missing_secret():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as f:
        yaml.dump({"bot": {"appid": "123"}}, f)
        f.flush()
    with pytest.raises(ValueError, match="bot.secret"):
        load_config(f.name)
    os.unlink(f.name)
