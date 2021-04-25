from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import CustomersDto
from ..service.customer_service import (
    save_new_customer,
    edit_a_customer,
    delete_a_customer,
    get_all_customers,
    get_a_customer,    
    get_customers_by_seller
)
from typing import Dict, Tuple

api = CustomersDto.api
_customer = CustomersDto.customers


@api.route('/')
class Customers(Resource):
    @api.doc('lista todos os clientes cadastrados')
    @admin_token_required
    @api.marshal_list_with(_customer, envelope='data')
    def get(self):
        """ Lista todos os clientes cadastrados """
        rota = request.args.get('rota', default = '', type = str).lower().split('|')
        vendedor = request.args.get('vendedor', default = '', type = str).lower().split('|')            
        return get_all_customers(rota, vendedor)
    
    @api.expect(_customer, validate=True)
    @api.response(201, 'Cliente successfully registered.') 
    @api.response(401, 'Some error occurred. Please try again.')
    @api.response(409, 'Cliente already exists.')        
    @api.doc('cadastra um novo cliente')
    def post(self) -> Tuple[Dict[str, str], int]:
        """ Cadastra um novo cliente """
        data = request.json
        return save_new_customer(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'ID público do vendedor')
@api.response(404, 'vendedor not found.')
class CustomersFromSeller(Resource):
    @token_required
    @api.doc('retorna clientes pelo ID público do vendedor')    
    @api.marshal_with(_customer)
    def get(self, public_id):
        """ Retorna clientes pelo ID público do vendedor """
        customer = get_customers_by_seller(public_id)
        if not customer:
            api.abort(404)
        else:
            return customer
    
    @token_required
    @api.expect(_customer, validate=True)
    @api.doc('edita um cliente pelo seu ID público')    
    def put(self, public_id):
        """ Edita um cliente pelo seu ID público """
        data = request.json
        customer = get_a_customer(public_id)
        
        if getattr(customer, "deleted", True):
            api.abort(404)   
            
        return edit_a_customer(customer, data)
    

    @token_required
    @api.doc('deleta um cliente pelo seu ID público (Soft Delete)')
    @api.response(204, 'Cliente successfully registered.')
    def delete(self, public_id):
        """ Deleta um cliente pelo seu ID público (Soft Delete) """
        customer = get_a_customer(public_id)
        
        if getattr(customer, "deleted", True):
            api.abort(404)                
            
        return delete_a_customer(customer)