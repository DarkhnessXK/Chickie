from dynaconf import Dynaconf  # type: ignore
from os.path import join, dirname
from pathlib import Path

PROJECT_PATH = str(Path(join(dirname(__file__))).parent.absolute())

s1 = join(PROJECT_PATH, "config", "settings.toml")
s2 = join(PROJECT_PATH, "config", ".secrets.toml")
settings_files = [s1, s2]

settings = Dynaconf(
    envvar_prefix="CHICKIE",
    # env_switcher='CHICKIE_ENV',
    environments=["local", "development", "production"],
    settings_files=settings_files,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
