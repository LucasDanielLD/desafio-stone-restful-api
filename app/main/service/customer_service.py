import uuid
import datetime

from app.main import db
from app.main.model.routes import Routes
from app.main.model.sellers import Sellers
from app.main.model.customers import Customers
from typing import Dict, Tuple
from sqlalchemy import func, or_, and_


def save_new_customer(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    geojsons = Routes.query.filter(
        and_(Routes.public_id != '651ea51f-0128-4a28-bc2d-78d1171beb93',
        Routes.deleted == False)
    )
    point = (data["longitude"], data["latitude"])
    associated_route = Customers.check_point_in_geojson(point, geojsons)
    customer = Customers.query.filter_by(
        latitude=data["latitude"], longitude=data["longitude"]
    ).first()

    if not customer:
        new_customer = Customers(
            public_id=str(uuid.uuid4()),
            name=data["name"],
            longitude=data["longitude"],
            latitude=data["latitude"],
            route_id=associated_route,
            created_on=datetime.datetime.utcnow(),
            last_update=datetime.datetime.utcnow(),
        )
        return save_changes(new_customer)
    else:
        response_object = {
            "status": "fail",
            "message": "Cliente already exists.",
        }
        return response_object, 409


def get_all_customers(route, seller):
    response_object = []

    if route[0] == "" and seller[0] == "":
        customers = Customers.query.filter_by(deleted=False)
    elif route[0] != "" and seller[0] != "":
        customers = (
            db.session.query(Customers)
            .filter(
                Routes.seller == Sellers.public_id,
            )
            .filter(
                Routes.public_id == Customers.route_id,
            )
            .filter(
                and_(
                    or_(
                        func.lower(Routes.public_id).in_(route),
                        func.lower(Routes.name).in_(route),
                    ),
                    or_(
                        func.lower(Sellers.name).in_(seller),
                        func.lower(Sellers.public_id).in_(seller),
                        func.lower(Sellers.email).in_(seller),
                    ),
                ),
                and_(Customers.deleted == False),
            )
            .all()
        )
    else:
        customers = (
            db.session.query(Customers)
            .filter(
                Routes.seller == Sellers.public_id,
            )
            .filter(
                Routes.public_id == Customers.route_id,
            )
            .filter(
                or_(
                    or_(
                        func.lower(Routes.public_id).in_(route),
                        func.lower(Routes.name).in_(route),
                    ),
                    or_(
                        func.lower(Sellers.name).in_(seller),
                        func.lower(Sellers.public_id).in_(seller),
                        func.lower(Sellers.email).in_(seller),
                    ),
                ),
                and_(Customers.deleted == False),
            )
            .all()
        )

    for customer in customers:
        customers_informations = {
            "name": customer.name,
            "longitude": customer.longitude,
            "latitude": customer.latitude,
            "public_id": customer.public_id,
        }
        response_object.append(customers_informations)

    return response_object


def get_a_customer(public_id):
    return Customers.query.filter_by(public_id=public_id, deleted=False).first()


def get_customers_by_route(route_id):
    customers = Customers.query.filter_by(route_id=route_id, deleted=False).all()
    response_object = []

    for customer in customers:
        customer_informations = {
            "name": customer.name,
            "longitude": customer.longitude,
            "latitude": customer.latitude,
            "public_id": customer.public_id,
        }
        response_object.append(customer_informations)

    return response_object


def get_customers_by_seller(seller_id):
    response_object = []
    customers = (
        db.session.query(Customers)
        .filter(
            Routes.seller == Sellers.public_id,
        )
        .filter(
            Routes.public_id == Customers.route_id,
        )
        .filter(and_(Sellers.public_id == seller_id, Customers.deleted == False))
        .all()
    )

    for customer in customers:
        customers_informations = {
            "name": customer.name,
            "longitude": customer.longitude,
            "latitude": customer.latitude,
            "public_id": customer.public_id,
        }
        response_object.append(customers_informations)

    return response_object


def edit_a_customer(customer, data):
    geojsons = Routes.query.filter(
        and_(Routes.public_id != '651ea51f-0128-4a28-bc2d-78d1171beb93',
        Routes.deleted == False)
    )
    point = (data["longitude"], data["latitude"])
    associated_route = Customers.check_point_in_geojson(point, geojsons)

    try:
        customer.name = data["name"]
        customer.longitude = data["longitude"]
        customer.latitude = data["latitude"]
        customer.last_update = datetime.datetime.utcnow()
        customer.route_id = associated_route
        db.session.commit()

        response_object = {
            "status": "sucess",
            "message": "Cliente successfully edited.",
        }

        return response_object, 204

    except Exception:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return response_object, 401


def delete_a_customer(customer):
    try:
        customer.deleted = True
        customer.last_update = datetime.datetime.utcnow()
        db.session.commit()

        response_object = {
            "status": "sucess",
            "message": "Cliente successfully deleted.",
        }
        return response_object, 204

    except Exception:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return response_object, 401


def save_changes(data: Customers) -> None:
    try:
        db.session.add(data)
        db.session.commit()

        response_object = {
            "status": "success",
            "message": "Cliente successfully registered.",
        }
        return response_object, 201

    except Exception:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return response_object, 401
