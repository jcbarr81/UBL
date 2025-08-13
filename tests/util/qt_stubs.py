"""Minimal PyQt6 stubs for headless testing."""

import sys
import types

class QDialog:
    def __init__(self, *args, **kwargs):
        pass

    def show(self):
        pass

    def close(self):
        pass

    def setWindowTitle(self, title):  # pragma: no cover - simple stub
        self._title = title

    def windowTitle(self):  # pragma: no cover
        return getattr(self, "_title", "")

class QLabel:
    def __init__(self, text=""):
        self._text = text
    def text(self):
        return self._text

class QVBoxLayout:
    def __init__(self, parent=None):
        self.widgets = []
    def addWidget(self, widget):
        self.widgets.append(widget)

class QTableWidget:
    def __init__(self, rows=0, columns=0):
        self._rows = rows
        self._cols = columns
        self._items = {}
    def setColumnCount(self, n):
        self._cols = n
    def setRowCount(self, n):
        self._rows = n
    def setHorizontalHeaderLabels(self, labels):
        self._headers = labels
    def setItem(self, row, col, item):
        self._items[(row, col)] = item
    def item(self, row, col):
        return self._items.get((row, col))
    def resizeColumnsToContents(self):
        pass

class QTableWidgetItem:
    def __init__(self, text=""):
        self._text = text
    def text(self):
        return self._text

qtwidgets = types.ModuleType("PyQt6.QtWidgets")
qtwidgets.QDialog = QDialog
qtwidgets.QLabel = QLabel
qtwidgets.QVBoxLayout = QVBoxLayout
qtwidgets.QTableWidget = QTableWidget
qtwidgets.QTableWidgetItem = QTableWidgetItem

sys.modules.setdefault("PyQt6", types.ModuleType("PyQt6"))
sys.modules["PyQt6.QtWidgets"] = qtwidgets
sys.modules.setdefault("PyQt6.QtCore", types.ModuleType("PyQt6.QtCore"))
sys.modules.setdefault("PyQt6.QtGui", types.ModuleType("PyQt6.QtGui"))
