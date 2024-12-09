from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="SHOWCASE",
    load_dotenv=True,
    settings_files=["settings.toml", ".secrets.toml"],
    merge_enabled=True,
    environments=True,
)
settings.validators.register(
    validators=[
        Validator(
            "airtable_token",
            must_exist=True,
        ),
        Validator(
            "airtable_base_id",
            must_exist=True,
        ),
        Validator(
            "airtable_events_table_id",
            must_exist=True,
        ),
        Validator(
            "airtable_users_table_id",
            must_exist=True,
        ),
    ],
)

settings.validators.validate()
