from lab6.app.models import Review
from sqlalchemy import desc, asc

class ReviewRepository:
    def __init__(self, db):
        self.db = db

    def get_last_reviews(self, course_id, limit=5):
        return (
            self.db.session.query(Review)
            .filter_by(course_id=course_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_paginated_reviews(self, course_id, sort='newest', page=1):
        query = self.db.select(Review).filter_by(course_id=course_id)

        if sort == 'positive':
            query = query.order_by(Review.rating.desc())
        elif sort == 'negative':
            query = query.order_by(Review.rating.asc())
        else:
            query = query.order_by(Review.created_at.desc())

        return self.db.paginate(query, page=page, per_page=5)

    def get_review_by_user_and_course(self, user_id, course_id):
        return self.db.session.query(Review).filter_by(user_id=user_id, course_id=course_id).first()

    def add_review(self, course, user_id, rating, text):
        review = Review(user_id=user_id, course_id=course.id, rating=rating, text=text)
        course.rating_sum += int(rating)
        course.rating_num += 1

        self.db.session.add(review)
        self.db.session.commit()
        return review
