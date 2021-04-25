from .. import db
import datetime
import json
import geopandas as gpd


class Routes(db.Model):
    """ Routes Model """
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    bounds = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)    
    seller = db.Column(db.Integer, nullable=False)
    public_id = db.Column(db.String(100), unique=True)
    created_on = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean(), default=False)
    

    @staticmethod
    def check_geojson(new_geojson: str, geojsons: str) -> bool:           
        new_polygon_geodataframe = gpd.GeoDataFrame.from_features(new_geojson["features"])        
        
        for geojson in geojsons:                  
            geojson = json.loads(geojson.bounds)            
            polygon_geodataframe = gpd.GeoDataFrame.from_features(geojson["features"])  
            exists = gpd.sjoin(new_polygon_geodataframe, polygon_geodataframe, how='inner',
                op='within', lsuffix='left', rsuffix='right')                       
            
            if not exists.empty:
                return True
    
        return False
    
    
    @staticmethod
    def check_seller(new_seller_id: str) -> bool:
        return Routes.query.filter_by(seller=new_seller_id, deleted=False).first() 
        
        
        
            