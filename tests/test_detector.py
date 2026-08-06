# ActiveVPN/tests/test_detector.py
from unittest.mock import MagicMock, patch

import pytest

from activevpn.detector import NetworkDetector, ProcessInfo, ScanResult, scan


@pytest.fixture
def detector():
    console = MagicMock()
    return NetworkDetector(console)


# --- Process matching ---

@pytest.mark.parametrize(
    "target,name,cmdline,expected",
    [
        ("openvpn", "openvpn.exe", [], True),
        ("openvpn", "OpenVPN", [], True),
        ("openvpn", "openvpn-gui.exe", [], True),
        ("openvpn", "myapp.exe", ["/usr/bin/openvpn"], True),
        ("openvpn", "notepad.exe", [], False),
        ("vpn", "myapp.exe", [], False),
        ("vpn", "vpn", [], True),
        ("vpn", "somevpnprocessthing.exe", [], False),
        ("cisco anyconnect", "cscui.exe", ["/opt/cisco/anyconnect/bin/vpn"], True),
        ("cisco anyconnect", "cscui.exe", ["/bin/cscui"], False),
        ("nordvpn", "nordvpn.exe", [], True),
        ("tor", "tor.exe", [], True),
    ],
)
def test_process_matches(detector, target, name, cmdline, expected):
    assert detector._process_matches(target, name, cmdline) is expected


def test_check_processes_matches_names(detector):
    proc = MagicMock()
    proc.info = {"pid": 123, "name": "openvpn.exe", "cmdline": []}
    with patch("psutil.process_iter", return_value=[proc]):
        found = detector.check_processes(["openvpn"])
    assert found == [ProcessInfo(pid=123, name="openvpn.exe")]


def test_check_processes_no_false_positive(detector):
    proc = MagicMock()
    proc.info = {"pid": 123, "name": "python.exe", "cmdline": ["python", "app.py"]}
    with patch("psutil.process_iter", return_value=[proc]):
        found = detector.check_processes(["vpn"])
    assert found == []


# --- Verdict scoring ---

def _scan(**kwargs) -> ScanResult:
    defaults = dict(interfaces=[], vpn_processes=[], tor_processes=[], public_ip=None)
    defaults.update(kwargs)
    return ScanResult(**defaults)


def test_verdict_clean(detector):
    result = _scan()
    verdict = detector._compute_verdict(result)
    assert verdict.label == "CLEAN"
    assert verdict.score == 0


def test_verdict_interface_detected(detector):
    result = _scan(interfaces=["tun0"])
    verdict = detector._compute_verdict(result)
    assert verdict.score == 50
    assert verdict.label == "LIKELY VPN/PROXY"


def test_verdict_hosting_and_proxy(detector):
    from activevpn.detector import IPInfo

    result = _scan(public_ip=IPInfo(hosting=True, proxy=True))
    verdict = detector._compute_verdict(result)
    assert verdict.score == 55
    assert verdict.label == "LIKELY VPN/PROXY"


def test_verdict_full_vpn(detector):
    from activevpn.detector import IPInfo

    result = _scan(
        interfaces=["tun0"],
        vpn_processes=[ProcessInfo(pid=1, name="openvpn")],
        public_ip=IPInfo(hosting=True),
    )
    verdict = detector._compute_verdict(result)
    assert verdict.score >= 100
    assert verdict.label == "VPN DETECTED"


# --- API calls ---

def test_get_public_ip_info_success(detector):
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"query": "1.2.3.4", "isp": "Test ISP"}
    with patch("requests.get", return_value=response):
        info = detector.get_public_ip_info()
    assert info.query == "1.2.3.4"
    assert info.address == "1.2.3.4"
    assert info.source.startswith("http")


def test_get_public_ip_info_fallback(detector):
    bad = MagicMock()
    bad.status_code = 500
    good = MagicMock()
    good.status_code = 200
    good.json.return_value = {"query": "5.6.7.8", "isp": "Fallback ISP"}

    calls = {"count": 0}

    def fake_get(url, timeout):
        calls["count"] += 1
        return bad if calls["count"] == 1 else good

    with patch("requests.get", side_effect=fake_get):
        info = detector.get_public_ip_info()
    assert info.query == "5.6.7.8"
    assert calls["count"] == 2


def test_get_public_ip_info_offline(detector):
    with patch("requests.get", side_effect=__import__("requests").RequestException("down")):
        assert detector.get_public_ip_info() is None


def test_get_ipv6_none(detector):
    with patch("requests.get", side_effect=__import__("requests").RequestException("no v6")):
        assert detector.get_ipv6() is None


# --- Library API ---

def test_scan_module_function(monkeypatch):
    monkeypatch.setattr(NetworkDetector, "scan_network", lambda self: ScanResult())
    result = scan(console=None)
    assert isinstance(result, ScanResult)


def test_scan_result_serialization():
    result = ScanResult(
        interfaces=["tun0"],
        vpn_processes=[ProcessInfo(pid=7, name="openvpn")],
        verdict=NetworkDetector(None)._compute_verdict(_scan(interfaces=["tun0"])),
    )
    data = result.to_dict()
    assert data["interfaces"] == ["tun0"]
    assert data["vpn_processes"] == [{"pid": 7, "name": "openvpn"}]
    assert data["verdict"]["label"] == "LIKELY VPN/PROXY"

    import json

    parsed = json.loads(result.to_json())
    assert parsed["interfaces"] == ["tun0"]


def test_detector_silent_mode():
    det = NetworkDetector(console=None)
    assert det.console is None
