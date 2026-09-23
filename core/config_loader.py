from pathlib import Path

import yaml


# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Configuration file path
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"


def load_config():
    """
    Load SecMate configuration from settings.yaml.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_PATH}"
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "settings.yaml must contain a valid YAML mapping."
        )

    return config


def get_target_config():
    """
    Return the AI target configuration.
    """
    config = load_config()
    return config.get("target", {})


if __name__ == "__main__":
    configuration = load_config()

    print("SecMate configuration loaded successfully.")
    print("Application:", configuration.get("app", {}).get("name"))
    print("Target:", get_target_config().get("name"))
    print("Assessment mode:", configuration.get("assessment", {}).get("mode"))