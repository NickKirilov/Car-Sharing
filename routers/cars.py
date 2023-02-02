import typing as t

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlmodel import Session

from db import get_session
from routers.auth import get_current_user
from schemas import CarInput, Car, CarOutput, Trip, TripInput, User

router = APIRouter(prefix="/api/cars")


@router.get("/")
def get_cars(size: t.Optional[str] = None, doors: t.Optional[int] = None,
             session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)

    return session.exec(query).all()


@router.get("/{id}", response_model=CarOutput)
async def car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)

    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Not Found. There is no {id} id")


@router.post("/", response_model=Car)
def add_car(car: CarInput, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> Car:
    new_car = Car.from_orm(car)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)

    return new_car


@router.delete("/{id}", status_code=200)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}")


@router.put("/{id}", response_model=Car)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()

        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


class BadTripException(Exception):
    pass


@router.post("/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip: TripInput, session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip, update={"car_id": car_id})
        if new_trip.end <= new_trip.start:
            raise BadTripException("Trip end before start!")
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)

        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")
