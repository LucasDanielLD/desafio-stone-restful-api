import uuid
import datetime
import json

from app.main import db
from app.main.model.routes import Routes
from sqlalchemy import and_
from typing import Dict, Tuple


def save_new_route(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    geojsons = db.session.query(Routes.bounds).filter(
        and_(Routes.public_id != '651ea51f-0128-4a28-bc2d-78d1171beb93',
        Routes.deleted == False)
    )
    routes = Routes.check_geojson(data['coordinates'], geojsons)
    
    if not routes:
        new_route = Routes(
            public_id=str(uuid.uuid4()),            
            name=data['name'],            
            bounds=json.dumps(data['coordinates']), 
            seller='',              
            created_on=datetime.datetime.utcnow(),
            last_update=datetime.datetime.utcnow()
        )       
        return save_changes(new_route)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Rota already exists.',
        }
        return response_object, 409


def get_all_routes():
    return Routes.query.filter_by(deleted=False).all()    


def get_a_route(public_id):
    return Routes.query.filter_by(public_id=public_id).first()


def get_route_by_seller(seller_id):
    return Routes.query.filter_by(seller=seller_id, deleted=False).first()


def edit_a_route(route, data):         
    if route.bounds != json.dumps(data['coordinates']):                
        geojsons = db.session.query(Routes.bounds).filter(
            and_(Routes.public_id != route.public_id,
            Routes.public_id != '651ea51f-0128-4a28-bc2d-78d1171beb93',
            Routes.deleted == False)
        )   
        routes_exists = Routes.check_geojson(data['coordinates'], geojsons)                      
        
        if routes_exists:
            response_object = {
                'status': 'fail',
                'message': 'Rota already exists.',
            }
            return response_object, 409

    try:                                        
        route.name = data['name']                                  
        route.bounds = json.dumps(data['coordinates'])
        route.last_update = datetime.datetime.utcnow()
        db.session.commit()    
        
        response_object = {
            'status': 'sucess',
            'message': 'Rota successfully edited.'            
        }
                
        return response_object, 204
    
    except Exception:                      
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401    
    
    
def delete_a_route(route):            
    try:        
        route.deleted = True 
        route.last_update = datetime.datetime.utcnow()       
        db.session.commit()    
        
        response_object = {
            'status': 'sucess',
            'message': 'Rota successfully deleted.'            
        }
                
        return response_object, 204
    
    except Exception:              
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    

def save_changes(data: Routes) -> None:
    try:
        db.session.add(data)
        db.session.commit()
        
        response_object = {
            'status': 'success',
            'message': 'Rota successfully registered.'            
        }        
        return response_object, 201
    
    except Exception:                      
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }        
        return response_object, 401
    
        
def associate_seller(route, data):
    seller_is_associated = Routes.check_seller(data['vendedor'])

    if seller_is_associated:
        response_object = {
            'status': 'fail',
            'message': 'Vendedor already associated with a route.',
        }
        return response_object, 409
    else:
        try:        
            route.seller = data['vendedor']
            db.session.commit()
            
            response_object = {
                'status': 'sucess',
                'message': 'Vendedor successfully associated.'            
            }
                    
            return response_object, 201
                
        except Exception:              
            response_object = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return response_object, 401
    
    
def disassociate_seller(route):
    if route.seller !=  '':
        route.seller = ''
        db.session.commit()
        
        response_object = {
            'status': 'sucess',
            'message': 'Vendedor successfully disassociated.'            
        }                    
        return response_object, 204    
    else:
        response_object = {
            'status': 'fail',
            'message': 'Associated vendedor not found.'            
        }                    
        return response_object, 404