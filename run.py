from teinfbot.bot import TeinfBot
import os

if __name__ == "__main__":
    DEBUG = True if os.environ.get("DEBUG") == "TRUE" else False
    tfbot = TeinfBot(debug=DEBUG)
    tfbot.run()
