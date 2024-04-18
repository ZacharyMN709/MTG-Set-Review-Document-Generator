from __future__ import annotations

import json

from definitions import CONFIG_DIR


class Config(dict):
    """
    Adapted from: https://stackoverflow.com/a/68244012
    
    Override to use dot notation access to dictionary attributes.

    By doing this however, we cannot add functions to be accessed on the object
    (which being a config object, may be for the better), so any validation or
    sanitization has to be taken care of in the static constructors or __init__
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        result = Config()
        for key, value in data.items():
            result[key] = Config.__load__(value)
        return result

    @staticmethod
    def load_list(data: list):
        result = [Config.__load__(item) for item in data]
        return result

    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Config.__load__(json.loads(f.read()))
        return result


class SetGeneratorConfig(Config):
    # TODO: Implement checks to ensure we have the data we need to run.

    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Config.__load__(json.loads(f.read()))

        result = SetGeneratorConfig._sanitize(result)
        SetGeneratorConfig._validate(result)
        return result

    # TODO: Implement logic to repair missing data.
    @staticmethod
    def _sanitize(self: SetGeneratorConfig):
        return self

    # TODO: Check for missing irreparable data.
    @staticmethod
    def _validate(self: SetGeneratorConfig):
        valid = True

        if not valid:
            raise ValueError("Invalid config detected")


if __name__ == "__main__":
    import os

    config = SetGeneratorConfig.load_json(os.path.join(CONFIG_DIR, "OTJ.json"))
    print(config.set_context.set_code)
    print(config.set_context.bonus_set_code)
    print(config.set_context.scryfall_queries)

