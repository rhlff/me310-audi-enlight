from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


class SettingsBlueprint(Blueprint):
    def __init__(self, *args, **kwargs):
        assert 'url_prefix' in kwargs
        self.display_name = None
        if 'display_name' in kwargs:
            self.display_name = kwargs['display_name']
            del kwargs['display_name']
        super(SettingsBlueprint, self).__init__(*args, **kwargs)
        self.has_page = False
        self.activated = False
        if self.display_name is None:
            self.display_name = self.name

    def as_json(self):
        return {
            'name': self.display_name,
            'url': self.name + ".show",
            'activate_url': self.name + ".activate",
            'activated': self.activated,
            'has_page': self.has_page,
        }
