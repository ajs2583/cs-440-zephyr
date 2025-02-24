from website import create_app
import os 

DEBUG_OPTION = os.environ("DEBUG_OPTION")

# Create app 
app = create_app()

# If main starts, run the app with debugger on
if __name__ == "__main__":
    app.run(debug=DEBUG_OPTION)
