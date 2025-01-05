import logging

from app import create_app

app = create_app()
app.logger.setLevel(logging.INFO)

if __name__ == "__main__":
    app.run()