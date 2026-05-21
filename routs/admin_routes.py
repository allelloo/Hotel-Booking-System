from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import db, User, Room, Booking
from routs.utils import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_rooms = Room.query.count()
    total_bookings = Booking.query.count()
    total_users = User.query.filter_by(role='customer').count()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    rooms = Room.query.all()
    return render_template('dashboard.html',
                           total_rooms=total_rooms,
                           total_bookings=total_bookings,
                           total_users=total_users,
                           recent_bookings=recent_bookings,
                           rooms=rooms)

@admin_bp.route('/add-room', methods=['GET', 'POST'])
@login_required
@admin_required
def add_room():
    if request.method == 'POST':
        room_number = request.form.get('room_number', '').strip()
        room_type = request.form.get('room_type', '').strip()
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        description = request.form.get('description', '').strip()
        image = request.form.get('image', '').strip() or 'default_room.jpg'
        if not room_number or not room_type or not price or not capacity:
            flash('All required fields must be filled.', 'danger')
        elif Room.query.filter_by(room_number=room_number).first():
            flash('Room number already exists.', 'danger')
        else:
            room = Room(
                room_number=room_number,
                room_type=room_type,
                price=float(price),
                capacity=int(capacity),
                description=description,
                image=image
            )
            db.session.add(room)
            db.session.commit()
            flash('Room added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('add_room.html')

@admin_bp.route('/edit-room/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        room.room_number = request.form.get('room_number', '').strip()
        room.room_type = request.form.get('room_type', '').strip()
        room.price = float(request.form.get('price', room.price))
        room.capacity = int(request.form.get('capacity', room.capacity))
        room.description = request.form.get('description', '').strip()
        room.image = request.form.get('image', '').strip() or room.image
        room.status = request.form.get('status', room.status)
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_room.html', room=room)

@admin_bp.route('/delete-room/<int:room_id>', methods=['POST'])
@login_required
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    active_booking = Booking.query.filter(
        Booking.room_id == room.id,
        Booking.status != 'cancelled'
    ).first()

    if active_booking:
        flash('Cannot delete this room because it has active bookings.', 'danger')
        return redirect(url_for('admin.dashboard'))

    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))