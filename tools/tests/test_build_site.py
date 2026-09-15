"""Exercise the public-site build from editable sources in an isolated directory."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class SiteBuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("tools", "content"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))

    def build(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.root / "tools/build_site.py"), *args],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_build_from_sources_preserves_public_routes_and_theme(self):
        self.build()
        self.build("--check")
        self.assertEqual(45, len([p for p in self.root.rglob("*.html")
                                  if "content" not in p.relative_to(self.root).parts]))
        for page in [*self.root.rglob("privacy.html"), *self.root.rglob("terms.html")]:
            text = page.read_text()
            self.assertIn('name="color-scheme" content="dark"', text)
            self.assertIn('<a href="./index.html">SnapMosaic</a>', text)
            self.assertTrue((page.parent / "index.html").is_file())
        self.assertIn('dir="rtl"', (self.root / "ur/privacy.html").read_text())

    def test_changed_legal_source_is_detected_and_regenerated(self):
        self.build()
        source = self.root / "content/legal/zh-CN.json"
        data = json.loads(source.read_text())
        data["privacy"]["intro"] += " 测试更新。"
        source.write_text(json.dumps(data, ensure_ascii=False))
        result = self.build("--check", success=False)
        self.assertIn("OUTDATED zh-CN/privacy.html", result.stdout)
        self.build()
        self.build("--check")
        self.assertIn("测试更新。", (self.root / "zh-CN/privacy.html").read_text())

    def test_shared_effective_date_updates_all_legal_pages(self):
        (self.root / "content/legal.json").write_text('{"effectiveDate": "2026-09-15"}')
        self.build()
        pages = [*self.root.rglob("privacy.html"), *self.root.rglob("terms.html")]
        self.assertEqual(30, len(pages))
        for page in pages:
            self.assertIn('<time datetime="2026-09-15">2026-09-15</time>', page.read_text())
        (self.root / "content/legal.json").write_text('{"effectiveDate": "2026-02-30"}')
        self.build("--check", success=False)

    def test_missing_translation_fails(self):
        (self.root / "content/legal/ur.json").unlink()
        self.build(success=False)


if __name__ == "__main__":
    unittest.main()
