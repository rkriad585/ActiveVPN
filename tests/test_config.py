# ActiveVPN/tests/test_config.py
import json

import pytest

from activevpn.config import (
    Config,
    CONFIG_FILE,
    CONFIG_DIR,
    LOG_FILE,
    load_config,
    load_config_file,
    resolve_config_path,
    save_config,
)


def test_config_defaults():
    cfg = load_config(overrides={})
    assert cfg.vpn_interface_patterns
    assert "openvpn" in cfg.vpn_process_names
    assert cfg.score_interface == 50
    assert cfg.dns_leak_api_url.startswith("https://")


def test_config_from_legacy_uppercase_keys(tmp_path):
    data = {
        "VPN_INTERFACE_PATTERNS": ["tun", "tap"],
        "SCORE_PROXY": 99,
        "COLOR_SUCCESS": "bold cyan",
    }
    cfg = Config.from_dict(data)
    assert cfg.vpn_interface_patterns == ["tun", "tap"]
    assert cfg.score_proxy == 99
    assert cfg.color_success == "bold cyan"
    # untouched defaults survive
    assert "openvpn" in cfg.vpn_process_names


def test_config_roundtrip_save_load(tmp_path):
    cfg = Config(score_tor_process=41, color_danger="bold red")
    path = tmp_path / "config.json"
    save_config(cfg, str(path))

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    assert raw["score_tor_process"] == 41

    loaded = load_config(custom=str(path))
    assert loaded.score_tor_process == 41
    assert loaded.color_danger == "bold red"


def test_load_config_custom_overrides_file(tmp_path):
    cfg_file = tmp_path / "cfg.json"
    cfg_file.write_text(json.dumps({"score_proxy": 77}), encoding="utf-8")
    cfg = load_config(custom=str(cfg_file), overrides={"score_proxy": 88})
    assert cfg.score_proxy == 88


def test_load_config_inline_overrides_win(tmp_path):
    cfg = load_config(overrides={"vpn_process_names": ["myvpn"]})
    assert cfg.vpn_process_names == ["myvpn"]


def test_resolve_config_path_env(monkeypatch, tmp_path):
    cfg_file = tmp_path / "env.json"
    cfg_file.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("ACTIVEVPN_CONFIG", str(cfg_file))
    assert resolve_config_path() == str(cfg_file)


def test_resolve_config_path_explicit_custom(tmp_path):
    cfg_file = tmp_path / "custom.json"
    assert resolve_config_path(str(cfg_file)) is None  # missing file -> None
    cfg_file.write_text("{}", encoding="utf-8")
    assert resolve_config_path(str(cfg_file)) == str(cfg_file)


def test_load_config_file_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{{{ not json", encoding="utf-8")
    assert load_config_file(str(bad)) == {}


def test_paths_use_neostore_namespace():
    assert "neostore" in CONFIG_DIR.replace("\\", "/").lower().replace("_", "")
    assert CONFIG_FILE.endswith("config.json")
    assert LOG_FILE.endswith("scan_history.json")
