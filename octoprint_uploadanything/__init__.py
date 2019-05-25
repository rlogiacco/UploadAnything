# coding=utf-8

import octoprint.plugin
import os
import octoprint.filemanager
import octoprint.filemanager.util

class UploadAnythingPlugin(octoprint.plugin.TemplatePlugin,
                octoprint.plugin.SettingsPlugin):
	
	@property
	def allowed(self):
		return str(self._settings.get(["allowed"]))

	##-- Settings hooks
	def get_settings_defaults(self):
		return ({'allowed': '3mf, obj, stl, png, gif, jpg'})
	
	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False)]

	##-- Image upload extenstion tree hook
	def get_extension_tree(self, *args, **kwargs):
		return dict(
			machinecode=dict(
				uploadanything=self.allowed.replace(" ", "").split(",")
			)
		)
		
	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version
		
	def get_update_information(self):
		return dict(
			uploadanything=dict(
				displayName="Custom Extensions",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="rlogiacco",
				repo="UploadAnything",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/rlogiacco/UploadAnything/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Upload Anything"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = UploadAnythingPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.filemanager.extension_tree": __plugin_implementation__.get_extension_tree
	}
