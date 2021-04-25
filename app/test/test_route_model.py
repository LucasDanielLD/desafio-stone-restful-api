import unittest
import json
import datetime

from app.main import db
from app.main.model.routes import Routes
from app.test.base import BaseTestCase


class TestRouteModel(BaseTestCase):
    def test_get_geojson(self):
        geojson = {            
            "type": "FeatureCollection",
            "features": [
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -43.23257446289062,
                                -22.896734399393843
                            ],
                            [
                                -43.23789596557617,
                                -22.896101854870967
                            ],
                            [
                                -43.246307373046875,
                                -22.905589713001344
                            ],
                            [
                                -43.233604431152344,
                                -22.918081047105982
                            ],
                            [
                                -43.22227478027344,
                                -22.934207395829283
                            ],
                            [
                                -43.20167541503906,
                                -22.938159639316396
                            ],
                            [
                                -43.18502426147461,
                                -22.923298605291222
                            ],
                            [
                                -43.18347930908203,
                                -22.913811986441825
                            ],
                            [
                                -43.187599182128906,
                                -22.90527346175716
                            ],
                            [
                                -43.23257446289062,
                                -22.896734399393843
                            ]
                        ]
                    ]
                }
                }                
            ]
        } 
        return geojson
    
    def test_get_new_geojson(self):
        new_geojson = {            
            "type": "FeatureCollection",
            "features": [
                {      
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                    [
                        [
                        -43.188629150390625,
                        -22.98016485299822
                        ],
                        [
                        -43.170905113220215,
                        -22.966849466784417
                        ],
                        [
                        -43.175411224365234,
                        -22.958827992826674
                        ],
                        [
                        -43.184852600097656,
                        -22.960290070337315
                        ],
                        [
                        -43.19416522979736,
                        -22.966968007166404
                        ],
                        [
                        -43.19819927215576,
                        -22.988185060738665
                        ],
                        [
                        -43.190474510192864,
                        -22.992609799088456
                        ],
                        [
                        -43.18184852600098,
                        -22.98668377728947
                        ],
                        [
                        -43.188629150390625,
                        -22.98016485299822
                        ]
                    ]
                    ]
                }    
                }
            ]
        }  
        return new_geojson
        
        
    def test_check_geojson(self):           
        geojson = self.test_get_geojson()
        new_geojson = self.test_get_new_geojson()                
        self.assertTrue(isinstance(new_geojson, dict))     
        self.assertTrue(isinstance(new_geojson, dict))     
        
        route = Routes(
            public_id="123123-123-123123-123",
            name='Centro do Rio de Janeiro',
            bounds=json.dumps(geojson),            
            seller="111-222-333-444-555",
            created_on=datetime.datetime.utcnow(),
            last_update=datetime.datetime.utcnow()
        )        
        db.session.add(route)
        db.session.commit()
        exists_route = Routes.check_geojson(new_geojson, route.query.all())                
        self.assertTrue(exists_route == False)
        
        
    def test_seller_is_associated(self):
        geojson = self.test_get_geojson()
        new_geojson = self.test_get_new_geojson()                
        self.assertTrue(isinstance(new_geojson, dict))     
        self.assertTrue(isinstance(new_geojson, dict))     
        route = Routes(
            public_id="123123-123-123123-123",
            name='Centro do Rio de Janeiro',
            bounds=json.dumps(geojson),            
            seller="111-222-333-444-555",
            created_on=datetime.datetime.utcnow(),
            last_update=datetime.datetime.utcnow()
        )        
        db.session.add(route)
        db.session.commit()
        new_seller = "999-999-999-999-999"
        seller_is_associated = Routes.check_seller(new_seller)
        self.assertTrue(seller_is_associated == None)


if __name__ == '__main__':
    unittest.main()

