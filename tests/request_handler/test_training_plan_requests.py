import pytest
from unittest.mock import Mock, patch
from telegram import Update, Message
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters, Application
from workout_tracker.request_handler.training_plan_request_handler import (start,
                                                                           create_training_plan,
                                                                           training_plan_name,
                                                                           training_plan_description,
                                                                           training_plan_description_skip)
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

def mock_db_functions():
    db.add = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    db.close = Mock()

@pytest.fixture
def mock_context_with_training_plan(mock_context, mock_training_plan) -> Mock:
    mock_context.user_data['training_plan'] = mock_training_plan

    return mock_context


class TestStartCommand:
    @pytest.mark.asyncio
    async def test_reply_to_user(self,mock_update, mock_context):
        await start(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()

class TestCreateTrainingPlanCommand:
    @pytest.mark.asyncio
    async def test_stage_number_zero(self,mock_update, mock_context):

        stage_number = await create_training_plan(mock_update, mock_context)

        assert stage_number == 0

    @pytest.mark.asyncio
    async def test_add_object_to_user_data(self,mock_training_plan,
                                        mock_update, mock_context):
        await create_training_plan(mock_update, mock_context)

        assert 'training_plan' in mock_context.user_data

    @pytest.mark.asyncio
    async def test_reply_to_user(self,mock_update, mock_context):
        await create_training_plan(mock_update, mock_context)

        mock_update.message.reply_text.assert_called_once()

class TestNameStage:
    @pytest.mark.asyncio
    async def test_stage_number_one(self,mock_update,
                                    mock_context_with_training_plan, mock_training_plan):
        stage_number = await training_plan_name(mock_update,mock_context_with_training_plan)

        assert stage_number == 1

    @pytest.mark.asyncio
    async def test_user_text_added_to_user_data(self,mock_update,
                                                mock_context_with_training_plan, mock_training_plan):
        await training_plan_name(mock_update, mock_context_with_training_plan)

        assert mock_training_plan.name ==  mock_update.message.text

    @pytest.mark.asyncio
    async def test_reply_to_user(self,mock_update, mock_context_with_training_plan):
        await training_plan_name(mock_update, mock_context_with_training_plan)
        mock_update.message.reply_text.assert_called_once()


class TestDescriptionStage:
    @pytest.mark.asyncio
    async def test_user_id_added_to_user_data(self, mock_update,
                                    mock_context_with_training_plan, mock_training_plan):
        mock_db_functions()

        await training_plan_description(mock_update, mock_context_with_training_plan)

        assert mock_training_plan.user_id == mock_update.message.from_user.id


    @pytest.mark.asyncio
    async def test_description_added_to_user_data(self,mock_update,
                                            mock_context_with_training_plan, mock_training_plan):
        mock_db_functions()

        await training_plan_description(mock_update, mock_context_with_training_plan)

        assert mock_training_plan.description == mock_update.message.text


    @pytest.mark.asyncio
    async def test_stage_END(self,mock_update,
                            mock_context_with_training_plan, mock_training_plan):
        mock_db_functions()

        result = await training_plan_description(mock_update, mock_context_with_training_plan)

        assert result == ConversationHandler.END

    @pytest.mark.asyncio
    async def test_reply_to_user(self,mock_update, mock_context_with_training_plan):
        await training_plan_description(mock_update, mock_context_with_training_plan)
        mock_update.message.reply_text.assert_called_once()

class TestDescriptionSkipCommand:
    @pytest.mark.asyncio
    async def test_reply_to_user(self, mock_update, mock_context_with_training_plan):
        await training_plan_description_skip(mock_update, mock_context_with_training_plan)
        mock_update.message.reply_text.assert_called_once()