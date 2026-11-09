def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Sign In' in response.data


def test_login_with_details_redirects_home(client):
    response = client.post('/login', data={'username': 'jane', 'password': 'secret'})
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/index')


def test_login_empty_fields_show_errors(client):
    response = client.post('/login', data={'username': '', 'password': ''})
    assert response.status_code == 200
    assert b'This field is required.' in response.data


def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_register_passwords_must_match(client):
    response = client.post('/register', data={
        'username': 'jane', 'email': 'jane@example.com',
        'password': 'one', 'password2': 'two'})
    assert response.status_code == 200
    assert b'Field must be equal to password.' in response.data
