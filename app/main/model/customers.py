from .. import db
import datetime
import json
from shapely.geometry import shape, Point

class Customers(db.Model):
    """ Customers Model """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    route_id = db.Column(db.String(100))
    created_on = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean(), default=False)
    

    @staticmethod
    def check_point_in_geojson(points: str, routes: str) -> bool:        
        point = Point(points)         

        for route in routes:                                 
            bounds = json.loads(route.bounds)                        
            polygon = shape(bounds['features'][0]['geometry'])
                    
            if polygon.contains(point):       
                return route.public_id
                
        return '651ea51f-0128-4a28-bc2d-78d1171beb93' #public ID rota Outros
    