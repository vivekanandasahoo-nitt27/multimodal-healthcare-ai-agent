from database import SessionLocal, HealthMetric


def save_metric(user_id, name, value):

    db = SessionLocal()

    metric = HealthMetric(
        user_id=user_id,
        metric_name=name,
        value=str(value)
    )

    db.add(metric)
    db.commit()
    db.close()


def get_metric_history(user_id, name):

    db = SessionLocal()

    rows = db.query(HealthMetric).filter(
        HealthMetric.user_id == user_id,
        HealthMetric.metric_name == name
    ).all()

    db.close()

    return rows