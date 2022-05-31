from .models.configuration import Configuration


def get_tracking_configuration():
    return Configuration.get_solo().get_configuration()
