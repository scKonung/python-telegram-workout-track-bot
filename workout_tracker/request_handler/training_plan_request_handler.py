"""
In this request handler described all functions for training plan configuration

It will need to create the name for this training plan and create exercise plan
"""
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from workout_tracker.db.database import db
from workout_tracker.logger_configuration import configurate_logger
from workout_tracker.constans import BOT_TOKEN
from workout_tracker.models.plan import TrainingPlan

training_plan = {}
logger = configurate_logger()

NAME, DESCRIPTION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"User: {update.message.from_user.username} start use the bot")

    await update.message.reply_text(
        "Hi! My name is Workout Track. I will help you to manage your workouts, so you can see you progress in the gym\n\n"
        "Bot currently in development proccess, this text will be uptaded later"
    )



async def create_training_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int :
    context.user_data["training_plan"] = TrainingPlan()

    await update.message.reply_text("Sure, we can create for you new training plan\n"
                                    "Please write the name for the new plan")

    return NAME

async def training_plan_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    training_plan: TrainingPlan = context.user_data['training_plan']
    training_plan.name = update.message.text

    await update.message.reply_text("Greate name, now write the description for this plan,"
                                    " if you won't do that, write /cancel")

    return DESCRIPTION

async def training_plan_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    training_plan: TrainingPlan = context.user_data['training_plan']
    training_plan.description = update.message.text
    training_plan.user_id = update.message.from_user.id

    # Save the training plan to the database
    db.add(training_plan)
    db.commit()
    db.refresh(training_plan)
    db.close()

    logger.info(f"new training creating for user: {training_plan.user_id}")

    await update.message.reply_text("Super, you create new training, here is the summarize about this:\n\n"
                                    f"{training_plan.name}\n\n"
                                   f"{training_plan.description}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    await update.message.reply_text(
        "Ok, maybe will in the next time! :)", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def add_training_plan_handlers(application) -> Application:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create_training_plan", create_training_plan)],
        states={
            NAME: [MessageHandler(filters.TEXT, training_plan_name)],
            DESCRIPTION: [MessageHandler(filters.TEXT, training_plan_description)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],

    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    application.add_handler(CommandHandler("start",start))



    application.add_handler(conv_handler)

    return application