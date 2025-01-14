from flask import Flask
from werkzeug.serving import run_simple  # werkzeug development server
from app import application

if __name__ == "__main__":
 
    run_simple(
        "0.0.0.0",
        6000,
        application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        threaded=True
    )
