import json
import os

class I18n:
    def __init__(self, default_lang="en"):
        self._lang = default_lang
        self._data = {}
        self._callbacks = []
        self._load(default_lang)

    def _load(self, lang):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "translations", f"{lang}.json")
        with open(path, encoding="utf-8") as f:
            self._data = json.load(f)
        self._lang = lang

    def set_lang(self, lang):
        self._load(lang)
        for cb in self._callbacks:
            try:
                cb()
            except Exception:
                pass  # widget may have been destroyed

    def t(self, *keys):
        """Get translation by keys, e.g. t('login', 'sign_in')"""
        val = self._data
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, keys[-1])
            else:
                return keys[-1]
        return val

    def on_change(self, callback):
        """Register a refresh callback for language changes."""
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    @property
    def lang(self):
        return self._lang

# Global singleton — import this everywhere
i18n = I18n("en")
