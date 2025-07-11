from flask import render_template, request, flash, redirect, url_for, current_app
from flask_mail import Mail, Message
from . import admin_bp
from pkg.models import db, ContactSubmission
from .auth import login_required


mail = Mail()

@admin_bp.route('/messages')
@login_required
def manage_messages():
    """Lists all contact submissions, most recent first."""
    messages = ContactSubmission.query.order_by(ContactSubmission.timestamp.desc()).all()
    return render_template('admin/manage_messages.html', messages=messages)

@admin_bp.route('/messages/view/<int:message_id>', methods=['GET', 'POST'])
@login_required
def view_message(message_id):
    """View a single message and handle the reply form."""
    message = ContactSubmission.query.get_or_404(message_id)

    if request.method == 'POST':
        reply_body = request.form.get('reply_body')
        if not reply_body:
            flash('Reply cannot be empty.', 'error')
            return redirect(url_for('admin.view_message', message_id=message.id))

        try:
            # Prepare and send the reply email
            msg = Message(
                subject=f"Re: Your message to Bolaji's Portfolio",
                recipients=[message.email],
                html=render_template(
                    'emails/admin_reply.html',
                    user_name=message.name,
                    original_message=message.message,
                    reply_body=reply_body
                )
            )
            mail.send(msg)
            flash('Reply sent successfully!', 'success')
            return redirect(url_for('admin.manage_messages'))

        except Exception as e:
            current_app.logger.error(f"Failed to send reply email: {e}")
            flash('There was an error sending the reply. Please try again.', 'error')

    # If GET request, mark the message as read
    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return render_template('admin/view_message.html', message=message)

@admin_bp.route('/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    """Deletes a message from the database."""
    message = ContactSubmission.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.manage_messages'))