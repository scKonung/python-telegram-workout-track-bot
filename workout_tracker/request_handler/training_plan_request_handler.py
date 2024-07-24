"""
In this request handler described all functions for training plan configuration

It will need to create the name for this training plan and create exercise plan
"""
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from workout_tracker.db.database import db
from workout_tracker.logger_configuration import configurate_logger
from workout_tracker.models.plan import TrainingPlan

training_plan = {}
logger = configurate_logger()

NAME, DESCRIPTION = range(2)

SELECT, CHOOSE, UPDATE_NAME, UPDATE_DESCRIPTION, UPDATE_EXERCISES = range(5)


def add_training_plan_handlers(application):
    _add_start_handler(application)
    _add_training_plan_conv_handler(application)
    _add_manage_training_plan_handler(application)
    _add_update_training_plan_handler(application)

def _add_start_handler(application):
    application.add_handler(CommandHandler("start", start))

def _add_training_plan_conv_handler(application):
    conv_handler = _create_training_conv_handler()
    application.add_handler(conv_handler)


def _create_training_conv_handler():
    filter = filters.TEXT & ~filters.COMMAND

    conv_handler = ConversationHandler(name="training_plan_creation",
                                       entry_points=[CommandHandler("create_training_plan", create_training_plan),
                                                     MessageHandler(filters.Regex("^(Create Training Plan)$"), create_training_plan)],
                                       states={
                                           NAME: [MessageHandler(filter, training_plan_name), ],
                                           DESCRIPTION: [MessageHandler(filter, training_plan_description),
                                                         CommandHandler("skip",training_plan_description_skip)]
                                       },
                                       fallbacks=[CommandHandler("cancel", cancel)],
                                       )
    return conv_handler

def _add_manage_training_plan_handler(application):
    application.add_handler(CommandHandler("manage", training_plan_manage))

def _add_update_training_plan_handler(application):
    filter = filters.TEXT & ~filters.COMMAND
    conv_handler = ConversationHandler(name="training_plan_update",
                                       entry_points=[CommandHandler("update", select_training_plan_to_update)],
                                       states={
                                           SELECT: [MessageHandler(filter, select_field_to_update), ],
                                           DESCRIPTION: [MessageHandler(filter, training_plan_description),
                                                         CommandHandler("skip", training_plan_description_skip)]
                                       },
                                       fallbacks=[CommandHandler("cancel", cancel)],
                                       )
    application.add_handler(conv_handler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [["Create Training Plan"]]
    logger.info(f"User: {update.message.from_user.username} start use the bot")

    await update.message.reply_text(
        "Hi! My name is Workout Track. I will help you to manage your workouts, so you can see you progress in the gym\n\n"
        "Bot currently in development process, this text will be uptaded later",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),

    )

async def create_training_plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["training_plan"] = TrainingPlan()

    await update.message.reply_text("Sure, we can create for you new training plan\n"
                                    "Please write the name for the new plan")

    return NAME

async def training_plan_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    training_plan: TrainingPlan = context.user_data['training_plan']
    training_plan.name = update.message.text

    await update.message.reply_text("Greate name, now write the description for this plan,"
                                    " if you won't do that, write /skip")

    return DESCRIPTION

async def training_plan_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    training_plan: TrainingPlan = context.user_data['training_plan']
    training_plan.description = update.message.text
    training_plan.user_id = update.message.from_user.id

    _save_training_plan_to_db(training_plan)
    logger.info(f"new training creating for user: {training_plan.user_id}")

    await _reply_summary_training_plan(update, training_plan)

    return ConversationHandler.END

async def training_plan_description_skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    training_plan: TrainingPlan = context.user_data['training_plan']
    training_plan.user_id = update.message.from_user.id

    _save_training_plan_to_db(training_plan)

    logger.info(f"new training creating for user: {training_plan.user_id}")

    await _reply_summary_training_plan(update, training_plan)
    return ConversationHandler.END

def _save_training_plan_to_db(training_plan: TrainingPlan):
    db.add(training_plan)
    db.commit()
    db.refresh(training_plan)
    db.close()

async def _reply_summary_training_plan(update: Update, training_plan: TrainingPlan):
    await update.message.reply_text("Super, you create new training, here is the summarize about this:\n\n"
                                    f"{training_plan.name}\n\n")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "Ok, maybe will in the next time! :)", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


#TODO also need to put here exercise plan, so you can see all information
async def training_plan_manage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    training_plans = db.query(TrainingPlan).filter_by(user_id=user_id).all()

    if training_plans:
        plans_text = "\n".join(
            [f"{plan.id}: {plan.name} - {plan.description or ' '}" for plan in training_plans])
        response_text = f"Here are your training plans:\n{plans_text}"
    else:
        response_text = "You have no training plans yet ;)"

    # Send the response message
    await update.message.reply_text(response_text)

async def select_training_plan_to_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id

    training_plans = db.query(TrainingPlan.name).filter_by(user_id=user_id).all()

    await update.message.reply_text(
        "Sure, please choose training plan, which you want to change: ",
        reply_markup=ReplyKeyboardMarkup(
            training_plans, one_time_keyboard=True
        ),
    )

    return SELECT

async def select_field_to_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    training_plan_name = update.message.text


    training_plans = db.query(TrainingPlan.name).filter_by(user_id=user_id, name=training_plan_name).all()

    await update.message.reply_text(
        "Sure, we will change this traning plan\n"
        "Choose what you want to change",
        reply_markup=ReplyKeyboardMarkup(
            [['Name','Description',"Exercises"]], one_time_keyboard=True
        ),
    )
    return CHOOSE

async def update_training_plan_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

