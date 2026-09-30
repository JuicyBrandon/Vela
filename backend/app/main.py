from datetime import date as Date, datetime, timezone
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from app.services.ephemeris import natal, sky

ROOT=Path(__file__).resolve().parents[1]
PROFILE_PATH=Path(os.environ.get('VELA_PROFILE_PATH',ROOT/'.local/profile.json'))
app=FastAPI(title='Vela',version='0.1.0')

class Profile(BaseModel):
    name: str=Field(min_length=1,max_length=80)
    date: str
    time: str
    place: str=Field(min_length=1,max_length=120)
    latitude: float=Field(ge=-65,le=65)
    longitude: float=Field(ge=-180,le=180)
    timezone: str
    uncertainty_minutes: int=Field(default=0,ge=0,le=240)
    time_source: str=Field(default='Not specified',max_length=120)
    @field_validator('date')
    @classmethod
    def valid_date(cls,v):
        d=Date.fromisoformat(v)
        if not 1900<=d.year<=2099: raise ValueError('Supported birth years: 1900 to 2099')
        return v
    @field_validator('time')
    @classmethod
    def valid_time(cls,v):
        datetime.strptime(v,'%H:%M')
        return v
    @field_validator('timezone')
    @classmethod
    def valid_zone(cls,v):
        try: ZoneInfo(v)
        except ZoneInfoNotFoundError: raise ValueError('Use an IANA time zone, such as Australia/Brisbane')
        return v

@app.middleware('http')
async def local_origin(request: Request,call_next):
    origin=request.headers.get('origin')
    if request.method not in ('GET','HEAD','OPTIONS') and origin and origin not in ('http://localhost:3000','http://127.0.0.1:3000','http://localhost:8000','http://127.0.0.1:8000'):
        return JSONResponse(status_code=403,content={'detail':'This local preview accepts changes only from its own interface.'})
    return await call_next(request)

@app.get('/api/health')
def health():
    return {'status':'ok','stage':'Calculation foundation','ai_ready':False}

@app.get('/api/profile')
def profile():
    if not PROFILE_PATH.exists(): return None
    return Profile.model_validate_json(PROFILE_PATH.read_text()).model_dump()

@app.put('/api/profile')
def save_profile(p:Profile):
    PROFILE_PATH.parent.mkdir(parents=True,exist_ok=True)
    temporary=PROFILE_PATH.with_suffix('.tmp')
    temporary.write_text(p.model_dump_json(indent=2))
    temporary.chmod(0o600)
    temporary.replace(PROFILE_PATH)
    return p

@lru_cache(maxsize=8)
def cached_natal(raw):
    return natal(Profile.model_validate_json(raw))

@app.get('/api/workspace')
def workspace(at:str|None=None):
    raw=profile()
    if raw is None: raise HTTPException(409,'Save a birth profile to calculate your charts.')
    p=Profile(**raw)
    try:
        moment=datetime.fromisoformat(at.replace('Z','+00:00')) if at else datetime.now(timezone.utc)
        if moment.tzinfo is None: raise ValueError('Time zone required')
        if not 1900<=moment.year<=2099: raise ValueError('Supported dates: 1900 to 2099')
        birth=cached_natal(p.model_dump_json())
        current=sky(p,moment,birth)
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc
    return {'profile':p,'natal':birth,'sky':current,'status':{'interpretations':'Not connected. No generated readings in this milestone.','dasha':'Not implemented in this milestone.','sensitivity':'Sampled every 15 minutes; changes between samples are not ruled out.'}}
