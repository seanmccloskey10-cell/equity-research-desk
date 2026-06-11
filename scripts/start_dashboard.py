"""Start the Streamlit dashboard and record its PID.

Usage:
    python scripts/start_dashboard.py

Behavior:
- Checks for an existing .streamlit.pid; if the process is alive, prints
  a message and exits 0 (already running).
- If the PID file is stale, removes it.
- Spawns `streamlit run app.py` as a detached background process on
  Windows / POSIX, writes the PID to .streamlit.pid.
- Prints the local URL so the agent can pass it to the user.
"""

from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PID_FILE = PROJECT_ROOT / ".streamlit.pid"
APP_FILE = PROJECT_ROOT / "app.py"
PORT = 8501
DEFAULT_URL = f"http://localhost:{PORT}"


def _port_in_use(port: int) -> bool:
    """True if something is already listening on localhost:port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _pid_alive(pid: int) -> bool:
    try:
        if os.name == "nt":
            # Windows — use tasklist
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
                check=False,
            )
            return str(pid) in out.stdout
        # POSIX — signal 0 checks existence
        os.kill(pid, 0)
        return True
    except (OSError, subprocess.SubprocessError):
        return False


def main() -> int:
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
        except ValueError:
            pid = -1
        if pid > 0 and _pid_alive(pid):
            print(f"Dashboard already running (PID {pid}). Visit {DEFAULT_URL}.")
            return 0
        print("Found stale PID file — cleaning up.")
        PID_FILE.unlink(missing_ok=True)

    if not APP_FILE.exists():
        print(f"ERROR: {APP_FILE} not found.")
        return 1

    # Port pre-check: if something else holds 8501, Streamlit would silently
    # drift to 8502 while we report 8501 — "started but unreachable". Catch it.
    if _port_in_use(PORT):
        print(f"ERROR: Port {PORT} is already in use, so the dashboard can't start cleanly.")
        print("  It may be an old dashboard that didn't shut down. Try `python run.py stop` first.")
        print("  If that doesn't help, stop whatever is using the port:")
        print(f"    Windows:  netstat -ano | findstr :{PORT}   then  taskkill /PID <pid> /F")
        print(f"    macOS:    lsof -i :{PORT}                   then  kill <pid>")
        return 1

    cmd = [
        sys.executable, "-m", "streamlit", "run", str(APP_FILE),
        "--server.port", str(PORT),
        "--server.headless", "true",
    ]

    if os.name == "nt":
        # Windows — new process group so we can kill cleanly
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
        proc = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_ROOT),
            creationflags=flags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    PID_FILE.write_text(str(proc.pid))
    # Give Streamlit a moment to boot so the URL is actually live.
    time.sleep(2)
    print(f"Dashboard started (PID {proc.pid}). Visit {DEFAULT_URL}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
