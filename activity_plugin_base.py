"""Base class for GarminDb plugins."""

__author__ = "Tom Goetz"
__copyright__ = "Copyright Tom Goetz"
__license__ = "GPL"

import logging


logger = logging.getLogger(__file__)


class ActivityPluginBase():
    """Base class for GarminDb plugins."""

    @classmethod
    def matches_activity_file(cls, fit_file):
        """Return if the file matches this plugin."""
        if hasattr(cls, '_application_id') and cls._application_id == fit_file.dev_application_id:
            logger.info("Plugin %s matches file %s on application_id %r", cls.__name__, fit_file, cls._application_id)
            return True
        if hasattr(cls, '_sport') and (fit_file.sport_type is None or fit_file.sport_type.value is not cls._sport):
            return False
        if hasattr(cls, '_sub_sport') and (fit_file.sub_sport_type is None or fit_file.sub_sport_type.value is not cls._sub_sport):
            return False
        if hasattr(cls, '_dev_fields'):
            for dev_field in cls._dev_fields:
                if dev_field not in fit_file.dev_fields:
                    logger.info("dev field %s not in %s", dev_field, fit_file.filename)
                    return False
        logger.info("Plugin %s matches file %s", cls.__name__, fit_file)
        return True

    @classmethod
    def init_activity(cls, dynamic_db, act_db_class, activities_table):
        """Initialize an instance of the elliptical plugin as an activity FIT file plugin."""
        logger.info("Initializing tables for activity plugin %s with act_table %s", cls.__name__, activities_table)
        if hasattr(cls, '_records_tablename') and 'record' not in cls._tables:
            cls._tables['record'] = dynamic_db.CreateTable(cls._records_tablename, act_db_class, cls._records_version, cls._records_pk, cls._records_cols)
        if hasattr(cls, '_laps_tablename') and 'lap' not in cls._tables:
            cls._tables['lap'] = dynamic_db.CreateTable(cls._laps_tablename, act_db_class, cls._laps_version, cls._laps_pk, cls._laps_cols)
        if hasattr(cls, '_sessions_tablename') and 'session' not in cls._tables:
            cls._tables['session'] = dynamic_db.CreateTable(cls._sessions_tablename, act_db_class, cls._sessions_version, cols=cls._sessions_cols,
                                                            create_view=cls._views['activity_view'], vars={'activities_table': activities_table})

    @classmethod
    def _get_field(cls, message_fields, field_name_list):
        for field_name in field_name_list:
            if field_name in message_fields:
                return message_fields[field_name]

    def __str__(self):
        """Return a string representation of the class instance."""
        return f'{self.__class__.__name__}(tables {self._records_tablename} and {self._sessions_tablename})'