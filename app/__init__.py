from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.seller_controller import api as seller_ns
from .main.controller.customer_controller import api as customer_ns
from .main.controller.route_controller import api as route_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          prefix='/api/v1',
          title='DESAFIO STONE (BACKEND)',
          version='1.0',
          description='API desenvolvida no desafio técnico da Stone Pagamentos para a vaga de Desenvolvedor Backend.\n' \
            'Desenvolvido por: Lucas Daniel.\n' \
            'https://github.com/LucasDanielLD/desafio-stone-restful-api.\n' \
            'https://www.linkedin.com/in/lucasdanielld/.'
          )

api.add_namespace(user_ns)
api.add_namespace(seller_ns)
api.add_namespace(customer_ns)
api.add_namespace(route_ns)
api.add_namespace(auth_ns)