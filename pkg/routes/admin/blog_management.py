import os
from flask import render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from slugify import slugify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from . import admin_bp
from pkg.models import db, BlogPost
from .auth import login_required
from .manage_projects import save_file, delete_file # Reuse helper functions

# --- Form Definition ---
class BlogPostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Subtitle (Optional)', validators=[Optional(), Length(max=200)])
    
    thumbnail = FileField('Thumbnail Image (JPG, PNG)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only JPG and PNG images are allowed!')
    ])
    
    category = SelectField('Category', choices=[
        ('Use Cases', 'Use Cases'), 
        ('Cryptocurrencies', 'Cryptocurrencies'), 
        ('Music', 'Music'),
        ('Web', 'Web'),
        ('AI', 'AI'),
        ('Conservations', 'Conservations')
    ], validators=[DataRequired()])
    
    content = TextAreaField('Content', validators=[DataRequired()])
    
    tags = StringField('Tags (comma-separated)', validators=[Optional(), Length(max=255)])
    
    read_time = IntegerField('Est. Reading Time (minutes)', validators=[Optional()])
    
    status = SelectField('Status', choices=[
        ('Draft', 'Draft'), 
        ('Published', 'Published')
    ], validators=[DataRequired()])

    meta_description = TextAreaField('Meta Description (for SEO)', validators=[Optional(), Length(max=160)])
    slug = StringField('URL Slug (Optional, will be auto-generated from title)', validators=[Optional(), Length(max=150)])
    
    submit = SubmitField('Save Post')


# --- Routes ---

@admin_bp.route('/manage-blog')
@login_required
def manage_blog():
    """Displays all blog posts in a list."""
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin/blog_management.html', posts=posts)


@admin_bp.route('/blog/add', methods=['GET', 'POST'])
@login_required
def add_blog_post():
    """Handles adding a new blog post."""
    form = BlogPostForm()
    form.thumbnail.validators = [FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')]

    if form.validate_on_submit():
        thumbnail_filename = save_file(form.thumbnail.data, current_app.config['UPLOAD_FOLDER_IMAGE'])
        
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            slug=form.slug.data or slugify(form.title.data),
            content=form.content.data,
            thumbnail_filename=thumbnail_filename,
            category=form.category.data,
            tags=form.tags.data,
            read_time=form.read_time.data,
            status=form.status.data,
            meta_description=form.meta_description.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Blog post has been successfully created!', 'success')
        return redirect(url_for('admin.manage_blog'))

    return render_template('admin/add_edit_blog_post.html', form=form, legend='Add New Blog Post')


@admin_bp.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    """Handles editing an existing blog post."""
    post = BlogPost.query.get_or_404(post_id)
    form = BlogPostForm(obj=post)

    if form.validate_on_submit():
        if form.thumbnail.data:
            delete_file(post.thumbnail_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
            post.thumbnail_filename = save_file(form.thumbnail.data, current_app.config['UPLOAD_FOLDER_IMAGE'])

        post.title = form.title.data
        post.subtitle = form.subtitle.data
        # Only update slug if it's changed, to avoid breaking links.
        new_slug = form.slug.data or slugify(form.title.data)
        if post.slug != new_slug:
            post.slug = new_slug
        post.content = form.content.data
        post.category = form.category.data
        post.tags = form.tags.data
        post.read_time = form.read_time.data
        post.status = form.status.data
        post.meta_description = form.meta_description.data
        
        db.session.commit()
        flash('Blog post has been successfully updated!', 'success')
        return redirect(url_for('admin.manage_blog'))
        
    return render_template('admin/add_edit_blog_post.html', form=form, legend=f'Edit "{post.title}"', post=post)


@admin_bp.route('/blog/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_blog_post(post_id):
    """Handles deleting a blog post and its thumbnail."""
    post = BlogPost.query.get_or_404(post_id)
    
    delete_file(post.thumbnail_filename, current_app.config['UPLOAD_FOLDER_IMAGE'])
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Blog post has been deleted.', 'success')
    return redirect(url_for('admin.manage_blog'))