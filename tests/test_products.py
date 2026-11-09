def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'My Vault Collection' in response.data


def test_about_page_loads(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About PaletteVault' in response.data


def test_unknown_page_returns_404(client):
    response = client.get('/does-not-exist')
    assert response.status_code == 404


def test_home_page_lists_products_from_routes(client):
    response = client.get('/')
    assert b'Radiant Creamy Concealer' in response.data
    assert b'Gloss Bomb Universal Luminiser' in response.data
