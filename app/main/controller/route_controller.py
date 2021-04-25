from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import RoutesDto
from ..service.seller_service import get_a_seller
from ..service.route_service import (
    get_all_routes, 
    get_a_route,
    save_new_route,
    edit_a_route,
    delete_a_route,
    associate_seller,
    disassociate_seller
)
from typing import Dict, Tuple

api = RoutesDto.api
_routes = RoutesDto.routes


@api.route('/')
class RoutesList(Resource):
    @api.doc('lista todas as rotas cadastradas')
    @admin_token_required
    @api.marshal_list_with(_routes, envelope='data')
    def get(self):
        """ Lista todas as rotas cadastradas """
        return get_all_routes()


    @api.expect(_routes, validate=True)
    @api.response(201, 'Rota successfully registered.') 
    @api.response(401, 'Some error occurred. Please try again.')
    @api.response(409, 'Rota already exists.')  
    @admin_token_required      
    @api.doc('cadastra uma nova rota')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Cadastra uma nova rota """                
        data = request.json                            
        
        return save_new_route(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'ID público da rota')
@api.response(404, 'Rota not found.')
class Route(Resource):
    @api.doc('retorna uma rota pelo seu ID público')
    @admin_token_required
    @api.marshal_with(_routes)
    def get(self, public_id):
        """ Retorna uma rota pelo seu ID público """
        route = get_a_route(public_id)
        if not route:
            api.abort(404)
        else:
            return route
        
    
    @api.expect(_routes, validate=True)
    @api.doc('edita uma rota pelo seu ID público')
    @admin_token_required    
    def put(self, public_id):
        """ Edita uma rota pelo seu ID público """
        data = request.json
        route = get_a_route(public_id)             
        
        if getattr(route, "deleted", True):
            api.abort(404)   
            
        return edit_a_route(route, data)
    

    @api.doc('deleta uma rota pelo seu ID público (Soft Delete)')
    @api.response(204, 'Rota successfully deleted.') 
    @admin_token_required    
    def delete(self, public_id):
        """ Deleta uma rota pelo seu ID público (Soft Delete) """
        route = get_a_route(public_id)
        seller = get_a_seller(route.seller)
        
        if getattr(route, "deleted", True):
            api.abort(404)                
            
        if not getattr(seller, "deleted", True):
            response_object = {
                'status': 'fail',
                'message': 'There is a seller associated with a route.',
            }
            return response_object, 409
        
        return delete_a_route(route)


@api.route('/<public_id>/vendedor/')
@api.param('public_id', 'ID público da rota')
@api.response(404, 'Rota not found.')
class RouteWithSeller(Resource):                
    @api.response(201, 'Vendedor successfully associated.') 
    @api.response(401, 'Some error occurred. Please try again.')
    @api.response(409, 'Vendedor already associated with a route.')  
    @admin_token_required      
    @api.doc('associa um vendedor a uma rota')
    def post(self, public_id) -> Tuple[Dict[str, str], int]:
        """ Associa um vendedor a uma rota """                
        data = request.json        
        route = get_a_route(public_id)   
        seller = get_a_seller(data["vendedor"])
                
        if getattr(seller, "deleted", True):
            response_object = {
                'status': 'fail',
                'message': 'Vendedor not found.',
            }
            return response_object, 404
        
        if getattr(route, "deleted", True):
            response_object = {
                'status': 'fail',
                'message': 'Rota not found.',
            }
            return response_object, 404
        
        return associate_seller(route, data)
        
    
    @api.doc('disassocia o vendedor a uma rota')
    @api.response(204, 'Vendedor successfully disassociated.') 
    @admin_token_required    
    def delete(self, public_id):
        """ Disassocia o vendedor a uma rota """
        route = get_a_route(public_id)        
        
        if getattr(route, "deleted", True):
            api.abort(404)                                
        
        return disassociate_seller(route)