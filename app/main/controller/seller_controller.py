from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import SellersDto
from ..service.seller_service import (
    get_all_sellers, 
    get_a_seller,
    save_new_seller,
    edit_a_seller,
    delete_a_seller     
)
from typing import Dict, Tuple

api = SellersDto.api
_seller = SellersDto.sellers


@api.route('/')
class SeelersList(Resource):
    @api.doc('lista todos os vendedores cadastrados')
    @admin_token_required
    @api.marshal_list_with(_seller, envelope='data')
    def get(self):
        """ Lista todos os vendedores cadastrados """                
        return get_all_sellers()                
        

    @api.expect(_seller, validate=True)
    @api.response(201, 'Vendedor successfully registered.') 
    @api.response(401, 'Some error occurred. Please try again.')
    @api.response(409, 'Vendedor already exists.')
    @admin_token_required        
    @api.doc('cadastra um novo vendedor')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Cadastra um novo vendedor """
        data = request.json
        return save_new_seller(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'ID público do vendedor')
@api.response(404, 'Vendedor not found.')
class Seeler(Resource):
    @api.doc('retorna um vendedor pelo seu ID público')
    @admin_token_required
    @api.marshal_with(_seller)
    def get(self, public_id):
        """ Retorna um vendedor pelo seu ID público """
        seller = get_a_seller(public_id)
        if not seller:
            api.abort(404)
        else:
            return seller
    

    @api.expect(_seller, validate=True)
    @api.doc('edita um vendedor pelo seu ID público')
    @admin_token_required    
    def put(self, public_id):
        """ Edita um vendedor pelo seu ID público """
        data = request.json
        seller = get_a_seller(public_id)
        
        if getattr(seller, "deleted", True):
            api.abort(404)   
            
        return edit_a_seller(seller, data)
    

    @api.doc('deleta um vendedor pelo seu ID público (Soft Delete)')
    @api.response(204, 'Vendedor successfully deleted.') 
    @admin_token_required    
    def delete(self, public_id):
        """ Deleta um vendedor pelo seu ID público (Soft Delete) """
        seller = get_a_seller(public_id)
        
        if getattr(seller, "deleted", True):
            api.abort(404)                
            
        return delete_a_seller(seller)
