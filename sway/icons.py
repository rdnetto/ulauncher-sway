import os
import os.path
import logging
from xdg.IconTheme import getIconPath
from sway.util import get_child_or_else


logger = logging.getLogger(__name__)


def get_icon(con):
    '''Determines the icon for a program.
    '''
    logger.debug("Resolving icon for container %s...", con["id"])

    # See: https://lists.freedesktop.org/archives/wayland-devel/2018-April/037998.html
    suppliers = [
        # Wayland native apps - should just work
        icon_loader(con["app_id"])
        ]

    # X11 apps - this is a bit messier / more heuristic
    if("window_properties" in con):
        props = con["window_properties"]
        suppliers += [
                icon_loader(get_child_or_else(props, "class", None)),
                icon_loader(get_child_or_else(props, "instance", None))
            ]

    # Try matching on executable name, for cases where app_id is wrong
    # e.g. firefox-wayland
    pid = con["pid"]
    exePath = os.readlink(f"/proc/{pid}/exe")
    suppliers.append(icon_loader(os.path.basename(exePath)))

    # Evaluate suppliers lazily, returning the first successful one
    for f in suppliers:
        res = f()
        if res is not None:
            return res

    logger.info("Unable to find icon for container %d \"%s\"",
                con["id"],
                con["name"]
                )

    return "images/default.svg"


def icon_loader(name):
    '''Returns a helper function for lazily loading an icon'''

    def f():
        if name is None:
            return None

        res = getIconPath(name)
        logger.debug("Resolving %s: %s", name, "failed" if res is None else "succeeded")
        return res

    return f
