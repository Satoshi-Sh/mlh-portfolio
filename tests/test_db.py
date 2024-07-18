# test_db py

import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

#use an in-memory SQLite for tests
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not neccessary but its good practice to have
        test_db.drop_tables(MODELS)

        # Close DB connection
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello World, I\'m John!')
        assert first_post.id == 1 
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello World, I\'m Jane!')
        assert second_post.id == 2

        # get timeline posts and assert that they are correct
        timeline_posts = [
                model_to_dict(p)
                for p in TimelinePost.select().order_by(TimelinePost.created_at)
        ]

        # assert that first time line post is equal to first time post we created
        assert model_to_dict(first_post) == timeline_posts[0]

        # check that second time line post is equal to second time post we created
        assert model_to_dict(second_post) == timeline_posts[1]

        