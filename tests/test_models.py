import pytest

from app.models.event import Comment, Subscription, Event


# Assuming the classes Event, Comment, and Subscription are imported here.
# If the classes are in a file named `test_models.py`, you can import them like this:
# from models import Event, Comment, Subscription

# Test for the Comment class
def test_comment_creation():
    comment = Comment(1, "This is a comment", "user1")

    assert comment.get_comment() == "This is a comment"
    assert comment.get_username() == "user1"


# Test for the Subscription class
def test_subscription_creation():
    subscription = Subscription(1, "user1")

    assert subscription.get_username() == "user1"


# Test for the Event class
@pytest.fixture
def event_with_no_subscriptions_and_comments():
    # Fixture to create an Event with no subscriptions or comments
    return Event(1, "owner", "Event Title", "Event Title Short", "Event Description")


def test_event_creation(event_with_no_subscriptions_and_comments):
    event = event_with_no_subscriptions_and_comments

    assert event.get_id() == 1
    assert event.get_title() == "Event Title"
    assert event.get_title_short() == "Event Title Short"
    assert event.get_description() == "Event Description"
    assert event.get_owner_username() == "owner"
    assert event.get_subscriptions() == ''
    assert event.get_comments() == []


def test_event_has_comments(event_with_no_subscriptions_and_comments):
    event = event_with_no_subscriptions_and_comments

    # Test the has_comments method
    assert event.has_comments() is False


def test_event_has_subscriptions(event_with_no_subscriptions_and_comments):
    event = event_with_no_subscriptions_and_comments

    # Test the has_subscriptions method
    assert event.has_subscriptions() is False


# Test event with subscriptions and comments
@pytest.fixture
def event_with_subscriptions_and_comments():
    comment1 = Comment(1, "Great event!", "user1")
    comment2 = Comment(2, "Looking forward to it!", "user2")
    subscription1 = Subscription(1, "user1")
    subscription2 = Subscription(2, "user2")

    event = Event(
        1,
        "owner",
        "Event Title",
        "Event Title Short",
        "Event Description",
        subscriptions=[subscription1, subscription2],
        comments=[comment1, comment2]
    )
    return event


def test_event_with_subscriptions_and_comments(event_with_subscriptions_and_comments):
    event = event_with_subscriptions_and_comments

    # Test the subscriptions
    assert event.get_subscriptions() == "user1, user2"

    # Test the comments
    assert len(event.get_comments()) == 2
    assert event.get_comments()[0].get_comment() == "Great event!"
    assert event.get_comments()[1].get_comment() == "Looking forward to it!"

    # Test the has_comments and has_subscriptions methods
    assert event.has_comments() is True
    assert event.has_subscriptions() is True
