import os.path
import subprocess

import ranger.api
import ranger.api.commands

HOOK_INIT_OLD = ranger.api.hook_init


def hook_init(fm):
    HOOK_INIT_OLD(fm)

    fm.execute_console('map YY eval fm.execute_console("yoink %s") '
                       'if fm.thisdir.marked_items else fm.execute_console("yoink %f")')


ranger.api.hook_init = hook_init


class yoink(ranger.api.commands.Command):
    """
    :yoink

    Send to Yoink
    """

    def execute(self):
        paths = self.args[1:]
        if not paths:
            return

        paths = [path for path in paths if os.path.isdir(path) or os.path.isfile(path)]
        self.send(paths)

    def send(self, paths):
        try:
            subprocess.Popen(['open', '-a', 'Yoink', *paths])
        except Exception as e:
            self.fm.notify(e, bad=True)
