from website import create_app
from os import getenv

DEBUG_OPTION = getenv("DEBUG_OPTION")

# Create app 
app = create_app()

# If main starts, run the app with debugger on
if __name__ == "__main__":
    app.run(debug=DEBUG_OPTION)
