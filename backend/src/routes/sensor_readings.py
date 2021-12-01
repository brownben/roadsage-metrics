from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..database import create_sensor_readings
from ..schemas import Message, SensorReading, User
from ..utils.auth import get_current_active_user

router = APIRouter(tags=["Sensor Readings"], prefix="/sensor-readings")


@router.post("/", response_model=Message)
async def add_sensor_readings(
    readings: List[SensorReading], current_user: User = Depends(get_current_active_user)
) -> Message:
    """
    Upload sensor readings to the database.

    There is a limit to the number of reading which can be sent per request. 1000 readings has been tested, and it is recommened to keep batches to a maximum of 1000.
    """

    try:
        await create_sensor_readings(current_user.email, readings)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problem adding sensor reading to the database",
        )

    return Message(detail=f"Successfully added {len(readings)} sensor readings")