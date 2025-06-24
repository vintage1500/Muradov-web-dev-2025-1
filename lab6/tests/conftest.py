import pytest
from datetime import datetime
from app import create_app
from app.models import db, Course, Review
from app.repositories.course_repository import CourseRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository

TEST_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://root:12345678@localhost/lab6',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'TESTING': True,
}

@pytest.fixture(scope='session')
def app():
    app = create_app(TEST_CONFIG)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def db_session(app):
    with app.app_context():
        yield db

@pytest.fixture
def course_repository(db_session):
    return CourseRepository(db_session)

@pytest.fixture
def review_repository(db_session):
    return ReviewRepository(db_session)

@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)

@pytest.fixture
def existing_reviews(course_repository, review_repository, user_repository):
    course = course_repository.get_course_by_id(1)
    if not course:
        course = course_repository.add_course(
            author_id=1,
            name="Тестовый курс",
            category_id=1,
            short_desc="Краткое описание",
            full_desc="Полное описание",
            background_image_id="f1a4ace0-645b-424d-8985-678ac3db897c"
        )
 
    for user_id in range(1, 8):
        user = user_repository.get_user_by_id(user_id)
        if not user:
            from app.models import User
            user = User(id=user_id, login=f"user{user_id}", first_name="Test", last_name=str(user_id))
            user.set_password("123")
            user_repository.db.session.add(user)

    user_repository.db.session.commit()

    # Удалим все отзывы к курсу
    review_repository.db.session.query(Review).filter_by(course_id=course.id).delete()
    review_repository.db.session.commit()

    ratings = [0, 1, 2, 3, 4, 5, 5]
    created = []

    for user_id, rating in zip(range(1, 8), ratings):
        review = review_repository.add_review(course, user_id, rating, f"Отзыв от пользователя {user_id} с оценкой {rating}")
        created.append(review)

    yield created

def parse_reviews_from_html(html_data: str):
    reviews = []
    for part in html_data.split('<div class="card-body">')[1:]:
        try:
            rating = int(part.split('★')[1].split('</h6>')[0].strip())
            date_str = part.split('<h6 class="card-subtitle')[1].split('|')[0].split('>')[1].strip()
            created_at = datetime.strptime(date_str, '%d.%m.%Y')
            reviews.append((rating, created_at))
        except Exception:
            continue
    return reviews
