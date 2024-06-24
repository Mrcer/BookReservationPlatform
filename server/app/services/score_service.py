# editor : banyanrong
# time : 2024/6/23 0:04
from app.models.model import Score, db

class ScoreService:
    @staticmethod
    def add_score(user_id, points, description):
        new_score = Score(user_id=user_id, points=points, description=description)
        db.session.add(new_score)
        db.session.commit()
        return new_score

    @staticmethod
    def get_scores_by_user(user_id):
        return Score.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_scores():
        return Score.query.all()

    @staticmethod
    def update_score(score_id, points, description):
        score = Score.query.get(score_id)
        if score:
            score.points = points
            score.description = description
            db.session.commit()
        return score

    @staticmethod
    def delete_score(score_id):
        score = Score.query.get(score_id)
        if score:
            db.session.delete(score)
            db.session.commit()
        return score
