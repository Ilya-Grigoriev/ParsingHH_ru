import os.path
import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from get_advanced_data import get_vacancies


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.search.clicked.connect(self.start_process)
        self.app = app

    def start_process(self) -> None:
        self.search.setEnabled(False)
        if not self.income.text().isdigit():
            self.statusBar().showMessage(
                'Уровень дохода должен быть в виде числа')
            self.search.setEnabled(True)
        elif not os.path.isdir(self.path.text()):
            self.statusBar().showMessage(
                'Неверный путь для сохранения результата')
            self.search.setEnabled(True)
        else:
            self.statusBar().showMessage('')
            busyness = [button.text() for button in self.busy.buttons() if
                        button.isChecked()]

            graph = [button.text() for button in self.graph.buttons() if
                     button.isChecked()]

            sort = [button.text() for button in self.sort.buttons() if
                    button.isChecked()]

            output = [button.text() for button in self.output.buttons() if
                      button.isChecked()]
            self.close()
            get_vacancies(self.keywords.text(), int(self.count_pars.text()),
                          str(self.specialization.currentText()),
                          str(self.branch.currentText()),
                          self.region.text(), self.income.text(),
                          str(self.currency.currentText()),
                          str(self.experience.currentText()), busyness,
                          graph, sort, output, self.path.text())


QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)


def main_for_project() -> None:
    widget = Interface()
    widget.resize(500, 400)
    widget.show()
    sys.excepthook = except_hook
    app.exec()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    sys.exit(app.exec())


if __name__ == '__main__':
    main_for_project()
