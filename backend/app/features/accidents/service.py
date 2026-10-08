from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from geoalchemy2.elements import WKTElement
from app.features.accidents.models import Accident
from app.features.accidents.schemas import AccidentCreate

async def get_all_accidents(db: AsyncSession):
    """Fetches all active accidents and formats coordinates for the frontend."""
    query = select(
        Accident.id,
        Accident.reporter_id,
        Accident.title,
        Accident.description,
        Accident.status,
        Accident.is_deleted,
        Accident.created_at,
        Accident.updated_at,
        func.ST_Y(Accident.location).label('lat'), 
        func.ST_X(Accident.location).label('lng')  
    ).where(Accident.is_deleted == False) 

    result = await db.execute(query)
    
    accidents = []
    for row in result.all():
        accidents.append({
            "id": row.id,
            "reporter_id": row.reporter_id,
            "title": row.title,
            "description": row.description,
            "status": row.status,
            "is_deleted": row.is_deleted,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "coordinates": [row.lat, row.lng]
        })
    return accidents


async def create_accident(db: AsyncSession, accident_in: AccidentCreate):
    """Creates a new accident and converts coordinates to PostGIS format."""
    lat, lng = accident_in.coordinates

    point_wkt = f"POINT({lng} {lat})"
    
    new_accident = Accident(
        reporter_id=accident_in.reporter_id,
        title=accident_in.title,
        description=accident_in.description,
        status=accident_in.status,
        location=WKTElement(point_wkt, srid=4326)
    )

    db.add(new_accident)
    await db.commit()
    await db.refresh(new_accident)

    return {
        "id": new_accident.id,
        "reporter_id": new_accident.reporter_id,
        "title": new_accident.title,
        "description": new_accident.description,
        "status": new_accident.status,
        "is_deleted": new_accident.is_deleted,
        "created_at": new_accident.created_at,
        "updated_at": new_accident.updated_at,
        "coordinates": [lat, lng]
    }