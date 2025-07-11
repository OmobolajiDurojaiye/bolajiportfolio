from . import main_bp
from flask import render_template, request, flash, redirect, url_for, current_app
from pkg.models import db, ContactSubmission
from flask_mail import Mail, Message

# Ensure Mail is initialized in your main app factory (__init__.py)
mail = Mail()

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not name or not email or not message_body:
            flash('All fields are required.', 'error')
            return redirect(url_for('main.contact'))

        try:
            # 1. Save submission to the database
            new_submission = ContactSubmission(
                name=name,
                email=email,
                message=message_body
            )
            db.session.add(new_submission)
            
            # 2. Prepare emails
            # Email to Admin (You)
            msg_to_admin = Message(
                subject=f"New Portfolio Message from {name}",
                recipients=[current_app.config['MAIL_USERNAME']]
            )
            msg_to_admin.body = f"From: {name} <{email}>\n\nMessage:\n{message_body}"

            # Confirmation Email to User
            msg_to_user = Message(
                subject="Thank you for your message!",
                recipients=[email]
            )
            msg_to_user.html = render_template('emails/contact_confirmation.html', name=name)

            # 3. Send emails
            mail.send(msg_to_admin)
            mail.send(msg_to_user)
            
            # 4. Commit to DB after successful email sending
            db.session.commit()

            flash('Your message has been sent successfully! I will get back to you soon.', 'success')
        
        except Exception as e:
            db.session.rollback()  # Rollback DB changes if anything fails
            current_app.logger.error(f"Failed to process contact form: {e}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')

        return redirect(url_for('main.contact'))

    return render_template('main/contact.html')