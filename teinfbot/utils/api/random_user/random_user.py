from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID
import json


@dataclass
class Dob:
    date: Optional[datetime] = None
    age: Optional[int] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class ID:
    name: Optional[str] = None
    value: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Coordinates:
    latitude: Optional[str] = None
    longitude: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Street:
    number: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Timezone:
    offset: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Location:
    street: Optional[Street] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[int] = None
    coordinates: Optional[Coordinates] = None
    timezone: Optional[Timezone] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Login:
    uuid: Optional[UUID] = None
    username: Optional[str] = None
    password: Optional[str] = None
    salt: Optional[str] = None
    md5: Optional[str] = None
    sha1: Optional[str] = None
    sha256: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Name:
    title: Optional[str] = None
    first: Optional[str] = None
    last: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Picture:
    large: Optional[str] = None
    medium: Optional[str] = None
    thumbnail: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class User:
    gender: Optional[str] = None
    name: Optional[Name] = None
    location: Optional[Location] = None
    email: Optional[str] = None
    login: Optional[Login] = None
    dob: Optional[Dob] = None
    registered: Optional[Dob] = None
    phone: Optional[str] = None
    cell: Optional[str] = None
    id: Optional[ID] = None
    picture: Optional[Picture] = None
    nat: Optional[str] = None

    @classmethod
    def from_json(cls, data):
        return cls(
            gender=data.get('gender'),
            name=Name.from_json(data.get("name")),
            location=Location.from_json(data.get("location")),
            email=data.get("email"),
            login=Login.from_json(data.get("login")),
            dob=Dob.from_json(data.get("dob")),
            registered=Dob.from_json(data.get("registered")),
            phone=data.get('phone'),
            cell=data.get('cell'),
            id=ID.from_json(data.get("id")),
            picture=Picture.from_json(data.get("picture")),
            nat=data.get('nat')
        )
