from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    """
    Entry point for running the Flask development server.
    This will start the application with debug mode enabled.
    """
    app.run(debug=True)
