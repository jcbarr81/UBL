import sys, types, os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# ---- Stub PyQt6 modules ----
class DummySignal:
    def __init__(self):
        self._slot = None
    def connect(self, slot):
        self._slot = slot
    def emit(self):
        if self._slot:
            self._slot()

class Dummy:
    def __init__(self, *args, **kwargs):
        self.clicked = DummySignal()
        self.triggered = DummySignal()
    def __getattr__(self, name):
        return Dummy()
    def addItem(self, *args, **kwargs):
        pass
    def clear(self, *args, **kwargs):
        pass
    def setLayout(self, *args, **kwargs):
        pass
    def connect(self, *args, **kwargs):
        pass
    def setFont(self, *args, **kwargs):
        pass
    def exec(self, *args, **kwargs):
        pass
    def setPlainText(self, *args, **kwargs):
        pass
    def setReadOnly(self, *args, **kwargs):
        pass
    def setStyleSheet(self, *args, **kwargs):
        pass
    def setMinimumHeight(self, *args, **kwargs):
        pass
    def setWindowTitle(self, *args, **kwargs):
        pass
    def setGeometry(self, *args, **kwargs):
        pass
    def setContentsMargins(self, *args, **kwargs):
        pass
    def addTab(self, *args, **kwargs):
        pass
    def addStretch(self, *args, **kwargs):
        pass
    def setMenuBar(self, *args, **kwargs):
        pass
    def addWidget(self, *args, **kwargs):
        pass
    def addItems(self, *args, **kwargs):
        pass
    def currentItem(self):
        return None
    def setText(self, *args, **kwargs):
        pass
    def warning(self, *args, **kwargs):
        return 0
    def information(self, *args, **kwargs):
        return 0
    def critical(self, *args, **kwargs):
        return 0
    def question(self, *args, **kwargs):
        return 0

class QAction:
    def __init__(self, *args, **kwargs):
        self.triggered = DummySignal()
    def trigger(self):
        self.triggered.emit()

class QMenu(Dummy):
    def addAction(self, *args, **kwargs):
        return QAction()

class QMenuBar(Dummy):
    def addMenu(self, *args, **kwargs):
        return QMenu()

qtwidgets = types.ModuleType("PyQt6.QtWidgets")
widget_names = [
    'QWidget','QLabel','QVBoxLayout','QTabWidget','QListWidget','QTextEdit','QPushButton',
    'QHBoxLayout','QComboBox','QMessageBox','QGroupBox','QMenuBar','QDialog','QFormLayout',
    'QSpinBox','QGridLayout','QScrollArea','QLineEdit','QTableWidget','QTableWidgetItem'
]
for name in widget_names:
    setattr(qtwidgets, name, Dummy)
qtwidgets.QMenuBar = QMenuBar
qtwidgets.QMenu = QMenu
qtwidgets.QAction = QAction

class QListWidgetItem:
    def __init__(self, text):
        self._text = text
        self._data = {}
    def setData(self, role, value):
        self._data[role] = value
    def data(self, role):
        return self._data.get(role)
    def text(self):
        return self._text
qtwidgets.QListWidgetItem = QListWidgetItem

qtcore = types.ModuleType("PyQt6.QtCore")
class Qt:
    pass
qtcore.Qt = Qt
class QPropertyAnimation:
    pass
qtcore.QPropertyAnimation = QPropertyAnimation
sys.modules['PyQt6'] = types.ModuleType('PyQt6')
sys.modules['PyQt6.QtWidgets'] = qtwidgets
sys.modules['PyQt6.QtCore'] = qtcore

qtgui = types.ModuleType("PyQt6.QtGui")
class QFont:
    def __init__(self, *args, **kwargs):
        pass
    def setBold(self, *args, **kwargs):
        pass
    def setPointSize(self, *args, **kwargs):
        pass
qtgui.QFont = QFont
qtgui.QPixmap = Dummy
sys.modules['PyQt6.QtGui'] = qtgui

# ---- Imports after stubbing ----
import ui.owner_dashboard as owner_dashboard


def test_standings_action_opens_dialog(monkeypatch):
    opened = {}

    class DummyStandings:
        def __init__(self, *a, **k):
            pass
        def exec(self):
            opened["shown"] = True

    monkeypatch.setattr(owner_dashboard, "StandingsWindow", DummyStandings)

    def fake_init(self, team_id):
        self.team_id = team_id
        self.standings_action = QAction()
        self.standings_action.triggered.connect(self.open_standings_window)

    monkeypatch.setattr(owner_dashboard.OwnerDashboard, "__init__", fake_init)

    dashboard = owner_dashboard.OwnerDashboard("DRO")
    dashboard.standings_action.trigger()

    assert opened.get("shown")
