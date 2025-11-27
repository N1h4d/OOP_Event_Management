from .logging_config import setup_logging, get_logger
from .database.connection import DatabaseConnection
from .database.schema import initialize_database
from .controllers.cli_controller import CLIController

logger = get_logger(__name__)

def main():
    setup_logging()
    logger.info("Starting Event Management System...")

    db = DatabaseConnection()
    conn = db.connection

    initialize_database(conn)

    controller = CLIController(conn)
    controller.run()

    db.close()
    logger.info("Application stopped.")

if __name__ == "__main__":
    main()
