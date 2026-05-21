from flask import Blueprint, render_template, request
from models import Room 

public_bp = Blueprint('public', __name__)
@public_bp.route('/')
def home():
    rooms = Room.query.filter_by(status='available').limit(6).all()
    return render_template('home.html', rooms=rooms)

@public_bp.route('/rooms')
def rooms():
    room_type = request.args.get('type', '')
    if room_type:
        all_rooms = Room.query.filter(Room.room_type.ilike(f'%{room_type}%')).all()
    else:
        all_rooms = Room.query.all()
    return render_template('rooms.html', rooms=all_rooms, search_type=room_type)

@public_bp.route('/room/<int:room_id>')
def room_details(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room_details.html', room=room)