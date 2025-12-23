import pytest

@pytest.fixture(autouse=True)
def _silence_print(monkeypatch):
    # Your Logger prints a lot; tests should stay signal > noise.
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)