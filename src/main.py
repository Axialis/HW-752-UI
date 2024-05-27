import asyncio
import sys

import qasync
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from src.core.process import ProcessHandler
import src.resources_rc

def main():
    loader = QUiLoader()
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setWindowIcon(QIcon(":/images/ico.png"))
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    ui_file_name = ":/view/main_window.ui"
    ui_file = QFile(ui_file_name)

    window = loader.load(ui_file)
    window.setWindowTitle("HW-752-UI")

    ui_file.close()

    process = ProcessHandler(window)

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.show()

    with loop:
        loop.run_forever()

main()
