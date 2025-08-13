import pytest

@pytest.fixture
def dialog_opener():
    """Create dialogs and ensure they are closed after the test."""
    created = []

    def _open(dialog_cls, *args, **kwargs):
        dlg = dialog_cls(*args, **kwargs)
        created.append(dlg)
        show = getattr(dlg, "show", None)
        if callable(show):
            try:
                show()
            except Exception:
                pass
        return dlg

    yield _open

    for dlg in created:
        for name in ("close", "done", "accept", "reject", "hide"):
            method = getattr(dlg, name, None)
            if callable(method):
                try:
                    method()
                    break
                except Exception:
                    continue
