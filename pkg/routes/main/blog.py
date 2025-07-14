from flask import render_template, abort
from . import main_bp
from pkg.models import BlogPost

# A mapping for category colors and data attributes
BLOG_CATEGORIES = {
    'Use Cases': {'color': 'blue', 'icon': 'fas fa-briefcase'},
    'Cryptocurrencies': {'color': 'yellow', 'icon': 'fab fa-bitcoin'},
    'Music': {'color': 'purple', 'icon': 'fas fa-music'},
    'Web': {'color': 'green', 'icon': 'fas fa-globe'},
    'AI': {'color': 'teal', 'icon': 'fas fa-robot'},
    'Conservations': {'color': 'orange', 'icon': 'fas fa-leaf'}
}

@main_bp.route('/blog')
def blog_index():
    """Shows the main blog page with all published posts."""
    posts = BlogPost.query.filter_by(status='Published').order_by(BlogPost.date_posted.desc()).all()
    return render_template('main/blog.html', posts=posts, categories=BLOG_CATEGORIES)


@main_bp.route('/blog/<slug>')
def blog_post(slug):
    """Shows a single blog post."""
    post = BlogPost.query.filter_by(slug=slug, status='Published').first_or_404()
    
    # Get related articles (same category, not the current one)
    related_posts = BlogPost.query.filter(
        BlogPost.category == post.category,
        BlogPost.id != post.id,
        BlogPost.status == 'Published'
    ).order_by(BlogPost.date_posted.desc()).limit(3).all()

    return render_template('main/blog_page.html', post=post, related_posts=related_posts, categories=BLOG_CATEGORIES)