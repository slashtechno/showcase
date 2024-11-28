from pyairtable import Api, Table
# from pyairtable.formulas import match
from showcase import settings



events: Table = None


def get_events(api: Api) -> Table:
    events = api.table(settings.airtable_base_id, settings.airtable_events_table_id)
    return events

def main():
    api = Api(api_key=settings.airtable_token)
    global events
    events = get_events(api)

main()