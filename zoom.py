import obspython as obs
import urllib.request
import urllib.error


participants    = 1
source_name = ""

# ------------------------------------------------------------

def update_obs():
	global participants
	global source_name

	source = obs.obs_get_source_by_name(source_name)
	print(source)
	if source is not None:
		
			#with urllib.request.urlopen(url) as response:
				#data = response.read()
				#text = data.decode('utf-8')
                        
		settings = obs.obs_data_create()
		obs.obs_data_set_int(settings, "text", participants)
		obs.obs_source_update(source, settings)
		obs.obs_data_release(settings)

		#except urllib.error.URLError as err:
			#obs.script_log(obs.LOG_WARNING, "Error opening URL '"+ "': " + err.reason)
			#obs.remove_current_callback()

		obs.obs_source_release(source)

def refresh_pressed(props, prop):
	update_obs()

# ------------------------------------------------------------

def script_description():
	return "Takes the feed from Zoom meeting and auto updates the OBS when you add the participants below.\n\nBy Karan"

def script_update(settings):

	global participants
	global source_name

	participants    = obs.obs_data_get_int(settings, "participants")
	source_name = obs.obs_data_get_string(settings, "source")

	obs.timer_remove(update_obs)


def script_properties():
	props = obs.obs_properties_create()


	obs.obs_properties_add_int(props, "participants", "Participants", 1, 12, 1)

	p = obs.obs_properties_add_list(props, "source", "Video Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
                        
			source_id = obs.obs_source_get_unversioned_id(source)
			if source_id == "window_capture":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)

	obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
	return props
