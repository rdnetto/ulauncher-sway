import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import subprocess
import sway.windows as windows
from sway.icons import get_icon


logger = logging.getLogger(__name__)


class SwayWindowsExtension(Extension):

    def __init__(self):
        super(SwayWindowsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    '''Generates items for display on query'''

    def on_event(self, event, extension):
        items = list([self.get_result_item(w)
                      for w in windows.get_windows()
                      # Don't include the ulauncher dialog in the list,
                      # since it already has focus
                      if not w["focused"]])
        return RenderResultListAction(items)


    def get_result_item(self, con):
        (_, appName, winTitle) = windows.app_details(con)

        return ExtensionResultItem(
                icon=get_icon(con),
                name=winTitle,
                description=appName,
                # This only works because con is a dict, and therefore pickleable
                on_enter=ExtensionCustomAction(con))


class ItemEnterEventListener(EventListener):
    '''Executes the focus event, using the data provided in ExtensionCustomAction'''

    def on_event(self, event, extension):
        con = event.get_data()
        windows.focus(con)


if __name__ == '__main__':
    SwayWindowsExtension().run()
