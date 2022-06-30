@echo off
.\venv\Scripts\python.exe -m pip install -U python-suanpan-slim -i https://pypi.org/simple
.\venv\Scripts\python.exe -m pip install -U pyinstaller -i https://pypi.mirrors.ustc.edu.cn/simple
.\venv\Scripts\pyinstaller.exe --additional-hooks-dir hooks --clean -D run.py -n video-editor