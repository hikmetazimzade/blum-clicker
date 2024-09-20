from pathlib import Path
import sys
import os

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(os.path.dirname(sys.executable)).resolve()
else:
    ROOT_DIR = Path(__file__).resolve().parent