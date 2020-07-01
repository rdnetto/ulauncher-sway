import json
import subprocess
from sway.util import get_child_or_else


def focus_cmd(con):
    '''Returns the list of args to pass to swaymsg'''

    # Container objects have 3 different ID fields:
    #   id - the container ID, called con_id in criteria syntax
    #   app_id - specific to wayland apps
    #   ??? - specific to X11 apps, called id in criteria syntax
    con_id = con["id"]

    # invokes: '<criteria> focus' (documented in sway(5))
    return [f"[con_id=\"{con_id}\"]", "focus"]


def get_tree_object():
    return json.loads(subprocess.check_output(["swaymsg", "-t", "get_tree"]))


def get_windows(tree=None):
    tree = get_tree_object() if tree == None else tree
    windows = []

    for output in tree["nodes"]:
        assert output["type"] == "output", "Expected output, got" + repr(output)

        for workspace in output["nodes"]:
            assert workspace["type"] == "workspace", "Expected workspace, got" + repr(workspace)

            for container in get_child_or_else(workspace, "nodes", []):
                windows += get_container_windows(container)

            for container in get_child_or_else(workspace, "floating_nodes", []):
                windows += get_container_windows(container)

    return windows


def get_container_windows(con):
    windows = []

    # Check if the container is an application in its own right
    if "app_id" in con.keys():
        windows.append(con)

    # Recurse
    for child in con['nodes']:
        windows += get_container_windows(child)

    return windows


def app_details(con):
    # app_id is wayland only, window_properties is X11 only
    app_name = (con["app_id"]
                if ("app_id" in con and con["app_id"] != None)
                else con["window_properties"]["instance"])

    # (con_id, application name, window title)
    return (con["id"], app_name, con["name"])


if __name__ == "__main__":
    tree = get_tree_object()
    wins = get_windows(tree)

    for w in wins:
        print(app_details(w))

