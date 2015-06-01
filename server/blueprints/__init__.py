from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

import threading
from datetime import datetime

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

class StoppableThread(threading.Thread):
    def __init__(self, actions):
        super(StoppableThread, self).__init__()
        self.actions = sorted(actions, key=lambda x: x[0])
        self.start_time = datetime.now()
        self.stopped = False

    def run(self):
        while not self.stopped:
            diff = (datetime.now() - self.start_time).totalSeconds()
            while self.actions and self.actions[0] <= diff and not self.stopped:
                action = self.actions[0]
                action[1](*(action[2]))
                self.actions.pop(0)

