import pytest
from unittest.mock import Mock, patch
from telegram import Update, Message
from telegram.ext import CallbackContext
from workout_tracker.request_handler.plan_request_handler import start, create_training_plan, training_plan_name
from workout_tracker.models.plan import TrainingPlan

@pytest.fixture
def mock_update() -> Mock:
    # Create a mock Update object
    mock_update = Mock(spec=Update)
    # Mock the message attribute of Update
    mock_message = Mock(spec=Message)

    mock_message.text = "Some text"
    mock_message.from_user.username = "testuser"  # Set the username

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
async def test_training_plan_name_return_one_when_triggered(mock_update, mock_context_with_training_plan, mock_training_plan):
    stage_number = await training_plan_name(mock_update,mock_context_with_training_plan)

    assert stage_number == 1

@pytest.mark.asyncio
async def test_training_plan_name_change_user_data_when_triggered(mock_update, mock_context_with_training_plan, mock_training_plan):
    await training_plan_name(mock_update, mock_context_with_training_plan)

    assert mock_context_with_training_plan.user_data['training_plan'].name == mock_update.message.text
