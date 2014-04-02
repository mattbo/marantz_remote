''' The communications module; used to talk to the Marantz. '''

import telnetlib

#Some constants
MARANTZ_IP='192.168.1.4'
DEBUG=True

class MaremComm(object):

   def __init__(self):
       self.tn = telnetlib.Telnet(MARANTZ_IP)

   def close(self):
       self.tn.close()

   def dprint(self, *args):
       if not DEBUG: return
       print(args)

   def run_cmd(self, cmd, resp_cnt):
       #self.open_conn()
       resp = []
       cmd = cmd.encode("ascii")
       self.dprint("Sending cmd %s" % cmd)
       self.tn.read_very_eager() #clear any old stuff
       self.tn.write(cmd)
       #Some commands return several pieces of state info, so 
       # grab them all.
       for r in range(resp_cnt):
           #Strip the trailing \r
           resp.append(self.tn.read_until('\r', 1)[:-1])
           #raw = self.tn.read_until('zzr', .25)[:-1]
           #for single_raw in raw.split('\r'):
               #resp.append(single_raw)

       self.dprint("Got response %s" % resp)
       #self.close()
       return resp

   def get_state(self):
       #Note that the keys must match the field names in forms.py
       return {
            'volume': self.get_volume(),
            'speakers': self.get_spkr(),
            'source': self.get_source(),
            'surround_mode': self.get_surround_mode()
        }

   def db_to_vol(self, db):
       ''' Convert decibels (float) to a volume param
           0 corresponds to -80.0dB
           99 corresponds to +19.0dB
           Send 2 digits for whole dB steps, send 3 digits for half dB :
               MV79\r :  -1.0dB
               MV795\r : -0.5dB
               MV80\r :  +0dB
               MV805\r : +0.5dB
       '''
       vol = db + 80
       if vol < 0: vol = 0
       if vol > 99: vol = 99
       if vol % 1 == 0: vol = '%02.0f' % vol
       else:
           #any non-integer number of decibels gets rounded to .5dB
           vol = int(vol) + 0.5
           vol = '%03.0f' % (vol * 10)
       return vol

   def vol_to_db(self, vol):
       if len(vol) == 2:
           return int(vol) - 80
       #three digits means half dB steps
       return (int(vol)/10.0) - 80

   def get_volume(self):
       '''Return the current master volume in dB'''
       rv = self.run_cmd('MV?\r', 3)
       #Pull the first result, strip the MV, and convert to dB
       return self.vol_to_db(rv[0][2:])

   def set_volume(self, db):
       ''' Set the master volume to a number of decibels (.5dB precision) '''
       #Bad things happen if you try to set the volume to the current
       #setting...
       db = float(db)
       if db == self.get_volume(): return db
       rv = self.run_cmd("MV%s\r" % self.db_to_vol(db), 3)
       return self.vol_to_db(rv[0][2:])

   speakers = (('SPA', 'Living Room'), ('SPB', 'Kitchen'), ('A+B', 'Both'))

   def get_spkr(self):
       rv = self.run_cmd('PSFRONT?\r', 4)
       return rv[2][8:]

   def set_spkr(self, val):
       if val not in [x[0] for x in self.speakers]:
           raise BadValue("%s is not a valid source", src)
       rv = self.run_cmd('PSFRONT %s\r' % val, 4)
       return rv[0][7:]

   sources = (
       ('SAT', 'Roku (SAT)'), #Roku
       ('BD', 'Mac Mini (BD)'), #Mac Mini
       ('NET/USB', 'AirPlay (NET/USB)'), #Airplay
       ('TUNER', 'Tuner'),
       ('CD', 'CD'),
       ('DVD', 'DVD'),
       ('TV', 'TV'),
       ('VCR', 'VCR'),
       ('GAME', 'Game'),
       ('M-XPORT', 'M-XPort'),
       ('USB/IPOD', 'USB/Ipod'))

   def get_source(self):
       rv = self.run_cmd('SI?\r', 3)
       return rv[0][2:]

   def set_source(self, src):
       if src not in [x[0] for x in self.sources]:
           raise BadValue("%s is not a valid source", src)
       rv = self.run_cmd('SI%s\r' % src, 5)
       return rv[0][2:]

   surround_modes = (
       ('DIRECT', 'Direct'),
       ('PURE DIRECT', 'Pure Direct'),
       ('STEREO', 'Stereo'),
       ('AUTO', 'Auto-select'),
       ('DOLBY DIGITAL', 'Dolby Digital'),
       ('DOLBY', 'Dolby'),
       ('DOLBY PL2 C', 'DOLBY PLII Cinema'),
       ('DOLBY PL2 M', 'DOLBY PLII Music'),
       ('DOLBY PL2 G', 'DOLBY PLII Game'),
       ('DTS SURROUND', 'DTS Surround'),
       ('DTS NEO:6 C', 'DTS Neo:6 Cinema'),
       ('DTS NEO:6 M', 'DTS Neo:6 Music'),
       ('MCH STEREO', 'Multi-channel stereo'),
       ('VIRTUAL', 'Virtual'))

   def get_surround_mode(self):
       rv = self.run_cmd('MS?\r', 9)
       return rv[0][2:]

   def set_surround_mode(self, mode):
       if mode not in [x[0] for x in self.surround_modes]:
           raise BadValue("%s is not an available mode", mode)
       rv = self.run_cmd('MS%s\r' % mode, 9)
       return rv[1][2:]

