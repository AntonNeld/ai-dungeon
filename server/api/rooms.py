from typing import List

from fastapi import APIRouter, HTTPException

from dungeon.room import room_from_dict
from models import Room


def rooms_routes(dungeon, template_keeper):

    router = APIRouter()

    @router.get("/rooms", response_model=List[str])
    async def list_rooms():
        return dungeon.list_rooms()

    @router.post("/rooms", response_model=str)
    async def create_room(room: Room = None, from_template: str = None):
        if from_template:
            room_obj = template_keeper.create_room(from_template)
        elif room:
            room_obj = room_from_dict(room.dict())
        else:
            raise HTTPException(status_code=422, detail="Unprocessable entity")
        return dungeon.add_room(room_obj)

    @router.get("/rooms/{room_id}", response_model=Room)
    async def get_room(room_id: str):
        return dungeon.get_room(room_id).to_dict()

    @router.put("/rooms/{room_id}", response_model=str)
    async def create_room_with_id(room_id: str,
                                  room: Room = None,
                                  from_template: str = None):
        if from_template:
            room_obj = template_keeper.create_room(from_template)
        elif room:
            room_obj = room_from_dict(room.dict())
        else:
            raise HTTPException(status_code=422, detail="Unprocessable entity")
        return dungeon.add_room(room_obj, room_id=room_id)

    @router.delete("/rooms/{room_id}")
    async def delete_room(room_id: str):
        return dungeon.remove_room_by_id(room_id)

    @router.post("/rooms/{room_id}/step")
    async def step_room(room_id: str):
        return dungeon.get_room(room_id).step()

    return router