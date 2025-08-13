import os
import sys
import types
import pytest

# Ensure tests run in environments without a display server
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:  # pragma: no cover - real PyQt6 if available
    from PyQt6.QtWidgets import (
        QApplication,
        QDialog,
        QLabel,
        QVBoxLayout,
        QTableWidget,
        QTableWidgetItem,
    )
    qtwidgets = None  # Real modules in use
except Exception:  # pragma: no cover - fallback stubs
    qtwidgets = types.ModuleType("PyQt6.QtWidgets")

    class _Widget:
        def __init__(self, *args, **kwargs):
            self._visible = False
            self._title = ""
        def show(self):
            self._visible = True
        def close(self):
            self._visible = False
        def isVisible(self):
            return self._visible
        def setWindowTitle(self, title):
            self._title = title
        def windowTitle(self):
            return self._title
        def addWidget(self, *a, **k):
            pass

    class QApplication:
        def __init__(self, *a, **k):
            pass
        @staticmethod
        def instance():
            return None
        def processEvents(self):
            pass
        def quit(self):
            pass

    class QLabel(_Widget):
        def __init__(self, *a, **k):
            super().__init__()

    class QVBoxLayout:
        def __init__(self, *a, **k):
            pass
        def addWidget(self, *a, **k):
            pass

    class QTableWidget(_Widget):
        def __init__(self, *a, **k):
            super().__init__()
            self._items = {}
        def setColumnCount(self, n):
            pass
        def setRowCount(self, n):
            pass
        def setHorizontalHeaderLabels(self, labels):
            pass
        def setItem(self, row, col, item):
            self._items[(row, col)] = item
        def item(self, row, col):
            return self._items.get((row, col))
        def resizeColumnsToContents(self):
            pass

    class QTableWidgetItem:
        def __init__(self, text):
            self._text = text
        def text(self):
            return self._text

    qtwidgets.QApplication = QApplication
    qtwidgets.QDialog = _Widget
    qtwidgets.QLabel = QLabel
    qtwidgets.QVBoxLayout = QVBoxLayout
    qtwidgets.QTableWidget = QTableWidget
    qtwidgets.QTableWidgetItem = QTableWidgetItem

    def _install_qt_stubs():
        sys.modules.setdefault("PyQt6", types.ModuleType("PyQt6"))
        sys.modules["PyQt6.QtWidgets"] = qtwidgets

    _install_qt_stubs()

    # Expose names locally for type checkers
    QDialog = _Widget
    QLabel = QLabel
    QVBoxLayout = QVBoxLayout
    QTableWidget = QTableWidget
    QTableWidgetItem = QTableWidgetItem
else:
    def _install_qt_stubs():
        """No-op when real PyQt6 is available."""
        pass


@pytest.fixture(scope="session")
def qapp():
    """Provide a QApplication instance for tests."""
    _install_qt_stubs()
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    if hasattr(app, "quit"):
        app.quit()


@pytest.fixture
def dialog(qapp):
    """Create and automatically close dialogs/widgets."""
    dialogs = []

    def _open(cls, *args, **kwargs):
        _install_qt_stubs()
        dlg = cls(*args, **kwargs)
        dlg.show()
        if hasattr(qapp, "processEvents"):
            qapp.processEvents()
        dialogs.append(dlg)
        return dlg

    yield _open

    for dlg in dialogs:
        dlg.close()
        if hasattr(qapp, "processEvents"):
            qapp.processEvents()
