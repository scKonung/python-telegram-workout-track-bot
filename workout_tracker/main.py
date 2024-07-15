from workout_tracker.db.database import init_db
from workout_tracker.request_handler.plan_request_handler import main

if __name__ == '__main__':
    init_db()
    main()