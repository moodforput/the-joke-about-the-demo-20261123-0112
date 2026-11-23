"""Tests for main.py: the joke entry for the-joke-about-the-demo-20261123-0112."""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import JOKE, output_dir


class TestJoke(unittest.TestCase):
    def test_length_1_to_280_code_points(self):
        self.assertGreaterEqual(len(JOKE), 1)
        self.assertLessEqual(len(JOKE), 280)

    def test_not_only_whitespace(self):
        self.assertTrue(JOKE.strip())

    def test_single_line(self):
        self.assertNotIn("\n", JOKE)
        self.assertNotIn("\r", JOKE)

    def test_on_subject_crash_and_agent(self):
        lowered = JOKE.lower()
        self.assertIn("crash", lowered)
        self.assertIn("agent", lowered)

    def test_ascii_only(self):
        JOKE.encode("ascii")

    def test_short_for_tie_break(self):
        self.assertLess(len(JOKE), 120)

    def test_no_trailing_newline(self):
        # entry.txt must hold exactly the joke bytes, no trailing newline.
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
            result = subprocess.run([sys.executable, main_path], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(os.path.join(tmp, "entry.txt"), "rb") as f:
                raw = f.read()
            self.assertEqual(raw, JOKE.encode("utf-8"))
            self.assertFalse(raw.endswith(b"\n"))


class TestMain(unittest.TestCase):
    def test_writes_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            result = subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")],
                env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(os.path.join(tmp, "entry.txt"), encoding="utf-8") as f:
                self.assertEqual(f.read(), JOKE)

    def test_two_runs_byte_identical(self):
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
            for d in (d1, d2):
                env = dict(os.environ, MAKEFUN_OUTPUT_DIR=d)
                result = subprocess.run([sys.executable, main_path], env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            with open(os.path.join(d1, "entry.txt"), "rb") as f:
                b1 = f.read()
            with open(os.path.join(d2, "entry.txt"), "rb") as f:
                b2 = f.read()
            self.assertEqual(b1, b2)
            self.assertEqual(b1, JOKE.encode("utf-8"))

    def test_output_dir_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("MAKEFUN_OUTPUT_DIR")
            os.environ["MAKEFUN_OUTPUT_DIR"] = tmp
            try:
                self.assertEqual(output_dir(), tmp)
            finally:
                if old is None:
                    del os.environ["MAKEFUN_OUTPUT_DIR"]
                else:
                    os.environ["MAKEFUN_OUTPUT_DIR"] = old

    def test_output_dir_default(self):
        old = os.environ.pop("MAKEFUN_OUTPUT_DIR", None)
        try:
            self.assertEqual(output_dir(), "/output")
        finally:
            if old is not None:
                os.environ["MAKEFUN_OUTPUT_DIR"] = old


if __name__ == "__main__":
    unittest.main()
