# ActiveVPN/tests/test_logger.py
import os

import pytest

import activevpn.logger as logger
from activevpn.detector import IPInfo, ProcessInfo, ScanResult, Verdict

SAMPLE_SCAN = {
    "interfaces": ["tun0"],
    "vpn_processes": [{"pid": 1, "name": "openvpn"}],
    "tor_processes": [],
    "public_ip": {"query": "1.2.3.4", "isp": "Test ISP", "country": "Testland"},
    "dns_leak": {"ip": "8.8.8.8"},
    "ipv4": "1.2.3.4",
    "ipv6": None,
    "verdict": {"score": 90, "label": "VPN DETECTED", "reasons": ["x"]},
}

SAMPLE_SCAN_RESULT = ScanResult(
    interfaces=["tun0"],
    vpn_processes=[ProcessInfo(pid=1, name="openvpn")],
    public_ip=IPInfo(query="1.2.3.4", isp="Test ISP", country="Testland"),
    dns_leak=__import__("activevpn.detector", fromlist=["DNSInfo"]).DNSInfo(ip="8.8.8.8"),
    ipv4="1.2.3.4",
    verdict=Verdict(score=90, label="VPN DETECTED", reasons=["x"]),
)


@pytest.fixture
def tmp_log(tmp_path, monkeypatch):
    monkeypatch.setattr(logger, "LOG_FILE", str(tmp_path / "history.json"))
    return tmp_path / "history.json"


def test_save_and_load_history(tmp_log):
    assert logger.save_log(SAMPLE_SCAN) is True
    assert logger.save_log(SAMPLE_SCAN) is True

    history = logger.load_history()
    assert len(history) == 2
    assert history[0]["scan_results"]["public_ip"]["query"] == "1.2.3.4"
    assert history[0]["timestamp"]


def test_save_scan_result_object(tmp_log):
    assert logger.save_log(SAMPLE_SCAN_RESULT) is True
    history = logger.load_history()
    assert history[0]["scan_results"]["public_ip"]["query"] == "1.2.3.4"
    assert history[0]["scan_results"]["verdict"]["label"] == "VPN DETECTED"


def test_load_missing_history(tmp_log):
    assert logger.load_history() == []


def test_load_corrupt_history(tmp_log):
    tmp_log.write_text("not json{{{", encoding="utf-8")
    assert logger.load_history() == []


def test_clear_history(tmp_log):
    logger.save_log(SAMPLE_SCAN)
    assert logger.clear_history() is True
    assert not os.path.exists(str(tmp_log))
    assert logger.load_history() == []


def test_export_json(tmp_log, tmp_path):
    logger.save_log(SAMPLE_SCAN)
    path = logger.export_history("json", str(tmp_path / "out.json"))
    import json

    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    assert rows[0]["public_ip"] == "1.2.3.4"
    assert rows[0]["verdict"] == "VPN DETECTED"


def test_export_csv(tmp_log, tmp_path):
    logger.save_log(SAMPLE_SCAN)
    path = logger.export_history("csv", str(tmp_path / "out.csv"))
    with open(path, encoding="utf-8") as f:
        content = f.read()
    assert "timestamp,verdict,score" in content
    assert "1.2.3.4" in content


def test_export_txt(tmp_log, tmp_path):
    logger.save_log(SAMPLE_SCAN)
    path = logger.export_history("txt", str(tmp_path / "out.txt"))
    with open(path, encoding="utf-8") as f:
        content = f.read()
    assert "VPN DETECTED" in content
