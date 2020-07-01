from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
import subprocess
import sway.windows


class SwayWindowsExtension(Extension):

    def __init__(self):
        super(SwayWindowsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        windows = sway.windows.get_windows()
        items = list([self.get_result_item(w) for w in windows])
        return RenderResultListAction(items)

    def get_result_item(self, con):
        (_, appName, winTitle) = sway.windows.app_details(con)

        cmd = sway.windows.focus_cmd(con)

        return ExtensionResultItem(
                # TODO: use the right icon
                icon='images/icon.png',
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
