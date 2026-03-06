from sqlalchemy import select

from models import task_model as models
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task_schema import taskCreate, taskUpdate 
from fastapi import HTTPException
from models.user_model import User

# Here we will define all the functions that will interact WITHIN database and perform CRUD operations

# creating tasks
async def create_task(db: AsyncSession, task: taskCreate, current_user: User):
    #db_task is the task to be added in db
    db_task = models.Task(title=task.title ,
                        description=task.description , 
                        user_id=current_user.id) # THIS LINE WAS THE CORE IDEA!
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

#getting all tasks
async def get_tasks(db: AsyncSession, current_user: User): #
    tasks = await db.execute(select(models.Task).where(models.Task.user_id == current_user.id))
    tasks = tasks.scalars().all() # scalars() is used to get the actual task objects from the result.
    return tasks

#getting single task
async def get_task(db: AsyncSession,task_id: int , current_user: User ):
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none() # this make sure that we get only one task or None if no/more than 1 task is found.
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task

#deleting single task
async def delete_task(db: AsyncSession, task_id: int):
    task = await db.execute(select(models.Task).where(models.Task.id == task_id))
    task = task.scalar_one_or_none()
    if task:
        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted"}
    return {"message": "Task not found"}

#updating single task
async def update_task(db: AsyncSession, task_id: int, current_user: User, task_update : taskUpdate):
    task = await db.execute(select(models.Task).where(models.Task.id == task_id, models.Task.user_id == current_user.id))
    # ethe we checked task id de whihc ki same user id hai na.
    task = task.scalar_one_or_none()
    if task is None:
       raise HTTPException(status_code=404, detail="Task not found")
    
    # jehri request ayi hai us wich koi field update karni hai usnu check karange and update karange
    if task_update.title is not None:
        task.title = task_update.title

    if task_update.description is not None:
        task.description = task_update.description

    if task_update.completed is not None:
        task.completed = task_update.completed
    
    await db.commit()
    await db.refresh(task)
    return task
