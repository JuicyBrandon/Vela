"""Deterministic geometry only. No generated interpretation or invented positions."""
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from threading import RLock
import swisseph as swe

LOCK = RLock()
swe.set_sid_mode(swe.SIDM_LAHIRI)
FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED
SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
BODIES = [(0,'Sun','☉','Surya','सूर्य'),(1,'Moon','☽','Chandra','चन्द्र'),(2,'Mercury','☿','Budha','बुध'),(3,'Venus','♀','Shukra','शुक्र'),(4,'Mars','♂','Mangala','मंगल'),(5,'Jupiter','♃','Guru','गुरु'),(6,'Saturn','♄','Shani','शनि'),(7,'Uranus','♅','Uranus',''),(8,'Neptune','♆','Neptune',''),(9,'Pluto','♇','Pluto',''),(swe.MEAN_NODE,'North node','☊','Rahu','राहु')]
ASPECTS = [(0,'Conjunction'),(60,'Sextile'),(90,'Square'),(120,'Trine'),(180,'Opposition')]

def jd_at(dt):
    utc = dt.astimezone(timezone.utc)
    return swe.utc_to_jd(utc.year, utc.month, utc.day, utc.hour, utc.minute, utc.second + utc.microsecond / 1e6)[1]

def iso_at(jd):
    y,m,d,h,minute,sec = swe.jdut1_to_utc(jd)
    return (datetime(y,m,d,h,minute,tzinfo=timezone.utc)+timedelta(seconds=sec)).isoformat()

def wrap(x):
    return (x+180)%360-180

def pos(jd, body, sidereal=False):
    values, used = swe.calc_ut(jd, body, FLAGS | (swe.FLG_SIDEREAL if sidereal else 0))
    if not used & swe.FLG_MOSEPH:
        raise ValueError('Unexpected ephemeris source')
    return values

def chart(jd, latitude, longitude, sidereal=False):
    with LOCK:
        cusps, axes = swe.houses_ex(jd,latitude,longitude,b'W',swe.FLG_SIDEREAL if sidereal else 0)
        asc = axes[0]
        first_sign = int(asc//30)
        planets=[]
        for body,name,glyph,vedic,sanskrit in BODIES:
            if sidereal and body in (7,8,9):
                continue
            p=pos(jd,body,sidereal)
            sign=int(p[0]//30)
            planets.append(dict(name=name,glyph=glyph,vedic_name=vedic,sanskrit=sanskrit,longitude=p[0],sign=SIGNS[sign],sign_index=sign,degree=p[0]%30,speed=p[3],retrograde=p[3]<0,house=(sign-first_sign)%12+1))
        if sidereal:
            node=planets[-1].copy()
            lng=(node['longitude']+180)%360
            sign=int(lng//30)
            node.update(name='South node',glyph='☋',vedic_name='Ketu',sanskrit='केतु',longitude=lng,sign=SIGNS[sign],sign_index=sign,degree=lng%30,house=(sign-first_sign)%12+1)
            planets.append(node)
        return dict(system='Lahiri sidereal' if sidereal else 'Tropical',house_system='Whole sign',ascendant=asc,cusps=list(cusps),planets=planets,ayanamsa=swe.get_ayanamsa_ut(jd) if sidereal else 0,aspects=aspects(planets,orb=6))

def aspects(planets, other=None, orb=3):
    found=[]
    targets=other or planets
    for i,a in enumerate(planets):
        for j,b in enumerate(targets):
            if other is None and j<=i:
                continue
            sep=abs(wrap(a['longitude']-b['longitude']))
            for angle,name in ASPECTS:
                error=abs(sep-angle)
                if error<=orb:
                    future_sep=abs(wrap(a['longitude']+a['speed']/24-b['longitude']-(b['speed']/24 if other is None else 0)))
                    future_error=abs(future_sep-angle)
                    found.append(dict(planet=a['name'],target=b['name'],aspect=name,angle=angle,orb=round(error,4),phase='Exact' if error<0.01 else ('Approaching' if future_error<error else 'Separating')))
    return sorted(found,key=lambda x:x['orb'])

def natal(profile):
    from zoneinfo import ZoneInfo
    dt=datetime.fromisoformat(f'{profile.date}T{profile.time}').replace(tzinfo=ZoneInfo(profile.timezone))
    j=jd_at(dt)
    with LOCK:
        result=dict(tropical=chart(j,profile.latitude,profile.longitude),sidereal=chart(j,profile.latitude,profile.longitude,True),birth_utc=dt.astimezone(timezone.utc).isoformat())
        if profile.uncertainty_minutes:
            samples=[]
            count=max(2,int(profile.uncertainty_minutes*2/15))
            for i in range(count+1):
                offset=-profile.uncertainty_minutes+2*profile.uncertainty_minutes*i/count
                sj=jd_at(dt+timedelta(minutes=offset))
                samples.append(dict(time=(dt+timedelta(minutes=offset)).strftime('%H:%M'),tropical=chart(sj,profile.latitude,profile.longitude),sidereal=chart(sj,profile.latitude,profile.longitude,True)))
            result['uncertainty']=dict(minutes=profile.uncertainty_minutes,sampling_minutes=2*profile.uncertainty_minutes/count,ascendants={system:sorted({SIGNS[int(s[system]['ascendant']//30)] for s in samples}) for system in ('tropical','sidereal')},stable_signs={system:[p['name'] for p in result[system]['planets'] if len({next(q['sign_index'] for q in s[system]['planets'] if q['name']==p['name']) for s in samples})==1] for system in ('tropical','sidereal')},samples=samples)
        else:
            result['uncertainty']=None
        return result

def refine(fn,lo,hi):
    value=fn(lo)
    for _ in range(28):
        mid=(lo+hi)/2
        if fn(mid)*value<=0:
            hi=mid
        else:
            lo=mid
            value=fn(lo)
    return (lo+hi)/2

@lru_cache(maxsize=12)
def events(start_day, days=45):
    with LOCK:
        start=jd_at(datetime.fromisoformat(start_day).replace(tzinfo=timezone.utc))
        end=start+days
        found=[]
        for solar in (True,False):
            j=start
            for _ in range(8):
                flags,times=(swe.sol_eclipse_when_glob(j,swe.FLG_MOSEPH) if solar else swe.lun_eclipse_when(j,swe.FLG_MOSEPH))
                if times[0]>=end:
                    break
                found.append(dict(kind='Solar eclipse' if solar else 'Lunar eclipse',at=iso_at(times[0]),detail='Global maximum. Local visibility is not calculated.',system='Astronomical event'))
                j=times[0]+1
        t=start
        while t<end:
            nxt=min(t+0.5,end)
            for target,name in ((0,'New moon'),(180,'Full moon')):
                fn=lambda j: wrap(pos(j,swe.MOON)[0]-pos(j,swe.SUN)[0]-target)
                a,b=fn(t),fn(nxt)
                if a*b<0 and abs(a-b)<90:
                    root=refine(fn,t,nxt)
                    found.append(dict(kind=name,at=iso_at(root),detail='Exact Sun and Moon longitude alignment.',system='Astronomical event'))
            for body,name,*_ in BODIES:
                if body==swe.MEAN_NODE:
                    continue
                a,b=pos(t,body),pos(nxt,body)
                if a[3]*b[3]<0:
                    root=refine(lambda j:pos(j,body)[3],t,nxt)
                    found.append(dict(kind='Station',at=iso_at(root),detail=f'{name} turns '+('retrograde' if b[3]<0 else 'direct')+'.',system='Both systems'))
                for sidereal in (False,True):
                    x,y=pos(t,body,sidereal)[0],pos(nxt,body,sidereal)[0]
                    if int(x//30)!=int(y//30):
                        boundary=(int(y//30)*30 if wrap(y-x)>0 else int(x//30)*30)%360
                        root=refine(lambda j:wrap(pos(j,body,sidereal)[0]-boundary),t,nxt)
                        entered=SIGNS[int(pos(root+1e-5,body,sidereal)[0]//30)]
                        found.append(dict(kind='Sign ingress',at=iso_at(root),detail=f'{name} enters {entered}.',system='Lahiri sidereal' if sidereal else 'Tropical'))
                if body in (swe.MERCURY,swe.VENUS,swe.MARS,swe.JUPITER,swe.SATURN):
                    fn=lambda j:wrap(pos(j,body)[0]-pos(j,swe.SUN)[0])
                    a,b=fn(t),fn(nxt)
                    if a*b<0 and abs(a-b)<90:
                        root=refine(fn,t,nxt)
                        found.append(dict(kind='Solar conjunction',at=iso_at(root),detail=f'{name} at exact conjunction with the Sun. Cazimi window uses the displayed 17 arcminute convention.',system='Tropical longitude'))
            t=nxt
        return sorted(found,key=lambda x:x['at'])

def sky(profile, moment, birth):
    j=jd_at(moment)
    with LOCK:
        tropical=chart(j,profile.latitude,profile.longitude)
        sidereal=chart(j,profile.latitude,profile.longitude,True)
        sun=tropical['planets'][0]['longitude']
        close=[dict(planet=p['name'],separation=abs(wrap(p['longitude']-sun))) for p in tropical['planets'][2:7] if abs(wrap(p['longitude']-sun))<=17/60]
        return dict(at=moment.isoformat(),tropical=tropical,sidereal=sidereal,transits=aspects(tropical['planets'],birth['tropical']['planets'],3),sidereal_geometry=aspects(sidereal['planets'],birth['sidereal']['planets'],3),cazimi=close,cazimi_rule='Within 17 arcminutes in ecliptic longitude. Configured convention; traditional rule review pending.',moon_phase_angle=(tropical['planets'][1]['longitude']-sun)%360,events=events(moment.astimezone(timezone.utc).date().isoformat()),calculation_source=dict(engine='Swiss Ephemeris',version=swe.version,ephemeris='Moshier',node='Mean lunar node',houses='Whole sign',sidereal='Lahiri',documentation='https://www.astro.com/swisseph/swephprg.htm'))
