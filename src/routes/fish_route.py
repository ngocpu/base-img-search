from flask import Blueprint, request, render_template
from src.controler.fish_controller import FishControler

fish_bp = Blueprint('fish', __name__)
@fish_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home')

@fish_bp.route('/search', methods=['POST'])
def search():
    file = request.files.get('image')
    return FishControler.search_similar_images(file)