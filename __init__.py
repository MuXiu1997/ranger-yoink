import os.path
import subprocess

import ranger.api
import ranger.api.commands

HOOK_INIT_OLD = ranger.api.hook_init


def hook_init(fm):
    fm.execute_console('map YY eval fm.execute_console("yoink %s") '
                       'if fm.thisdir.marked_items else fm.execute_console("yoink %f")')

    return HOOK_INIT_OLD(fm)


ranger.api.hook_init = hook_init


class yoink(ranger.api.commands.Command):
    """
    :yoink <paths...>

    Send to Yoink
    """

    def execute(self):
        paths = self.args[1:]
        if not paths:
            return

        _paths = paths
        paths = [path for path in paths if os.path.isdir(path) or os.path.isfile(path)]
        if len(paths) == 0:
            self.fm.notify('invalid paths: {}'.format(_paths), bad=True)
            return

        invalid_paths = [path for path in _paths if path not in paths]
        if self.send(paths):
            if len(invalid_paths) == 0:
                self.fm.notify('sent to yoink: {}'.format(paths))
                return
            self.fm.notify('sent to yoink: {}, invalid paths: {}'.format(paths, invalid_paths))

    def send(self, paths):
        try:
            subprocess.Popen(['open', '-a', 'Yoink', *paths])
        except Exception as e:
            self.fm.notify(e, bad=True)
            return False
        return True
