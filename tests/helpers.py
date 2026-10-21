import os
import sys
import shutil
import tempfile
import subprocess
from contextlib import contextmanager

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANAGE_STORY_PY = os.path.join(REPO_ROOT, "manage_story.py")


@contextmanager
def isolated_workspace():
    """
    Creates an isolated temporary directory for testing CLI operations.
    Sets cwd to the temp directory and yields (temp_dir, run_cli_function).
    Automatically cleans up on exit without touching real repo stories/.
    """
    prev_cwd = os.getcwd()
    temp_dir = tempfile.mkdtemp(prefix="svb_test_ws_")
    try:
        os.chdir(temp_dir)

        def run_cli(*args):
            cmd = [sys.executable, MANAGE_STORY_PY] + list(args)
            res = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            return res

        yield temp_dir, run_cli
    finally:
        os.chdir(prev_cwd)
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass
