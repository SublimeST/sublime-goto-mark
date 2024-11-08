import sublime
import sublime_plugin


class GoToMark(sublime_plugin.WindowCommand):
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
                fmt=r"\1"
            )

            self.window.show_quick_panel(
                self.extractions,
                on_select=on_select,
                on_highlight=on_highlight,
            )

        sublime.set_timeout(show_panel, 0)
