from enum import Enum

class EventType(Enum):
    SYNC_BEEP = 0
    INFLIGHT_ADJ = 13
    RESUME = 14
    DISARM = 15
    FLIGHT_MODE = 30
    LOG_END = 255

class FrameType(Enum):
    I = 'I' # Inter
    P = 'P' # Intra
    S = 'S' # Slow
    E = 'E' # Event
    G = 'G' # Gps
    H = 'H' # Gps home

class EncodingType(Enum):
    SIGNED = 0
    UNSIGNED = 1
    NEG14 = 3
    TAG8_8SVB = 6
    TAG2_3S32 = 7
    TAG8_4S16 = 8
    NULL = 9
    TAG2_3SV = 10

class PredictorType(Enum):
    ZERO = 0 # no prediction
    PREV = 1 # same as last frame
    STRAIGHT = 2 # slope of this and previous is the same
    AVERAGE = 3 # average of previous 2 frames
    MINTHROTTLE = 4 # same as min throttle
    MOTOR0 = 5 # same as motor 0
    INCREMENT = 6 # always increment
    HOMECOORD = 7 # home coord or no prediction
    SERVO = 8 # servo center 1500
    VBATREF = 9 # vbar reference
    LASTTIME = 10 # last time prediction
    MINMOTOR = 11 # minmotor prediction
