import uuid
import datetime

import json
from app.main import db
from app.main.model.sellers import Sellers
from ..service.customer_service import get_customers_by_route
from ..service.route_service import get_route_by_seller
from typing import Dict, Tuple


def save_new_seller(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    seller = Sellers.query.filter_by(name=data['name'], email=data['email'], deleted=False).first()        
    if not seller:
        new_seller = Sellers(    
            public_id=str(uuid.uuid4()),        
            name=data['name'],            
            email=data['email'], 
            created_on=datetime.datetime.utcnow(),
            last_update=datetime.datetime.utcnow()
        )        
        return save_changes(new_seller)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Vendedor already exists.',
        }
        return response_object, 409


def get_all_sellers():
    response_object = []        
    sellers = Sellers.query.filter_by(deleted=False).all()       
    
    for seller in sellers:              
        route = get_route_by_seller(seller.public_id)          
        customers = get_customers_by_route(getattr(route, "public_id", ""))              
                                          
        seller_informations = {
            "name": seller.name,
            "email": seller.email,
            "public_id": seller.public_id,
            "associated_route": getattr(route, "name", "Outros"),
            "customers": customers
        }
        response_object.append(seller_informations)
    
    return response_object


def get_a_seller(public_id): 
    seller = Sellers.query.filter_by(public_id=public_id).first()    
    route = get_route_by_seller(seller.public_id)  
    customers = get_customers_by_route(getattr(route, "public_id", ""))              
    
    response_object = {
        "name": seller.name,
        "email": seller.email,
        "public_id": seller.public_id,
        "associated_route": getattr(route, "name", "Outros"),
        "customers": customers
    }
    
    return response_object


def edit_a_seller(seller, data):    
    try:
        seller.name = data['name']
        seller.email = data['email']
        seller.last_update = datetime.datetime.utcnow()
        db.session.commit()    
        
        response_object = {
            'status': 'sucess',
            'message': 'Vendedor successfully edited.'            
        }
                
        return response_object, 204
    
    except Exception:              
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def delete_a_seller(seller):    
    try:
        seller.deleted = True
        seller.last_update = datetime.datetime.utcnow()
        db.session.commit()    
        
        response_object = {
            'status': 'sucess',
            'message': 'Vendedor successfully deleted.'            
        }
                
        return response_object, 204
    
    except Exception:              
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    

def save_changes(data: Sellers) -> None:
    try:
        db.session.add(data)
        db.session.commit()
        
        response_object = {
            'status': 'success',
            'message': 'Vendedor successfully registered.'            
        }        
        return response_object, 201
    
    except Exception:              
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
        