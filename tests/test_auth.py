from app import User


def test_default_hr_user_is_created_with_a_werkzeug_hash(client, app):
    response = client.get('/login')

    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='hr').first()
        assert user is not None
        assert user.password_hash != 'hr123'
        assert user.check_password('hr123')


def test_login_rejects_invalid_and_missing_passwords(client):
    for password in ('incorrect', ''):
        response = client.post(
            '/login',
            data={'username': 'hr', 'password': password},
        )

        assert response.status_code == 200
        assert b'Invalid username or password' in response.data


def test_login_redirects_to_dashboard_and_logout_clears_session(client):
    response = client.post(
        '/login',
        data={'username': 'hr', 'password': 'hr123'},
    )

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')
    assert client.get('/').status_code == 200

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')
    assert client.get('/').status_code == 302


def test_protected_pages_require_login(client):
    for path in ('/', '/resume', '/performance', '/analytics'):
        response = client.get(path)

        assert response.status_code == 302
        assert '/login' in response.headers['Location']


def test_login_rejects_external_next_redirect(client):
    response = client.post(
        '/login?next=https://example.com/',
        data={'username': 'hr', 'password': 'hr123'},
    )

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/')


def test_password_change_cli_updates_werkzeug_hash(runner, app):
    result = runner.invoke(
        args=['set-user-password', 'hr'],
        input='new-test-password\nnew-test-password\n',
    )

    assert result.exit_code == 0
    with app.app_context():
        user = User.query.filter_by(username='hr').first()
        assert user is not None
        assert user.check_password('new-test-password')
