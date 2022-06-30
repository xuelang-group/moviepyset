@echo off
python -m venv venv
.\venv\Scripts\python.exe -m pip install -U pip -i https://pypi.mirrors.ustc.edu.cn/simple
.\venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple
.\venv\Scripts\activate.bat