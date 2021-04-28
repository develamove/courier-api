from src.utils import response_creator, SERVER_ERROR


@response_creator
def handle_db_error(error):
    return 'Can\'t connect to main database', dict(database=['Can\'t connect to main database']),  SERVER_ERROR
