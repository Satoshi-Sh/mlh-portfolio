# tests/test_app.py

import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html

        # normally beautifulsoup library would better but this works for now
        # get number of img tags and compare to number of 'alt'
        assert html.count("<img") == html.count("alt=")

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Test POST
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
            },
        )
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() != {}
        first_post = response.get_json()

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Frank Obedi",
                "email": "frank@test.com",
                "content": "Hello Satoshi, Just testing you API endpoints!",
            },
        )
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() != {}
        second_post = response.get_json()

        # Test GET endpoint
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        posts = json["timeline_posts"]

        # check if posts were created
        assert first_post in posts
        assert second_post in posts

        # check order of posts
        assert posts[0]["id"] == second_post["id"]
        assert posts[1]["id"] == first_post["id"]

        # Test if there a form on timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # You are using double qoutes on the form id/class names
        # if later you change to single qoute this test would fail (FYI)
        assert '<form id="timeline-form">' in html
        assert '<h2 class="subtitle">Timeline</h2>' in html

    def test_malformed_timeline_post(self):

        # Post request with missing name
        response = self.client.post(
            "api/timeline_post",
            data={"email": "john@example.com", "content": 'Hello World I"m John!'},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # Post request with empty content
        response = self.client.post(
            "api/timeline_post",
            data={"name": "John Doe", "email": "john@example.com", "content": ""},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # Post request with malformed email
        response = self.client.post(
            "api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": 'Hello World I"m John!',
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
