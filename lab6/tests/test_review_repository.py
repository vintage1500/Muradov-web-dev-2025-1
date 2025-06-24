from conftest import parse_reviews_from_html
import random

def test_review_list_content(existing_reviews, review_repository):
    course_id = existing_reviews[0].course_id
    reviews = review_repository.get_last_reviews(course_id, limit=10)
    assert len(reviews) == 7

    texts = [r.text for r in reviews]
    for i in range(1, 8):
        assert f"Отзыв от пользователя {i}" in texts[i - 1] or any(f"Отзыв от пользователя {i}" in t for t in texts)

def test_latest_review_limit(review_repository, existing_reviews):
    course_id = existing_reviews[0].course_id
    limited_reviews = review_repository.get_last_reviews(course_id)
    assert len(limited_reviews) == 5

    sorted_reviews = sorted(existing_reviews, key=lambda r: r.created_at, reverse=True)
    assert [r.id for r in limited_reviews] == [r.id for r in sorted_reviews[:5]]

def test_get_user_review(review_repository, existing_reviews):
    r = random.choice(existing_reviews)
    found = review_repository.get_review_by_user_and_course(r.user_id, r.course_id)
    assert found is not None
    assert found.id == r.id

def test_sort_newest(client, existing_reviews):
    course_id = existing_reviews[0].course_id
    response = client.get(f'/courses/{course_id}/reviews?sort=newest')
    assert response.status_code == 200
    reviews = parse_reviews_from_html(response.data.decode())
    dates = [r[1] for r in reviews]
    assert dates == sorted(dates, reverse=True)

def test_sort_positive_html(client, existing_reviews):
    course_id = existing_reviews[0].course_id
    response = client.get(f'/courses/{course_id}/reviews?sort=positive')
    assert response.status_code == 200
    reviews = parse_reviews_from_html(response.data.decode())
    ratings = [r[0] for r in reviews]
    assert ratings == sorted(ratings, reverse=True)

def test_sort_negative_html(client, existing_reviews):
    course_id = existing_reviews[0].course_id
    response = client.get(f'/courses/{course_id}/reviews?sort=negative')
    assert response.status_code == 200
    reviews = parse_reviews_from_html(response.data.decode())
    ratings = [r[0] for r in reviews]
    assert ratings == sorted(ratings)

def test_review_pagination(client, existing_reviews):
    course_id = existing_reviews[0].course_id

    # страница 1
    response_1 = client.get(f'/courses/{course_id}/reviews')
    assert response_1.status_code == 200
    reviews_1 = parse_reviews_from_html(response_1.data.decode("utf-8"))
    assert len(reviews_1) == 5  # первая страница — 5 отзывов

    # страница 2
    response_2 = client.get(f'/courses/{course_id}/reviews?page=2')
    assert response_2.status_code == 200
    reviews_2 = parse_reviews_from_html(response_2.data.decode("utf-8"))
    assert len(reviews_2) == len(existing_reviews) - 5  # остальные отзывы (2 из 7)