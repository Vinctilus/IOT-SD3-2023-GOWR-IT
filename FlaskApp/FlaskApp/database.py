#wiht the help of chat gpt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()

#usere realatet
def setup_user(email, name,gId):
    session = db.session
    try:
        # Ation
        Nuereintrag= User(useremail=email,name=name,googelid=gId,logedin=True)
        session.add(Nuereintrag)
        session.commit()  # Speichern
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
    finally:
        session.close() # Warten
def removeuser(googelid):
    session = db.session
    try:
        user = User.query.filter_by(googelid=googelid).first()
        if user:
            db.session.delete(user)
            db.session.commit()
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
    finally:
        session.close() # Warten
def isUser(gId):
    user = User.query.filter_by(googelid=gId).first()
    return user is not None

def findUser(gId):
    user = User.query.filter_by(googelid=gId).first()
    return user
def findallUser():
    all_users = User.query.all()
    return all_users


def getUser(gId):
    user = User.query.filter_by(googelid=gId).first()
    return user

def logInUserStatus(gId,status):
    session = db.session
    try:
        user = User.query.filter_by(googelid=gId).first()
        if user:
            user.logedin = status
            db.session.commit()
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
    finally:
        session.close() # Warten
def lastloginUser(gId):
     data = UserLogin.query.filter_by(googelid=gId).first()
     return data

def setUser(googelid, name):
    session = db.session
    try:
        user = User.query.filter_by(googelid=googelid).first()
        if user:
            user.name = name
            db.session.commit()
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
    finally:
        session.close() # Warten

    
#PI realatet 
def setup_pi():
    #soll einen den login token geben
    return "Sring"

def findPi(pyId):
    device = Device.query.filter_by(deviceid=pyId).first()
    return device is not None

def addPi(deviceid, devicename,connectToken):
        session = db.session
        try:
            # Ation
            device= Device(deviceid=deviceid,devicename=devicename,connectToken=connectToken,tempartur=True,humity=True,light=True,soil=True)
            session.add(device)
            session.commit()  # Speichern
        except Exception as e:
            session.rollback()  # Änderungen verwerfen
        finally:
            session.close() # Warten

def removePi(deviceid):
        session = db.session
        try:
            device = Device.query.filter_by(deviceid=deviceid).first()
            if device:
                db.session.delete(device)
                db.session.commit()
        except Exception as e:
            session.rollback()  # Änderungen verwerfen
        finally:
            session.close() # Warten

def getPi(deviceid):
    device = Device.query.filter_by(deviceid=deviceid).first()
    return device

def findallPibytoUser(gId):
    listofDvices = AccessToDevice.query.filter_by(googelid=gId).all()
    device_ids = [device.deviceid for device in listofDvices]
    return device_ids

def findallUsertoPiby(deviceid):
    listofDvices = AccessToDevice.query.filter_by(deviceid=deviceid).all()
    User_ids = [device.googelid for device in listofDvices]
    return User_ids

def mergePItonewUser(oldgoogelid, newgoogelid):
    session = db.session

    listofDviceshave = AccessToDevice.query.filter_by(googelid=newgoogelid).all()
    device_ids_have = {device.deviceid for device in listofDviceshave}

    listofDvicesget = AccessToDevice.query.filter_by(googelid=oldgoogelid).all()

    for data in listofDvicesget:
        if data.deviceid not in device_ids_have:
            try:
                data.googelid = newgoogelid
                db.session.commit()
            except Exception as e:
                session.rollback()
        else:
            try:
                db.session.delete(data)
                db.session.commit()
            except Exception as e:
                session.rollback()

    session.close()



def findallPi():
    all_device = Device.query.all()
    device_ids = [device.deviceid for device in all_device]
    return device_ids



def setPi(deviceid, devicename, tempartur, humity, light, soil):
    session = db.session
    try:
        user = Device.query.filter_by(deviceid=deviceid).first()
        if user:
            user.devicename = devicename
            user.tempartur = tempartur
            user.humity = humity
            user.light = light
            user.soil = soil
            db.session.commit()
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
    finally:
        session.close() # Warten

def get_latest_data_for_device(deviceid):
    try:
        latest_data = (
            Data.query
            .filter_by(deviceid=deviceid)
            .order_by(desc(Data.measuredtime))
            .first()
        )
        device_data = Device.query.filter_by(deviceid=deviceid).first()
        if latest_data:
            tempartur = float(latest_data.tempartur) if latest_data.tempartur is not None else None
            humity = float(latest_data.humity) if latest_data.humity is not None else None


            combined_data = {
                    'deviceid': deviceid,
                    'measuredtime': str(latest_data.measuredtime),
                    'tempartur':tempartur,
                    'humity': humity,
                    'light': latest_data.light,
                    'soil': latest_data.soil,
                    'devicename': device_data.devicename,
            }
        else:
            combined_data = {
                    'deviceid': deviceid,
                    'measuredtime': None,
                    'tempartur': None,
                    'humity': None,
                    'light': None,
                    'soil': None,
                    'devicename': device_data.devicename,
            }

    except Exception as e:
        device_data = Device.query.filter_by(deviceid=deviceid).first()
        combined_data={
                'deviceid': deviceid,
                'measuredtime': None,
                'tempartur': None,
                'humity': None,
                'light': None,
                'soil': None,
                'devicename': device_data.devicename,
        }

    return combined_data
def get_data_for_device(deviceid):
    try:
        all_daten = Data.query.filter_by(deviceid=deviceid).order_by(desc(Data.measuredtime)).all()
    except Exception as e:
        all_daten = []

    return all_daten


def storeSenseorData(deviceid,measuredtime,tempartur,humity,light,soil):
    session = db.session
    try:
        new_access = Data(deviceid=deviceid,measuredtime=measuredtime,tempartur=tempartur,humity=humity,light=light,soil=soil)
        db.session.add(new_access)
        db.session.commit()
    except Exception as e:
        session.rollback() 
    finally:
        session.close()

def isUsertoDevice(gId,piId):
    device = AccessToDevice.query.filter_by(googelid=gId,deviceid=piId).first()
    return device is not None

def adddevice(gId, piId):
    session = db.session
    try:
        new_access = AccessToDevice(googelid=gId, deviceid=piId, accesslevel=1)
        db.session.add(new_access)
        db.session.commit()

    except Exception as e:
        session.rollback() 
    finally:
        session.close()  # Close the session

def removedevice(googelid, deviceid):
    session = db.session
    try:
        access = AccessToDevice.query.filter_by(googelid=googelid, deviceid=deviceid).first()
        if access:
            db.session.delete(access)
            db.session.commit()

    except Exception as e:
        session.rollback() 
    finally:
        session.close()  # Close the session



    

# Auf bau sicher Komunikation
def allgmein(Wert):
    session = db.session
    try:
        # Ation
        Nuereintrag= Tablle(Wert1='Alpha', Wert2=15, Wert3=179)
        session.add(Nuereintrag)
        session.commit()  # Speichern
    except Exception as e:
        session.rollback()  # Änderungen verwerfen
        print(f"Fehler: {e}")
    finally:
        session.close() # Warten

class Device(db.Model):
    __tablename__ = 'devices'
    
    deviceid = db.Column(db.DECIMAL(32, 0), primary_key=True, nullable=False,autoincrement=False)
    devicename = db.Column(db.String(32), nullable=False)
    connectToken = db.Column(db.String(1024), nullable=False)
    tempartur = db.Column(db.Boolean, default=True, nullable=False)
    humity = db.Column(db.Boolean, default=True, nullable=False)
    light = db.Column(db.Boolean, default=True, nullable=False)
    soil = db.Column(db.Boolean, default=True, nullable=False)

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    measuredtime = db.Column(db.DateTime, nullable=False)
    tempartur = db.Column(db.DECIMAL(10, 2), nullable=True)
    humity = db.Column(db.DECIMAL(5, 2), nullable=True)
    light = db.Column(db.Boolean, nullable=True)
    soil = db.Column(db.Boolean, nullable=True)
    deviceid = db.Column(db.DECIMAL(32, 0), db.ForeignKey('devices.deviceid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('deviceid', 'measuredtime'),
    )
    

class User(db.Model):
    __tablename__ = 'users'

    googelid = db.Column(db.DECIMAL(32, 0), primary_key=True, nullable=False,autoincrement=False)
    useremail = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(512), nullable=False)
    logedin = db.Column(db.Boolean, default=False, nullable=False)

class AccessToDevice(db.Model):
    __tablename__ = 'accesstodevices'
    id = db.Column(db.Integer, primary_key=True)
    accesslevel = db.Column(db.Integer, default=0, nullable=False)
    googelid = db.Column(db.DECIMAL(32, 0), db.ForeignKey('users.googelid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    deviceid = db.Column(db.DECIMAL(32, 0), db.ForeignKey('devices.deviceid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('deviceid', 'googelid'),
    )
    


class UserLogin(db.Model):
    __tablename__ = 'userloging'
    id = db.Column(db.Integer, primary_key=True)
    googelid = db.Column(db.DECIMAL(32, 0), db.ForeignKey('users.googelid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    measuredtime = db.Column(db.DateTime, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('googelid', 'measuredtime'),
    )

        