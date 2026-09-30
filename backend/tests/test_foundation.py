import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
import swisseph as swe
from app.main import app, Profile
from app.services.ephemeris import chart, natal, jd_at, aspects, events, iso_at
DATA=dict(name='Synthetic profile',date='2000-01-01',time='12:00',place='Greenwich',latitude=51.48,longitude=0,timezone='Europe/London',uncertainty_minutes=30,time_source='Synthetic fixture')
class GeometryTests(unittest.TestCase):
    def setUp(self): self.jd=jd_at(datetime(2000,1,1,12,tzinfo=timezone.utc))
    def test_time_round_trip(self):
        self.assertAlmostEqual(self.jd,2451545,places=4)
        self.assertLess(abs((datetime.fromisoformat(iso_at(self.jd))-datetime(2000,1,1,12,tzinfo=timezone.utc)).total_seconds()),.1)
    def test_lahiri_and_houses(self):
        a,b=chart(self.jd,51.48,0),chart(self.jd,51.48,0,True)
        for p in b['planets'][:-1]:
            q=next(q for q in a['planets'] if q['name']==p['name'])
            self.assertAlmostEqual((q['longitude']-p['longitude'])%360,b['ayanamsa'],delta=.01)
        for i,c in enumerate(a['cusps']):
            self.assertAlmostEqual(c%30,0,places=7)
            self.assertAlmostEqual((c-a['cusps'][0])%360,i*30,places=6)
    def test_nodes_and_classical_planets(self):
        b=chart(self.jd,51.48,0,True)
        rahu,ketu=b['planets'][-2:]
        self.assertAlmostEqual((ketu['longitude']-rahu['longitude'])%360,180)
        self.assertEqual(len(b['planets']),9)
        self.assertFalse(any(p['name']=='Uranus' for p in b['planets']))
    def test_aspect_wrap_and_phase(self):
        target=[dict(name='Natal',longitude=1,speed=0)]
        contact=aspects([dict(name='Transit',longitude=359,speed=1)],target,3)[0]
        self.assertEqual((contact['aspect'],contact['orb'],contact['phase']),('Conjunction',2,'Approaching'))
        self.assertFalse(aspects([dict(name='Transit',longitude=357,speed=1)],target,3))
    def test_uncertainty_endpoints(self):
        u=natal(Profile(**DATA))['uncertainty']
        self.assertEqual((u['samples'][0]['time'],u['samples'][-1]['time']),('11:30','12:30'))
        self.assertEqual(len(u['samples']),5)
        self.assertEqual(u['sampling_minutes'],15)
    def test_events_and_lunation(self):
        found=events('2024-04-01',15)
        self.assertTrue(next(e for e in found if e['kind']=='Solar eclipse')['at'].startswith('2024-04-08'))
        j=jd_at(datetime.fromisoformat(next(e for e in found if e['kind']=='New moon')['at']))
        moon=swe.calc_ut(j,swe.MOON,swe.FLG_MOSEPH)[0][0]
        sun=swe.calc_ut(j,swe.SUN,swe.FLG_MOSEPH)[0][0]
        self.assertLess(abs((moon-sun+180)%360-180),1e-5)
        self.assertEqual(found,sorted(found,key=lambda e:e['at']))
class APITests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.patch=patch('app.main.PROFILE_PATH',Path(self.temp.name)/'profile.json')
        self.patch.start()
        self.client=TestClient(app)
    def tearDown(self):
        self.patch.stop(); self.temp.cleanup()
    def test_saved_profile_to_calculation(self):
        self.assertIsNone(self.client.get('/api/profile').json())
        self.assertEqual(self.client.get('/api/workspace').status_code,409)
        self.assertEqual(self.client.put('/api/profile',json=DATA).status_code,200)
        result=self.client.get('/api/workspace?at=2026-10-01T00:00:00%2B00:00')
        self.assertEqual(result.status_code,200,result.text)
        self.assertEqual(result.json()['sky']['calculation_source']['ephemeris'],'Moshier')
        self.assertFalse(self.client.get('/api/health').json()['ai_ready'])
        self.assertIn('Not connected',result.json()['status']['interpretations'])
    def test_invalid_input_and_origin(self):
        self.assertEqual(self.client.put('/api/profile',json=dict(DATA,timezone='Invented/Zone')).status_code,422)
        self.assertEqual(self.client.put('/api/profile',json=DATA,headers={'Origin':'https://unrelated.example'}).status_code,403)
        self.assertEqual(self.client.put('/api/profile',json=DATA,headers={'Origin':'http://localhost:3000'}).status_code,200)
        self.assertEqual(self.client.get('/api/workspace?at=2026-10-01T00:00:00').status_code,422)
if __name__=='__main__': unittest.main()
