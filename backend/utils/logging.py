import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

setup_logging()  # Ensure logging is actually set up when imported
