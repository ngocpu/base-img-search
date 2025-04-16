
from src import init_app
from dotenv import load_dotenv
load_dotenv()
app = init_app()

if __name__ == '__main__':
    app.run(debug=True)
