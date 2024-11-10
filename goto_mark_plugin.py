import sublime
import sublime_plugin


from typing import Any, Optional

settings = None


class GotoMark(sublime_plugin.WindowCommand):
    def run(self):
        def on_select(selected_idx):
            pass

        def on_highlight(selected_idx):
            self.marker = self.markers[selected_idx]
            sel = self.target_view.sel()
            sel.clear()
            sel.add(self.marker)
            self.target_view.show(self.marker)

        def show_panel():
            self.target_view = self.window.active_view()
            self.extractions = []
            self.markers = self.target_view.find_all(
                r"(%%[^\n$]*)",
                flags=sublime.FindFlags.NONE,
                extractions=self.extractions,
                fmt=r"\1",
            )

            self.window.show_quick_panel(
                self.extractions,
                on_select=on_select,
                on_highlight=on_highlight,
            )

        sublime.set_timeout(show_panel, 0)


class GotoMarkListener(sublime_plugin.EventListener):
    def on_query_context(
        self,
        view: sublime.View,
        key: str,
        operator: "sublime.QueryOperator",
        operand: Any,
        match_all: bool,
    ) -> Optional[bool]:
        if not key.startswith("goto_mark."):
            return None

        settings_key = key[len("goto_mark.") :]
        setting_value = settings.get(settings_key, None)

        if operator == sublime.OP_EQUAL:
            return setting_value == operand

        if operator == sublime.OP_NOT_EQUAL:
            return setting_value != operand

        return None


def plugin_loaded():
    global settings
    settings = sublime.load_settings("GotoMark.sublime-settings")
    print(f"Settings: {settings.to_dict()}")
