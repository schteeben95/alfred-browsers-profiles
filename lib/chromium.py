import os
import json
from lib.helpers import get_browsers_titles


def get_chromium_profiles(browser, path):
    browser_titles = get_browsers_titles('chromium')

    name = browser['name']
    icon = browser['icon']
    title = browser_titles[name]

    profiles = []

    if os.path.isdir(path) == False:
        return profiles

    # Read profile names from Local State (per-profile Preferences often just says "Your Chrome")
    info_cache = {}
    local_state_file = os.path.join(path, "Local State")
    if os.path.isfile(local_state_file):
        with open(local_state_file) as f:
            local_state = json.load(f)
            info_cache = local_state.get("profile", {}).get("info_cache", {})

    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    for folder in folders:
        file = "{}/{}/Preferences".format(path, folder)
        if folder != 'System Profile' and os.path.isfile(file):
            cached = info_cache.get(folder, {})
            browser_profile = (
                cached.get("name")
                or cached.get("shortcut_name")
                or cached.get("gaia_name")
                or folder
            )

            profiles.append({
                "icon": {
                    "path": "icons/{}".format(icon)
                },
                "arg": "{} {}".format(name, folder),
                "subtitle": "Open {} using {} profile.".format(title, browser_profile),
                "title": browser_profile,
            })

    return profiles
