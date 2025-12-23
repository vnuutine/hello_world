import pytest
from hello_world import Config, ConfigValidator, Logger

def test_config_validator_rejects_empty_primary():
    cfg = Config(
        greeting_primary="",
        greeting_secondary="world",
        separator=",",
        space=" ",
        punctuation="!",
        output_enabled=True,
    )

    validator = ConfigValidator(Logger("test"))
    with pytest.raises(ValueError):
        validator.validate(cfg)

def test_config_validator_accepts_valid_config():
    cfg = Config(
        greeting_primary="Hello",
        greeting_secondary="world",
        separator=",",
        space=" ",
        punctuation="!",
        output_enabled=True,
    )

    validator = ConfigValidator(Logger("test"))
    validator.validate(cfg)  # should not raise
    