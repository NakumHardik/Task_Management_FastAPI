from src.task.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.task.models import taskModel
from fastapi import HTTPException, status
from src.user.models import UserModel


def create_task(body: TaskSchema, db: Session, user: UserModel):
    new_task = taskModel(**body.model_dump(), user_id=user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_task(db: Session, user: UserModel):
    tasks = db.query(taskModel).filter(taskModel.user_id == user.id).all()
    return tasks


def get_one_task(task_id: int, db: Session, user: UserModel):
    one_task = db.get(taskModel, task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID is incorrect")

    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to view this task")

    return one_task


def update_task(body: TaskSchema, task_id: int, db: Session, user: UserModel):
    one_task = db.get(taskModel, task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID is incorrect")

    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this task")

    body_dict = body.model_dump(exclude_unset=True)
    for field, value in body_dict.items():
        setattr(one_task, field, value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id: int, db: Session, user: UserModel):
    one_task = db.get(taskModel, task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task ID is incorrect")

    if one_task.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this task")

    db.delete(one_task)
    db.commit()

    return None
