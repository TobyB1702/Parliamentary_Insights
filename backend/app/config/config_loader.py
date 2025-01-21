# import yaml
# from pathlib import Path

# class Config:
#     """
#     A class to load and manage configuration settings from a YAML file.
#     """

#     def __init__(self, config_path: str):
#         """
#         Initialize the Config class with the given configuration file path.

#         Parameters:
#         config_path (str): The path to the configuration file.
#         """
#         self.config_path = config_path
#         self.config = self.load_config()

#     def load_config(self) -> dict:
#         """
#         Load the configuration from the YAML file.

#         Returns:
#         dict: The loaded configuration as a dictionary.
#         """
#         with open(self.config_path, 'r') as file:
#             return yaml.safe_load(file)


import yaml
import os
from pathlib import Path

class Config:
    """
    A class to load and manage configuration settings from a YAML file.
    """

    def __init__(self, config_path: str):
        """
        Initialize the Config class with the given configuration file path.

        Parameters:
        config_path (str): The path to the configuration file.
        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Load the configuration from the YAML file and replace placeholders with environment variables.

        Returns:
        dict: The loaded configuration as a dictionary.
        """
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            return self.replace_placeholders(config)

    def replace_placeholders(self, config: dict) -> dict:
        """
        Replace placeholders in the configuration with environment variable values.

        Parameters:
        config (dict): The configuration dictionary.

        Returns:
        dict: The configuration dictionary with placeholders replaced.
        """
        for key, value in config.items():
            if isinstance(value, dict):
                config[key] = self.replace_placeholders(value)
            elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var, value)
        return config