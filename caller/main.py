from caller.database import session_scope
from caller.database.run import add_run
import requests

# with session_scope() as db_session:
#     add_run(db_session, endpoint_name, parameter, response_time, fmd_level)

BASE_URL = 'http://127.0.0.1:5001/'


def main():
    r = requests.get(BASE_URL + 'powerset/19')
    print(r.json())
    with session_scope() as db_session:
        add_run(db_session, 'powerset', 19, r.json()['response_time'], -1)


if __name__ == "__main__":
    main()
