import pytest
from flask import url_for
from app import app, posts_list


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_page_status_code(client):
    response = client.get(url_for('index'))
    assert response.status_code == 200

def test_index_page_html(client):
    response = client.get(url_for('index')) 
    assert b'<!doctype html>' in response.data

def test_about_page_status_code(client):
    response = client.get(url_for('about'))
    assert response.status_code == 200 

def test_about_page_html(client):
    response = client.get(url_for('about')) 
    assert b'<!doctype html>' in response.data

def test_about_page_html_tag(client):
    response = client.get(url_for('about')) 
    response_text = response.data.decode('utf-8').strip()
    assert '<h1 class="mt-5 text-center">Об авторе</h1>' in response_text

def test_posts_page_status_code(client):
    response = client.get(url_for('posts'))
    assert response.status_code == 200  

def test_posts_page_html(client):
    response = client.get(url_for('posts')) 
    assert b'<!doctype html>' in response.data

def test_posts_page_html_tag(client):
    response = client.get(url_for('posts')) 
    response_text = response.data.decode('utf-8').strip()
    assert '<h1 class="my-5">Последние посты</h1>' in response_text

def test_post_page_status_code(client):
    response = client.get(url_for('post', index=0))
    assert response.status_code == 200

def test_post_page_html(client):
    response = client.get(url_for('post', index=0))
    assert b'<!doctype html>' in response.data

def test_page_post_comment_title(client): 
    response = client.get(url_for('post', index=1)) 
    response_text = response.data.decode('utf-8').strip()
    assert 'Оставьте комментарий' in response_text

def test_posts_page_title(client):
    response = client.get(url_for('posts'))
    for post in posts_list():
        assert post['title'].encode() in response.data

def test_post_page_data(client):
    post = posts_list()[0]
    response = client.get(url_for('post', index=0)) 
    assert post['title'].encode() in response.data
    assert post['text'][:50].encode() in response.data
    assert post['author'].encode() in response.data

def test_non_existent_post(client):
    response = client.get(url_for('post', index=999))
    assert response.status_code == 404

def test_post_image_loading(client):
    post = posts_list()[0]
    response = client.get(url_for('post', index=0)) 
    assert f'src="{url_for("static", filename="images/" + post["image_id"])}"'.encode() in response.data

def test_redirect_on_invalid_url(client):
    response = client.get('/some_invalid_url')
    assert response.status_code == 404  

def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.data.decode("utf-8")

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

def test_posts_index_data(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        context = templates[0]
        assert 'posts' in context   
        assert isinstance(context['posts'], list)  
        assert len(context['posts']) == len(posts_list)
        expected_post = posts_list[0]
        actual_post = context['posts'][0]
        assert actual_post['author'] == expected_post['author']
        assert actual_post['text'] == expected_post['text']
        assert actual_post['date'] == expected_post['date']
        assert actual_post['image_id'] == expected_post['image_id']
