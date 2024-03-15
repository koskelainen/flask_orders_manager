from pathlib import Path

from dotenv import load_dotenv

from src import create_application

fpath = Path(".env.local")
if fpath.exists():
    load_dotenv(dotenv_path=fpath, override=True)

app = create_application()
if __name__ == '__main__':
    app.run()
