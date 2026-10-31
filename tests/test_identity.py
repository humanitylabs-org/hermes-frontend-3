"""Identity-only packaging regression checks. Run with unittest + PyYAML."""
import json
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def manifest():
    return yaml.safe_load((ROOT / "wizard.md").read_text().split("---", 2)[1])


class IdentityTests(unittest.TestCase):
    def test_app_id_matches_display_name_and_keeps_migration_source(self):
        doc = manifest()
        self.assertEqual(doc["id"], NEW_ID)
        self.assertEqual(doc["renamed_from"], [OLD_ID])
        self.assertEqual(doc["name"].lower().replace(" ", "-"), NEW_ID)

    def test_packaging_identity_and_version_agree(self):
        doc = manifest()
        cfg = json.loads((ROOT / "runtipi/config.json").read_text())
        self.assertEqual(cfg["id"], doc["id"])
        self.assertEqual(cfg["name"], doc["name"])
        self.assertEqual(cfg["version"], doc["version"])
        self.assertEqual(doc["version"], VERSION)
        compose = yaml.safe_load((ROOT / "runtipi/docker-compose.yml").read_text())
        self.assertIn(NEW_ID, compose["services"])
        self.assertNotIn(OLD_ID, compose["services"])

import subprocess

NEW_ID = "hermes-desktop-in-browser"
OLD_ID = "hermes-frontend-3"
VERSION = "0.1.1+1af684e"


class FrontendCompatibilityTests(unittest.TestCase):
    def test_existing_image_backend_and_port_are_preserved(self):
        cfg = json.loads((ROOT / "runtipi/config.json").read_text())
        compose = yaml.safe_load((ROOT / "runtipi/docker-compose.yml").read_text())
        service = compose["services"][NEW_ID]
        self.assertEqual(service["image"], "ghcr.io/humanitylabs-org/hermes-frontend-3:1af684e-1")
        self.assertEqual(cfg["port"], 9120)
        self.assertEqual(cfg["form_fields"][0]["default"], "http://hermes-agent:9119")
        self.assertEqual(service["environment"]["HERMES_BACKEND_URL"], "${HERMES_BACKEND_URL}")
        self.assertNotIn("volumes", service)
        self.assertIn(OLD_ID, service["networks"]["default"]["aliases"])

    def test_invalid_backend_origins_fail_before_nginx_starts(self):
        import os
        for origin in ("", "https://user:pass@example.org", "http://example.org/path", "http://host;bad"):
            with self.subTest(origin=origin):
                run = subprocess.run(["sh", str(ROOT / "start.sh")],
                    env={**os.environ, "HERMES_BACKEND_URL": origin}, capture_output=True, text=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertRegex(run.stderr, "Invalid backend origin|HERMES_BACKEND_URL must")
