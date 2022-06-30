import pathlib
from PyInstaller.utils.hooks import collect_all, collect_system_data_files
from PyInstaller.utils.hooks import logger

datas, binaries, hiddenimports = collect_all('components', include_py_files=False)

logger.info('Collecting suanpan components datas: {}'.format(datas))
logger.info('Collecting suanpan components hiddenimports: {}'.format(hiddenimports))