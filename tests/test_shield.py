import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from shield import redact


class RedactionTests(unittest.TestCase):
    def test_common_formats(self):
        result = redact("a@example.com 12345-1234567-1 0300-1234567 +92 300 1234567 00923001234567")
        self.assertEqual(result.text, "[EMAIL] [CNIC] [PHONE] [PHONE] [PHONE]")
        self.assertEqual(result.counts, {"EMAIL": 1, "CNIC": 1, "PHONE": 3})

    def test_unicode(self):
        self.assertEqual(redact("شناخت ۱۲۳۴۵-۱۲۳۴۵۶۷-۱ نام فرضی", ["نام فرضی"]).text, "شناخت [CNIC] [CUSTOM]")

    def test_custom_is_literal(self):
        self.assertEqual(redact("A+B aab", ["a+b"]).text, "[CUSTOM] aab")

    def test_overlapping_matches_mask_whole_union(self):
        self.assertEqual(redact("a@example.com", ["a@example"]).text, "[CUSTOM]")
        self.assertEqual(redact("abcdef", ["abcd", "cdef"]).text, "[CUSTOM]")

    def test_boundaries(self):
        text = "X03001234567Y 99123451234567199 ordinary\ntext"
        self.assertEqual(redact(text).text, text)

    def test_empty_and_repeated(self):
        self.assertEqual(redact("").text, "")
        self.assertEqual(redact("x@y.com x@y.com").counts, {"EMAIL": 2})

    def test_cli_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / "in.txt", Path(folder) / "out.txt"
            src.write_text("a@example.com", encoding="utf-8")
            dst.write_text("KEEP", encoding="utf-8")
            run = subprocess.run([sys.executable, "shield.py", str(src), str(dst)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertEqual(dst.read_text(), "KEEP")
            self.assertEqual(src.read_text(), "a@example.com")

    def test_cli_output(self):
        with tempfile.TemporaryDirectory() as folder:
            src, dst = Path(folder) / "in.txt", Path(folder) / "out.txt"
            src.write_text("Contact a@example.com", encoding="utf-8")
            subprocess.run([sys.executable, "shield.py", str(src), str(dst)], check=True, capture_output=True)
            self.assertEqual(dst.read_text(), "Contact [EMAIL]")


if __name__ == "__main__":
    unittest.main()
