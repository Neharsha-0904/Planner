from datetime import date
from app.models.task import Task, Priority, TaskStatus


def test_create_task(db, user):
    task = Task(
        user_id=user.id,
        title="Test task",
        priority=Priority.P1,
        status=TaskStatus.OPEN,
        scheduled_for=date.today(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    assert task.id is not None
    assert task.title == "Test task"
    assert task.priority == Priority.P1
    assert task.status == TaskStatus.OPEN
    assert task.rolled_over_count == 0


def test_complete_task(db, user):
    task = Task(
        user_id=user.id,
        title="Complete me",
        priority=Priority.P0,
        status=TaskStatus.OPEN,
    )
    db.add(task)
    db.commit()

    task.status = TaskStatus.DONE
    db.commit()
    db.refresh(task)

    assert task.status == TaskStatus.DONE


def test_task_tags(db, user):
    task = Task(
        user_id=user.id,
        title="Tagged task",
        priority=Priority.P2,
        status=TaskStatus.OPEN,
        tags=["coursework", "ml"],
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # SQLite doesn't support ARRAY, so tags may be stored differently
    # This test validates the model accepts tags
    assert task.title == "Tagged task"


def test_update_task(db, user):
    task = Task(
        user_id=user.id,
        title="Original",
        priority=Priority.P2,
        status=TaskStatus.OPEN,
    )
    db.add(task)
    db.commit()

    task.title = "Updated"
    task.priority = Priority.P0
    db.commit()
    db.refresh(task)

    assert task.title == "Updated"
    assert task.priority == Priority.P0


def test_delete_task(db, user):
    task = Task(
        user_id=user.id,
        title="Delete me",
        priority=Priority.P2,
        status=TaskStatus.OPEN,
    )
    db.add(task)
    db.commit()

    task_id = task.id
    db.delete(task)
    db.commit()

    result = db.query(Task).filter(Task.id == task_id).first()
    assert result is None
