import sys
import os
from cx_Freeze import setup, Executable

# Configuration pour Streamlit
build_exe_options = {
    "packages": ["streamlit", "pandas", "numpy", "plotly", "json", "random", "time", "base64", "os", "pathlib", "socket"],
    "includes": ["streamlit.web.bootstrap", "streamlit.runtime.scriptrunner", "streamlit.runtime.scriptrunner_utils"],
    "include_files": [],
    "excludes": ["tkinter", "test"],
    "optimize": 1
}

# Configuration pour .exe
base = "Console"

setup(
    name="ContradictionsApp",
    version="1.0",
    description="Application Contradictions Coran-Boukhari",
    options={"build_exe": build_exe_options},
    executables=[Executable("contradictions_app.py", base=base, target_name="ContradictionsApp.exe")]
)