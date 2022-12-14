#
# Autogenerated by Thrift Compiler (0.14.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class BotErrorCode(object):
    UNKNOWN = 0
    INTERNAL_ERROR = 500
    ILLEGAL_ARGUMENT = 400
    AUTHENTICATION_FAILED = 401
    BOT_NOT_FOUND = 1
    BOT_NOT_AVAILABLE = 2
    NOT_A_MEMBER = 3

    _VALUES_TO_NAMES = {
        0: "UNKNOWN",
        500: "INTERNAL_ERROR",
        400: "ILLEGAL_ARGUMENT",
        401: "AUTHENTICATION_FAILED",
        1: "BOT_NOT_FOUND",
        2: "BOT_NOT_AVAILABLE",
        3: "NOT_A_MEMBER",
    }

    _NAMES_TO_VALUES = {
        "UNKNOWN": 0,
        "INTERNAL_ERROR": 500,
        "ILLEGAL_ARGUMENT": 400,
        "AUTHENTICATION_FAILED": 401,
        "BOT_NOT_FOUND": 1,
        "BOT_NOT_AVAILABLE": 2,
        "NOT_A_MEMBER": 3,
    }


class SquareBot(object):
    """
    Attributes:
     - botMid
     - active
     - displayName
     - profileImageObsHash
     - iconType
     - lastModifiedAt
     - expiredIn

    """


    def __init__(self, botMid=None, active=None, displayName=None, profileImageObsHash=None, iconType=None, lastModifiedAt=None, expiredIn=None,):
        self.botMid = botMid
        self.active = active
        self.displayName = displayName
        self.profileImageObsHash = profileImageObsHash
        self.iconType = iconType
        self.lastModifiedAt = lastModifiedAt
        self.expiredIn = expiredIn

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.botMid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.BOOL:
                    self.active = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.displayName = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.profileImageObsHash = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.iconType = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I64:
                    self.lastModifiedAt = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I64:
                    self.expiredIn = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('SquareBot')
        if self.botMid is not None:
            oprot.writeFieldBegin('botMid', TType.STRING, 1)
            oprot.writeString(self.botMid.encode('utf-8') if sys.version_info[0] == 2 else self.botMid)
            oprot.writeFieldEnd()
        if self.active is not None:
            oprot.writeFieldBegin('active', TType.BOOL, 2)
            oprot.writeBool(self.active)
            oprot.writeFieldEnd()
        if self.displayName is not None:
            oprot.writeFieldBegin('displayName', TType.STRING, 3)
            oprot.writeString(self.displayName.encode('utf-8') if sys.version_info[0] == 2 else self.displayName)
            oprot.writeFieldEnd()
        if self.profileImageObsHash is not None:
            oprot.writeFieldBegin('profileImageObsHash', TType.STRING, 4)
            oprot.writeString(self.profileImageObsHash.encode('utf-8') if sys.version_info[0] == 2 else self.profileImageObsHash)
            oprot.writeFieldEnd()
        if self.iconType is not None:
            oprot.writeFieldBegin('iconType', TType.I32, 5)
            oprot.writeI32(self.iconType)
            oprot.writeFieldEnd()
        if self.lastModifiedAt is not None:
            oprot.writeFieldBegin('lastModifiedAt', TType.I64, 6)
            oprot.writeI64(self.lastModifiedAt)
            oprot.writeFieldEnd()
        if self.expiredIn is not None:
            oprot.writeFieldBegin('expiredIn', TType.I64, 7)
            oprot.writeI64(self.expiredIn)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class GetSquareBotResponse(object):
    """
    Attributes:
     - squareBot

    """


    def __init__(self, squareBot=None,):
        self.squareBot = squareBot

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.squareBot = SquareBot()
                    self.squareBot.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('GetSquareBotResponse')
        if self.squareBot is not None:
            oprot.writeFieldBegin('squareBot', TType.STRUCT, 1)
            self.squareBot.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class GetSquareBotRequest(object):
    """
    Attributes:
     - botMid

    """


    def __init__(self, botMid=None,):
        self.botMid = botMid

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.botMid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('GetSquareBotRequest')
        if self.botMid is not None:
            oprot.writeFieldBegin('botMid', TType.STRING, 1)
            oprot.writeString(self.botMid.encode('utf-8') if sys.version_info[0] == 2 else self.botMid)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class BotException(TException):
    """
    Attributes:
     - errorCode
     - reason
     - parameterMap

    """


    def __init__(self, errorCode=None, reason=None, parameterMap=None,):
        super(BotException, self).__setattr__('errorCode', errorCode)
        super(BotException, self).__setattr__('reason', reason)
        super(BotException, self).__setattr__('parameterMap', parameterMap)

    def __setattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __delattr__(self, *args):
        raise TypeError("can't modify immutable instance")

    def __hash__(self):
        return hash(self.__class__) ^ hash((self.errorCode, self.reason, self.parameterMap, ))

    @classmethod
    def read(cls, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and cls.thrift_spec is not None:
            return iprot._fast_decode(None, iprot, [cls, cls.thrift_spec])
        iprot.readStructBegin()
        errorCode = None
        reason = None
        parameterMap = None
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I32:
                    errorCode = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    reason = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.MAP:
                    parameterMap = {}
                    (_ktype1, _vtype2, _size0) = iprot.readMapBegin()
                    for _i4 in range(_size0):
                        _key5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val6 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        parameterMap[_key5] = _val6
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        return cls(
            errorCode=errorCode,
            reason=reason,
            parameterMap=parameterMap,
        )

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('BotException')
        if self.errorCode is not None:
            oprot.writeFieldBegin('errorCode', TType.I32, 1)
            oprot.writeI32(self.errorCode)
            oprot.writeFieldEnd()
        if self.reason is not None:
            oprot.writeFieldBegin('reason', TType.STRING, 2)
            oprot.writeString(self.reason.encode('utf-8') if sys.version_info[0] == 2 else self.reason)
            oprot.writeFieldEnd()
        if self.parameterMap is not None:
            oprot.writeFieldBegin('parameterMap', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.parameterMap))
            for kiter7, viter8 in self.parameterMap.items():
                oprot.writeString(kiter7.encode('utf-8') if sys.version_info[0] == 2 else kiter7)
                oprot.writeString(viter8.encode('utf-8') if sys.version_info[0] == 2 else viter8)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(SquareBot)
SquareBot.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'botMid', 'UTF8', None, ),  # 1
    (2, TType.BOOL, 'active', None, None, ),  # 2
    (3, TType.STRING, 'displayName', 'UTF8', None, ),  # 3
    (4, TType.STRING, 'profileImageObsHash', 'UTF8', None, ),  # 4
    (5, TType.I32, 'iconType', None, None, ),  # 5
    (6, TType.I64, 'lastModifiedAt', None, None, ),  # 6
    (7, TType.I64, 'expiredIn', None, None, ),  # 7
)
all_structs.append(GetSquareBotResponse)
GetSquareBotResponse.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'squareBot', [SquareBot, None], None, ),  # 1
)
all_structs.append(GetSquareBotRequest)
GetSquareBotRequest.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'botMid', 'UTF8', None, ),  # 1
)
all_structs.append(BotException)
BotException.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'errorCode', None, None, ),  # 1
    (2, TType.STRING, 'reason', 'UTF8', None, ),  # 2
    (3, TType.MAP, 'parameterMap', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 3
)
fix_spec(all_structs)
del all_structs
