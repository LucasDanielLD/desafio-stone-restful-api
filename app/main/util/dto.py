""" Data Transfer Objects (DTOs) to Swagger Documentation. """

from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('users', description='operações relacionadas a usuário')
    user = api.model('users', {
        'email': fields.String(required=True, description='Email do usuário'),
        'name': fields.String(required=True, description='Nome do usuário'),
        'password': fields.String(required=True, description='Senha do usuário'),
        'public_id': fields.String(description='ID público do usuário')
    })


class AuthDto:
    api = Namespace('auth', description='operações relacionadas a autenticação')
    user_auth = api.model('autenticação', {
        'email': fields.String(required=True, description='O endereço de email'),
        'password': fields.String(required=True, description='Senha de autenticação'),
    })

    
class SellersDto:
    api = Namespace('vendedores', description='operações relacionadas a vendedores')
    sellers = api.model('vendedores', {
        'name': fields.String(required=True, description='Nome do vendedor'),
        'email': fields.String(required=True, description='Email do vendedor'),
        'public_id': fields.String(description='ID público do vendedor'),
        'associated_route': fields.String(description='Nome da rota associada ao vendedor'),
        'customers': fields.Raw(description="Clientes do Vendedor")
    })
    
    
class CustomersDto:
    api = Namespace('clientes', description='operações relacionadas a clientes')
    customers = api.model('clientes', {
        'name': fields.String(required=True, description='Nome do cliente'),
        'latitude': fields.Float(required=True, description='Latitude do cliente'),
        'longitude': fields.Float(required=True, description='Longitude do cliente'),
        'public_id': fields.String(description='ID público do cliente')
    })
        
    
class RoutesDto:
    api = Namespace('rotas', description='operações relacionadas a rotas')
    routes = api.model('rotas', {
        'name': fields.String(required=True, description='Nome da rota'),            
        'coordinates': fields.Raw(required=True, description="GeoJSON "),
        'public_id': fields.String(description='ID público da rota')
    })
