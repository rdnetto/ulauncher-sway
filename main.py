import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import subprocess
import sway.windows as windows
from sway.icons import get_icon


logger = logging.getLogger(__name__)


class SwayWindowsExtension(Extension):

    def __init__(self):
        super(SwayWindowsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = list([self.get_result_item(w) for w in windows.get_windows()])
        return RenderResultListAction(items)


    def get_result_item(self, con):
        (_, appName, winTitle) = windows.app_details(con)

        cmd = windows.focus_cmd(con)

        return ExtensionResultItem(
                icon=get_icon(con),
                name=winTitle,
                description=appName,
                on_enter=self.swaymsg_action(cmd))

    def swaymsg_action(self, args):
        ''' We can only use predefined actions, so have to specify the
            behaviour using a shell script
        '''
        return RunScriptAction("#!/bin/sh -e\nswaymsg " + " ".join(["'" + a + "'" for a in args]))


if __name__ == '__main__':
    SwayWindowsExtension().run()
