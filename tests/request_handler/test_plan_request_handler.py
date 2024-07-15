import pytest
from unittest.mock import Mock
from telegram import Update, Message
from telegram.ext import CallbackContext
from workout_tracker.request_handler.plan_request_handler import start

@pytest.fixture
def update():
    # Create a mock Update object
    mock_update = Mock(spec=Update)
    # Mock the message attribute of Update
    mock_message = Mock(spec=Message)
    mock_message.from_user.username = "testuser"  # Set the username
    mock_update.message = mock_message
    return mock_update

@pytest.fixture
def context():
    # Create a mock Context object
    mock_context = Mock(spec=CallbackContext)
    return mock_context

def test_start(update, context):
    # Call your start function with the mocked update and context
    start(update, context)

    # Assert that the reply_text method was called with the expected text
    update.message.reply_text.assert_called_once_with(
        "Hi! My name is Workout Track. I will help you to manage your workouts, so you can see you progress in the gym\n\n"
        "Bot currently in development proccess, this text will be uptaded later"
    )
