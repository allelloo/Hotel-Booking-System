from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, date
from models import db, User, Room, Booking

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/book/<int:room_id>', methods=['GET', 'POST'])
@login_required
def book(room_id):
    room = Room.query.get_or_404(room_id)

    if request.method == 'POST':
        check_in_str = request.form.get('check_in')
        check_out_str = request.form.get('check_out')

        try:
          check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
          check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
          flash('Invalid dates.', 'danger')
          return render_template('book.html', room=room)

        if check_in >= check_out:
            flash('Check-out must be after check-in.', 'danger')
            return render_template('book.html', room=room)

        if check_in < date.today():
            flash('Check-in cannot be in the past.', 'danger')
            return render_template('book.html', room=room)

        existing_booking = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.status == 'confirmed',
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()

        if existing_booking:
            flash('Room already booked for these dates.', 'danger')
            return render_template('book.html', room=room)

        nights = (check_out - check_in).days
        total_price = nights * room.price

        booking = Booking(
            user_id=current_user.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='confirmed'
        )

        room.status = 'booked'

        db.session.add(booking)
        db.session.commit()

        flash('Room booked successfully!', 'success')
        return redirect(url_for('customer.my_bookings'))

    return render_template('book.html', room=room)

@customer_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

@customer_bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('customer.my_bookings'))
    if booking.status == 'cancelled':
        flash('Already cancelled.', 'warning')
    else:
        booking.status = 'cancelled'
        booking.room.status = 'available'
        db.session.commit()
        flash('Booking cancelled.', 'success')
    return redirect(url_for('customer.my_bookings'))

@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')

        existing_user = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('customer.profile'))

        current_user.username = username
        current_user.email = email

        if password:
            current_user.password = generate_password_hash(password)

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('customer.profile'))

    return render_template('profile.html')