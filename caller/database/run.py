"""
Contains all functions that access a Run object.
"""
from caller.database import Run, session_scope


def add_run(endpoint_name, parameter, response_time, fmd_level):
    """ Adds a run to the database. Returns the id.
       :param endpoint_name: name of the endpoint that was executed
       :param parameter: parameter of the load
       :param response_time: time it took for the endpoint to execute
       :param fmd_level: the level of fmd
       :return the id of the run after it was stored in the database
       """
    run = Run(endpoint_name=endpoint_name, parameter=parameter, response_time=response_time, fmd_level=fmd_level)
    with session_scope() as db_session:
        db_session.add(run)
        db_session.flush()
        return run.id


def get_runs(endpoint_name):
    """
    Returns all Run objects from the database for the given endpoint name.
    :param endpoint_name: name of the endpoint for which the runs are collected
    :return list of Run objects
    """
    with session_scope() as db_session:
        return db_session.query(Run).filter(Run.endpoint_name == endpoint_name)
