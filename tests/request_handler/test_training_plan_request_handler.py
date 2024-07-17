import pytest
from unittest.mock import Mock, patch
from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler
from workout_tracker.request_handler.training_plan_request_handler import (start,
                                                                           create_training_plan,
                                                                           training_plan_name,
                                                                           training_plan_description)
from workout_tracker.models.plan import TrainingPlan
from workout_tracker.db.database import db

USER_ID = 12345
MESSAGE_TEXT = "Some message"


@pytest.fixture
def mock_update() -> Mock:
    # Create a mock Update object
    mock_update = Mock(spec=Update)
    # Mock the message attribute of Update
    mock_message = Mock(spec=Message)

    mock_message.text = MESSAGE_TEXT
    mock_message.from_user.username = "testuser"  # Set the username
    mock_message.from_user.id = USER_ID

    mock_update.message = mock_message
    return mock_update

@pytest.fixture
def mock_context() -> Mock:
    # Create a mock Context object
    mock_context = Mock(spec=CallbackContext)
    mock_context.user_data = {}
    return mock_context

@pytest.fixture
def mock_training_plan() -> Mock:
    return Mock(spec=TrainingPlan)

@pytest.fixture
def mock_context_with_training_plan(mock_context, mock_training_plan) -> Mock:
    mock_context.user_data['training_plan'] = mock_training_plan

    return mock_context



@pytest.mark.asyncio
async def test_start_return_reply_when_triggered(mock_update, mock_context):
    await start(mock_update, mock_context)

    mock_update.message.reply_text.assert_called_once_with(
        "Hi! My name is Workout Track. I will help you to manage your workouts, so you can see you progress in the gym\n\n"
        "Bot currently in development proccess, this text will be uptaded later"
    )

@pytest.mark.asyncio
async def test_create_training_plan_return_zero_when_triggered(mock_update, mock_context):

    stage_number = await create_training_plan(mock_update, mock_context)

    assert stage_number == 0

@pytest.mark.asyncio
async def test_create_training_plan_create_user_data_training_plan_when_triggered(mock_training_plan, mock_update,
                                                                                  mock_context):
    await create_training_plan(mock_update, mock_context)

    assert 'training_plan' in mock_context.user_data
    assert isinstance(mock_context.user_data['training_plan'], TrainingPlan)

@pytest.mark.asyncio
async def test_training_plan_name_return_one_when_triggered(mock_update,
                                                            mock_context_with_training_plan, mock_training_plan):
    stage_number = await training_plan_name(mock_update,mock_context_with_training_plan)

    assert stage_number == 1

@pytest.mark.asyncio
async def test_training_plan_name_change_user_data_when_triggered(mock_update,
                                                                  mock_context_with_training_plan, mock_training_plan):
    await training_plan_name(mock_update, mock_context_with_training_plan)

    assert mock_training_plan.name ==  mock_update.message.text


@pytest.mark.asyncio
async def test_training_plan_description_user_id_added_to_training_plan(mock_update,
                                                                        mock_context_with_training_plan,
                                                                        mock_training_plan):
    mock_db_functions()

    # Call the function
    await training_plan_description(mock_update, mock_context_with_training_plan)

    # Assert that the user_id attribute of mock_training_plan matches USER_ID
    assert mock_training_plan.user_id == mock_update.message.from_user.id


@pytest.mark.asyncio
async def test_training_plan_description_description_added_to_training_plan(mock_update,
                                                                        mock_context_with_training_plan,
                                                                        mock_training_plan):
    mock_db_functions()

    # Call the function
    await training_plan_description(mock_update, mock_context_with_training_plan)

    # Assert that the user_id attribute of mock_training_plan matches USER_ID
    assert mock_training_plan.description == mock_update.message.text


@pytest.mark.asyncio
async def test_training_plan_description_add_record_to_database_when_safe_training_plan(mock_update,
                                                                                        mock_context_with_training_plan,mock_training_plan):
    mock_db_functions()

    # Call the function
    await training_plan_description(mock_update, mock_context_with_training_plan)

    # Assert database methods are called
    db.add.assert_called_once_with(mock_training_plan)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(mock_training_plan)
    db.close.assert_called_once()



@pytest.mark.asyncio
async def test_training_plan_description_return_END_when_triggered(mock_update,
                                                                   mock_context_with_training_plan, mock_training_plan):
    mock_db_functions()

    # Call the function
    result = await training_plan_description(mock_update, mock_context_with_training_plan)

    # Assert the correct return value
    assert result == ConversationHandler.END

def mock_db_functions():
    db.add = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    db.close = Mock()
