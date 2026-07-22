import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "client"))

from websocket import normalize_server_url
from agent import build_task_command, build_schtasks_create_command


class NormalizeServerUrlTests(unittest.TestCase):
    def test_https_base_url_is_converted_to_wss_websocket_endpoint(self):
        self.assertEqual(
            normalize_server_url("https://screen-production-4c82.up.railway.app"),
            "wss://screen-production-4c82.up.railway.app/ws",
        )

    def test_https_websocket_url_keeps_path_and_switches_scheme(self):
        self.assertEqual(
            normalize_server_url("https://screen-production-4c82.up.railway.app/ws"),
            "wss://screen-production-4c82.up.railway.app/ws",
        )

    def test_http_base_url_is_converted_to_ws_websocket_endpoint(self):
        self.assertEqual(
            normalize_server_url("http://localhost:8000"),
            "ws://localhost:8000/ws",
        )

    def test_existing_ws_url_is_left_unchanged(self):
        self.assertEqual(
            normalize_server_url("ws://localhost:8000/ws"),
            "ws://localhost:8000/ws",
        )

    def test_task_command_quotes_executable_with_spaces(self):
        self.assertIn('"C:/Program Files/Monitoring Agent/MonitoringAgent.exe"', build_task_command(
            r"C:\Program Files\Monitoring Agent\MonitoringAgent.exe",
            ["--server", "https://example.test"]
        ))

    def test_schtasks_command_uses_logon_trigger_and_highest_privilege(self):
        command = build_schtasks_create_command(
            task_name="MonitoringAgentRestart",
            command=r"C:\Program Files\Monitoring Agent\MonitoringAgent.exe",
        )
        self.assertTrue(any(token == "/SC" for token in command))
        self.assertIn("ONLOGON", command)
        self.assertIn("/RL", command)


if __name__ == "__main__":
    unittest.main()
