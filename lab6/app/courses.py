from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from lab6.app.models import db
from lab6.app.repositories import CourseRepository, UserRepository, CategoryRepository, ImageRepository, ReviewRepository

user_repository = UserRepository(db)
course_repository = CourseRepository(db)
category_repository = CategoryRepository(db)
image_repository = ImageRepository(db)

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    pagination = course_repository.get_pagination_info(**search_params())
    courses = course_repository.get_all_courses(pagination=pagination)
    categories = category_repository.get_all_categories()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = course_repository.new_course()
    categories = category_repository.get_all_categories()
    users = user_repository.get_all_users()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = None

    try:
        if f and f.filename:
            img = image_repository.add_image(f)

        image_id = img.id if img else None
        course = course_repository.add_course(**params(), background_image_id=image_id)
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        categories = category_repository.get_all_categories()
        users = user_repository.get_all_users()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)
    review_repository = ReviewRepository(db)
    last_reviews = review_repository.get_last_reviews(course_id)
    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_review_by_user_and_course(current_user.id, course_id)

    return render_template('courses/show.html',
                           course=course,
                           reviews=last_reviews,
                           user_review=user_review)

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)

    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)

    review_repository = ReviewRepository(db)
    pagination = review_repository.get_paginated_reviews(course_id, sort=sort, page=page)
    reviews = pagination.items

    user_review = None
    if current_user.is_authenticated:
        user_review = review_repository.get_review_by_user_and_course(current_user.id, course_id)

    return render_template('courses/review.html',
                           course=course,
                           reviews=reviews,
                           pagination=pagination,
                           sort=sort,
                           user_review=user_review)


@bp.route('/<int:course_id>/reviews', methods=['POST'])
@login_required
def create_review(course_id):
    course = course_repository.get_course_by_id(course_id)
    if not course:
        abort(404)

    review_repository = ReviewRepository(db)
    existing = review_repository.get_review_by_user_and_course(current_user.id, course_id)
    if existing:
        flash('Вы уже оставили отзыв на этот курс.', 'warning')
        return redirect(url_for('courses.show', course_id=course_id))

    rating = request.form.get('rating', type=int)
    text = request.form.get('text')

    review_repository.add_review(course, current_user.id, rating, text)
    flash('Ваш отзыв успешно добавлен!', 'success')

    return redirect(url_for('courses.show', course_id=course_id))
