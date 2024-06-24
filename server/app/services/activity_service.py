# editor : banyanrong
# time : 2024/6/23 16:39
from app.models.model import Activity, db

class ActivityService:
    @staticmethod
    def add_activity(name, description, start_time, end_time, location, link):
        new_activity = Activity(
            name=name,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            link=link
        )
        db.session.add(new_activity)
        db.session.commit()
        return new_activity

    @staticmethod
    def get_activity(activity_id):
        return Activity.query.get(activity_id)

    @staticmethod
    def get_all_activities():
        return Activity.query.all()

    @staticmethod
    def update_activity(activity_id, name, description, start_time, end_time, location, link):
        activity = Activity.query.get(activity_id)
        if activity:
            activity.name = name
            activity.description = description
            activity.start_time = start_time
            activity.end_time = end_time
            activity.location = location
            activity.link = link
            db.session.commit()
        return activity

    @staticmethod
    def delete_activity(activity_id):
        activity = Activity.query.get(activity_id)
        if activity:
            db.session.delete(activity)
            db.session.commit()
        return activity
