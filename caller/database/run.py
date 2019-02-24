"""
Contains all functions that access a Run object.
"""
from caller.database import Run


def add_run(db_session, endpoint_name, parameter, response_time, fmd_level):
    """ Adds a run to the database. Returns the id.
       :param db_session: session for the database
       :param endpoint_name: name of the endpoint that was executed
       :param parameter: parameter of the load
       :param response_time: time it took for the endpoint to execute
       :param fmd_level: the level of fmd
       :return the id of the run after it was stored in the database
       """
    run = Run(endpoint_name=endpoint_name, parameter=parameter, response_time=response_time, fmd_level=fmd_level)
    db_session.add(run)
    db_session.flush()
    return run.id
