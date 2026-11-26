from web import create_app
import sys
from console import console_menu

def main():
    """Start the game mode"""
    if "--console" in sys.argv[1:]:
        console_menu()
    else:
        app = create_app()
        app.run(port=8000)
if __name__=="__main__":
    main()
