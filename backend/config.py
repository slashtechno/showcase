from dynaconf import Dynaconf, Validator
import re

settings = Dynaconf(
    envvar_prefix="SHROUD",
    load_dotenv=True,
    settings_files=["settings.toml", ".secrets.toml"],
    merge_enabled=True,
)
settings.validators.register(
    validators=[
        Validator(
            "slack_bot_token",
            must_exist=True,
            condition=lambda x: x.startswith("xoxb-"),
            messages={"condition": "Must start with 'xoxb-'"},
        ),
        Validator(
            "slack_app_token",
            must_exist=True,
            condition=lambda x: x.startswith("xapp-"),
            messages={"condition": "Must start with 'xapp-'"},
        ),
        Validator(
            "channel",
            must_exist=True,
            condition=lambda x: re.match(r"^[CG][A-Z0-9]{10}$", x) is not None,
            messages={"condition": "Must look like C123ABC456 or G123ABC456"},
            default="C07JX2TK0UX",
        ),
        Validator(
            "airtable_token",
            must_exist=True,
        ),
        Validator(
            "airtable_base_id",
            must_exist=True,
        ),
        Validator(
            "airtable_table_name",
            must_exist=True,
        ),

        # Optional settings
        Validator(
            "leading_help_text",
            default="",
        ),
        Validator(
            "command_prefix",
            default="shroud-",
        ),
    ],
)

settings.validators.validate()
