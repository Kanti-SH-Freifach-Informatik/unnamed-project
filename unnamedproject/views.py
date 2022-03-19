from unnamedproject import app
from unnamedproject.routes.game_routes import game_bp

app.register_blueprint(game_bp, url_prefix='/games')

@app.route('/')
def index():
    return 'Hello World!'