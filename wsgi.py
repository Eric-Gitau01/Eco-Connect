from app import create_app
import os


# Set the environment variable for the Flask app
env = os.getenv('FLASK_ENV', 'production')
# Create the Flask app based on the environment
app = create_app(env)


if __name__ == "__main__":
    app.run()