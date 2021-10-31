import urllib.request
import urllib.error
import obspython as obs
import json

url = ""

# ------------------------------------------------------------


def update():
    global url
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            response = json.loads(data)

            _scenes = zip(obs.obs_frontend_get_scene_names(),
                          obs.obs_frontend_get_scenes())
            scenes = {}
            for scene in _scenes:
                scenes[scene[0]] = scene[1]
            if scenes.get(response['camera']) is not None:
                print("Switching to scene: " + response['camera'])
                obs.obs_frontend_set_current_scene(scenes[response['camera']])

    except urllib.error.URLError as err:
        obs.script_log(obs.LOG_WARNING,
                       "Error opening URL '" + url + "': " + err.reason)
        obs.remove_current_callback()


# ------------------------------------------------------------


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """

    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "url", "URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "secret", "secret",
                                obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "cycle_rate", "Cycle Rate(ms)",
                               10000, 10000, 10000)
    return props


def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global url

    obs.timer_remove(update)
    blink_rate = obs.obs_data_get_int(settings, "cycle_rate")
    obs.timer_add(update, blink_rate)  # Change scene every cycle_rate ms
    url = obs.obs_data_get_string(settings, "url")
