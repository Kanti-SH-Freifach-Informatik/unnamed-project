from unnamedproject import app
from unnamedproject.routes.home_routes import home_bp
from unnamedproject.routes.game_routes import game_bp

app.register_blueprint(home_bp)
app.register_blueprint(game_bp, url_prefix='/games')