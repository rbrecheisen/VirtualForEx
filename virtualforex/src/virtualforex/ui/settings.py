from PySide6.QtCore import QSettings

from virtualforex.ui.constants import Constants


class Settings(QSettings):
    def __init__(self):
        super(Settings, self).__init__(
            QSettings.IniFormat, 
            QSettings.UserScope, 
            Constants.VIRTUALFOREX_BUNDLE_IDENTIFIER, 
            Constants.VIRTUALFOREX_NAME,
        )

    def prepend_bundle_identifier_and_name(self, name):
        return '{}.{}.{}'.format(
            Constants.VIRTUALFOREX_BUNDLE_IDENTIFIER, 
            Constants.VIRTUALFOREX_NAME,
            name,
        )

    def get(self, name, default=None):
        if not name.startswith(Constants.VIRTUALFOREX_BUNDLE_IDENTIFIER):
            name = self.prepend_bundle_identifier_and_name(name)
        value = self.value(name)
        if value is None or value == '':
            return default
        return value
    
    def set(self, name, value):
        name = self.prepend_bundle_identifier_and_name(name)
        self.setValue(name, value)