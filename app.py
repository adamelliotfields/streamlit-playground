#!/usr/bin/env python
import subprocess
import sys

try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "0_🏠_Home.py"], check=True)
except KeyboardInterrupt:
    sys.exit(0)
except subprocess.CalledProcessError as e:
    sys.exit(e.returncode)
