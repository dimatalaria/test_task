import json

import httpx
from fastapi import APIRouter, HTTPException
from core.schemas.comment import CommentBase

from utils.redis_client import redis_client

router = APIRouter(
    tags=["Users"],
)


async def get_task(task_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'http://api:8001/api/v1/check_task/{task_id}')
            response.raise_for_status()
            print(response.json)
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Задачи не найдены")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Сервер недоступен")

@router.get("/view/comments/{task_id}/")
async def view_comments(task_id: str):
    comment_keys = redis_client.keys(f"comment_{task_id}_*")
    if not comment_keys:
        raise HTTPException(status_code=404, detail="Нету комментариев у задачи с данным ID")

    contents = []
    for key in comment_keys:
        key = key.decode("utf-8") if isinstance(key, bytes) else key
        comment_data = redis_client.get(key)
        if comment_data:
            comment = json.loads(comment_data)
            contents.append(comment.get("content"))

    return {"contents": contents}


@router.post("/comments/")
async def create_comment(comment: CommentBase):
    existing_comments = redis_client.keys(f"comment_{comment.task_id}_*")
    if existing_comments:
        raise HTTPException(status_code=400)
    task = await get_task(comment.task_id)
    if task:
        comment_key = f"comment_{comment.task_id}_{comment.id}"
        redis_client.set(comment_key, comment.model_dump_json())
        redis_client.rpush(f"task_{comment.task_id}_comments", comment_key)
        return {"status": "Комментарий создан"}

    raise HTTPException(status_code=404)


@router.put("/comments/{task_id}/")
async def update_comment(task_id: str, updated_data: dict):
    comment_keys = redis_client.keys(f"comment_{task_id}_*")
    if not comment_keys:
        raise HTTPException(status_code=404)

    comment_key = comment_keys[0]
    comment_data = json.loads(redis_client.get(comment_key))

    comment_data["content"] = updated_data.get("content")
    redis_client.set(comment_key, json.dumps(comment_data))

    return {"status": "Комментарий обновлён"}


@router.delete("/delete/comments/{task_id}/")
async def delete_comments_by_task(task_id: str):
    comment_keys = redis_client.keys(f"comment_{task_id}_*")
    if not comment_keys:
        raise HTTPException(status_code=404, detail="Комментарии к данному task_id не найдены")
    for key in comment_keys:
        redis_client.delete(key)
    redis_client.delete(f"task_{task_id}_comments")

    return {"status": "Комментарии удалены"}