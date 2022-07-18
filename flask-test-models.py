from unittest import TestCase

from app import app
from models import db, User, DEFAULT_PIC_URL
from flask import session
# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
db.drop_all()
db.create_all()


class UserAccount(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled commit() transaction."""

        db.session.rollback()

    def test_greet(self):
        user = User(first_name="Quinten", last_name="Tarantino", image_url=DEFAULT_PIC_URL)
        self.assertEqual(User.greet(), f"Hello There. I'm Quinten Tarantino")
    def test_root(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://127.0.0.1:5000")
    
    def test_user_page(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>All Users</h1>', html)
    
    def test_new_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            
    def test_new_user_submit(self):
        with app.test_client() as client:
            resp = client.post('/users/new', data={'first_name': 'Justin'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{1}")
            user = User.query.get_or_404(1)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(user.id, 1)
            
    def test_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1/edit")
            user = User.query.get_or_404(1)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(user.id, 1)
            self.assertEqual('<input type="text" class="form-control" id="first_name" name="first_name" value="{{user.first_name}}">', html)
    def test_edit_submit(self):
        with app.test_client() as client:
            resp = client.post(f"/users/1/edit", data={'first_name': 'Justin'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 302)
            self.assertIn('Justin', html)

    def test_delete(self):
        with app.test_client() as client:
            resp = client.post(f"/users/1/edit", data={'first_name': 'Justin'})
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Justin', html)
    