import io
import struct
from dataclasses import dataclass
from .tools import (
    sign_extend_14bit,
    sign_extend_4bit,
    sign_extend_2bit,
    sign_extend_6bit,
    sign_extend_8bit,
    sign_extend_16bit,
    sign_extend_24bit 
)
from .types import FrameType, EncodingType, PredictorType, EventType


@dataclass
class FieldMeta:
    name: str = ""
    signed: bool = False
    encoding: int = 0
    predictor: int = 0

@dataclass
class Frame:
    type: FrameType
    data: list[int]

class LogReader:
    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.stream = io.BytesIO(self.data)

    def read_byte(self) -> int:
        b = self.stream.read(1)
        if not b:
            raise EOFError("End of file reached")
        return b[0]

    def read_uint32(self, endian: str = "<") -> int:
        """
        endian: 
          - < little-endian (intel)
          - > big-endian (network)
        """
        data = self.stream.read(4)
        if len(data) < 4:
            raise EOFError("End of file reached")
        return struct.unpack(f"{endian}L", data)[0]

    def tell(self) -> int:
        return self.stream.tell()

    def seek(self, pos: int) -> None:
        self.stream.seek(pos)

    def read(self, size: int) -> bytes:
        data = self.stream.read(size)
        if len(data) < size:
            raise EOFError("End of file reached")
        return data

    def peek(self, size: int) -> bytes:
        pos = self.tell()
        data = self.read(size)
        self.seek(pos)
        return data

    def peek_byte(self) -> int:
        return self.peek(1)[0]

    def read_line(self) -> str:
        return self.stream.readline().decode('ascii')

    def find(self, seq: str, start: int = 0) -> int:
        return self.data.find(seq.encode('ascii'), start)

    def len(self):
        return len(self.data)


class LogItem:
    def __init__(self, reader: LogReader, range: tuple[int, int]):
        self.reader = reader
        self.range = range
        self.headers: dict[str, str] = {}
        self.fields: dict[FrameType, list[FieldMeta]] = {}
        self.frames: list[Frame] = []
        self.parse_headers()
        self.decode_headers()
    
    def parse_headers(self):
        self.reader.seek(self.range[0])
        while True:
            start = self.reader.tell()
            tag = self.reader.read(2)
            if tag != b"H ":
                # end of headers, step back to start position as we are in log data
                self.reader.seek(start)
                break
            raw_line = self.reader.read_line()
            line = raw_line.strip()
            parts = line.split(':', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid header line: {raw_line}")
            k, v = parts[0].strip(), parts[1].strip()
            self.headers[k] = v

    def decode_headers(self):
        for k, v in self.headers.items():
            if k == "Field I name":
                self.fields[FrameType.I] = [FieldMeta(name=field) for field in v.split(",")]
                self.fields[FrameType.P] = [FieldMeta(name=field) for field in v.split(",")]
            elif k == "Field I signed":
                for field, signed in zip(self.fields[FrameType.I], v.split(",")):
                    field.signed = bool(int(signed.strip()))
                for field, signed in zip(self.fields[FrameType.P], v.split(",")):
                    field.signed = bool(int(signed.strip()))
            elif k == "Field I predictor":
                for field, predictor in zip(self.fields[FrameType.I], v.split(",")):
                    field.predictor = int(predictor.strip())
            elif k == "Field I encoding":
                for field, encoding in zip(self.fields[FrameType.I], v.split(",")):
                    field.encoding = int(encoding.strip())
                #[print(f) for f in self.fields[FrameType.I]]

            elif k == "Field P predictor":
                for field, predictor in zip(self.fields[FrameType.P], v.split(",")):
                    field.predictor = int(predictor.strip())
            elif k == "Field P encoding":
                for field, encoding in zip(self.fields[FrameType.P], v.split(",")):
                    field.encoding = int(encoding.strip())
                #[print(f) for f in self.fields[FrameType.P]]

            if k == "Field H name":
                self.fields[FrameType.H] = [FieldMeta(name=field) for field in v.split(",")]
            elif k == "Field H signed":
                for field, signed in zip(self.fields[FrameType.H], v.split(",")):
                    field.signed = bool(int(signed.strip()))
            elif k == "Field H predictor":
                for field, predictor in zip(self.fields[FrameType.H], v.split(",")):
                    field.predictor = int(predictor.strip())
            elif k == "Field H encoding":
                for field, encoding in zip(self.fields[FrameType.H], v.split(",")):
                    field.encoding = int(encoding.strip())
                #[print(f) for f in self.fields[FrameType.H]]

            if k == "Field G name":
                self.fields[FrameType.G] = [FieldMeta(name=field) for field in v.split(",")]
            elif k == "Field G signed":
                for field, signed in zip(self.fields[FrameType.G], v.split(",")):
                    field.signed = bool(int(signed.strip()))
            elif k == "Field G predictor":
                for field, predictor in zip(self.fields[FrameType.G], v.split(",")):
                    field.predictor = int(predictor.strip())
            elif k == "Field G encoding":
                for field, encoding in zip(self.fields[FrameType.G], v.split(",")):
                    field.encoding = int(encoding.strip())
                #[print(f) for f in self.fields[FrameType.G]]

            if k == "Field S name":
                self.fields[FrameType.S] = [FieldMeta(name=field) for field in v.split(",")]
            elif k == "Field S signed":
                for field, signed in zip(self.fields[FrameType.S], v.split(",")):
                    field.signed = bool(int(signed.strip()))
            elif k == "Field S predictor":
                for field, predictor in zip(self.fields[FrameType.S], v.split(",")):
                    field.predictor = int(predictor.strip())
            elif k == "Field S encoding":
                for field, encoding in zip(self.fields[FrameType.S], v.split(",")):
                    field.encoding = int(encoding.strip())
                #[print(f) for f in self.fields[FrameType.S]]

            elif k == 'looptime':
                self.looptime = int(v)
            elif k == 'I interval':
                self.i_interval = int(v)
            elif k == 'P interval':
                self.p_interval = int(v) # TODO: inav use extra denom here (1/2)
            elif k == 'P ratio':
                self.h_interval = int(v)
            elif k == 'pid_process_denom':
                self.pid_denom = int(v)

            #print(f'.{k}: {v}')

def get_log_ranges(reader: LogReader) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    first_line = reader.read_line()
    step = len(first_line)
    start = 0
    content_len = reader.len()
    while True:
        pos = reader.find(first_line, start + step)
        if pos > 0:
            ranges.append((start, pos))
        else:
            ranges.append((start, content_len))
            break
        start = pos
    return ranges

def get_logs(reader: LogReader, ranges: list[tuple[int, int]]) -> list[LogItem]:
    """
    Return a list of log items from the reader.
    Each log item is a tuple of (start, end) indices.
    """
    return [LogItem(reader, range) for range in ranges]

def load_logs(filename: str) -> list[LogItem]:
    with open(filename, "rb") as f:
        data = f.read()
        reader = LogReader(data)
        ranges = get_log_ranges(reader)
        return get_logs(reader, ranges)

class LogParser:
    def __init__(self, log: LogItem):
        self.log = log
        self.desync = False

    def load(self):
        reader = self.log.reader
        while True:
            frame_type = reader.read_byte()
            
            if self.desync:
                # if lost sync, skip all data until I frame begins
                if frame_type == ord('I'):
                    self.desync = False
                else:
                    continue

            try:
                ft = FrameType(chr(frame_type))
            
                match ft:
                    case FrameType.E:                   
                        if self.read_event_frame(reader):
                            break # end of log
                    case FrameType.I | FrameType.P | FrameType.H | FrameType.G | FrameType.S:
                        values = self.read_data_frame(reader, self.log.fields[ft])
                        self.log.frames.append(Frame(ft, values))
                    case _:
                        raise RuntimeError(f"Unhandled frame type: '{frame_type:02X} at {reader.tell() - 1}'")

            except EOFError:
                # unexpected end of file
                break

            except ValueError:
                # we lost sync or got unsupported frame type, skip everything till next I frame
                self.desync = True
                continue


    def read_data_frame(self, reader: LogReader, fields: list[FieldMeta]) -> list[int]:
        fields_iter = enumerate(fields)
        values = []
        for i, field in fields_iter:
            enc = EncodingType(field.encoding)
            match enc:
                case EncodingType.SIGNED:
                    val = self.read_signed_vb(reader)
                    values.append(val)
                case EncodingType.UNSIGNED:
                    val = self.read_unsigned_vb(reader)
                    values.append(val)
                case EncodingType.NEG14:
                    val = self.read_neg14_vb(reader)
                    values.append(val)
                case EncodingType.TAG8_8SVB:
                    val = self.read_tag8_8svb(reader, fields, i)
                    values.extend(val)
                case EncodingType.TAG2_3S32:
                    val = self.read_tag2_3s32(reader)
                    values.extend(val)
                case EncodingType.TAG8_4S16:
                    val = self.read_tag8_4s16(reader)
                    values.extend(val)
                case EncodingType.NULL:
                    val = 0
                    values.append(val)
                case EncodingType.TAG2_3SV:
                    val = self.read_tag2_3sv(reader)
                    values.extend(val)
                case _:
                    raise ValueError("unsupported encoding")
            
            if isinstance(val, list) and len(val) > 0:
                for _ in range(len(val) - 1):
                    next(fields_iter)

        return values

    def read_event_frame(self, reader: LogReader):
        # print(f'Event Frame')
        et = reader.read_byte()

        if et == EventType.SYNC_BEEP.value:
            tm = self.read_unsigned_vb(reader)
            print(f".Beep({tm})")
        elif et == EventType.FLIGHT_MODE.value:
            mode = self.read_unsigned_vb(reader)
            tm = self.read_unsigned_vb(reader)
            print(f".FlightMode({mode}, {tm})")
        elif et == EventType.DISARM.value:
            reason = self.read_unsigned_vb(reader)
            print(f".Disarm({reason})")
        elif et == EventType.INFLIGHT_ADJ.value:
            func_code = reader.read_byte()
            if func_code >= 128:
                # case for float
                func_val = struct.unpack('<f', reader.read(4))[0]
            else:
                func_val = self.read_signed_vb(reader)
            print(f".InflightAdj({func_code}, {func_val})")
        elif et == EventType.RESUME.value:
            mode = self.read_unsigned_vb(reader)
            tm = self.read_unsigned_vb(reader)
            print(f".Resume({mode}, {tm})")
        elif et == EventType.LOG_END.value:
            while True:
                b = reader.read_byte()
                if b == 0x00:
                    break
            print(".End")
            return True
        else:
            print(f"Unknown event type: {et}")

        return False

    def read_unsigned_vb(self, reader: LogReader) -> int:
        shift, result = 0, 0
        for i in range(5):
            byte = reader.read_byte()
            result = result | ((byte & ~0x80) << shift)
            if byte < 128:
                # final byte
                return result
            shift += 7

        # too long
        return 0

    def read_signed_vb(self, reader: LogReader) -> int:
        value = self.read_unsigned_vb(reader)
        # ZigZag decode
        value = ((value % 0x100000000) >> 1) ^ -(value & 1)
        return value

    def read_neg14_vb(self, reader: LogReader) -> int:
        value = self.read_unsigned_vb(reader)
        value = -sign_extend_14bit(value)
        return value

    def read_null(self, reader: LogReader) -> int:
        return 0

    def read_tag8_8svb(self, reader: LogReader, fields: list[FieldMeta], field_index: int) -> list[int]:
        # count adjacent fields with same encoding
        group_count = 1
        for field in fields[field_index + 1 : field_index + 8]:
            if field.encoding != EncodingType.TAG8_8SVB.value:
                break
            group_count += 1

        values = []
        if group_count == 1:
            # single field
            val = self.read_signed_vb(reader)
            values.append(val)
        else:
            # multiple fields
            header = reader.read_byte()
            for _ in range(group_count):
                if header & 0x01:
                    val = self.read_signed_vb(reader)
                    values.append(val)
                else:
                    values.append(0)
                header >>= 1

        return values

    def read_tag2_3s32(self, reader: LogReader) -> list[int]:
        lead = reader.read_byte()
        shifted = lead >> 6
        if shifted == 0:  # 2bit fields
            v1 = sign_extend_2bit((lead >> 4) & 0x03)
            v2 = sign_extend_2bit((lead >> 2) & 0x03)
            v3 = sign_extend_2bit(lead & 0x03)
            return [v1, v2, v3]
        elif shifted == 1:  # 4bit fields
            v1 = sign_extend_4bit(lead & 0x0F)
            lead = reader.read_byte()
            v2 = sign_extend_4bit(lead >> 4)
            v3 = sign_extend_4bit(lead & 0x0F)
            return [v1, v2, v3]
        elif shifted == 2:  # 6bit fields
            v1 = sign_extend_6bit(lead & 0x3F)
            lead = reader.read_byte()
            v2 = sign_extend_6bit(lead & 0x3F)
            lead = reader.read_byte()
            v3 = sign_extend_6bit(lead & 0x3F)
            return [v1, v2, v3]
        elif shifted == 3:  # fields are 8, 16 or 24bit
            values = []
            for _ in range(3):
                field_type = lead & 0x03
                if field_type == 0:  # 8bit
                    v1 = reader.read_byte()
                    values.append(sign_extend_8bit(v1))
                elif field_type == 1:  # 16bit
                    v1 = reader.read_byte()
                    v2 = reader.read_byte()
                    values.append(sign_extend_16bit(v1 | (v2 << 8)))
                elif field_type == 2:  # 24bit
                    v1 = reader.read_byte()
                    v2 = reader.read_byte()
                    v3 = reader.read_byte()
                    values.append(sign_extend_24bit(v1 | (v2 << 8) | (v3 << 16)))
                elif field_type == 3:  # 32bit
                    v1 = reader.read_byte()
                    v2 = reader.read_byte()
                    v3 = reader.read_byte()
                    v4 = reader.read_byte()
                    values.append(v1 | (v2 << 8) | (v3 << 16) | (v4 << 24))
                lead >>= 2
            return values
        return []

    def read_tag8_4s16(self, reader: LogReader) -> list[int]:
        selector = reader.read_byte()
        values = []
        nibble_index = 0
        buffer = 0
        for _ in range(4):
            field_type = selector & 0x03
            if field_type == 0:  # field zero
                values.append(0)
            elif field_type == 1:  # field 4bit
                if nibble_index == 0:
                    buffer = reader.read_byte()
                    values.append(sign_extend_4bit(buffer >> 4))
                    nibble_index = 1
                else:
                    values.append(sign_extend_4bit(buffer & 0x0F))
                    nibble_index = 0
            elif field_type == 2:  # field 8bit
                if nibble_index == 0:
                    values.append(sign_extend_8bit(reader.read_byte()))
                else:
                    v1 = (buffer & 0x0F) << 4
                    buffer = reader.read_byte()
                    v1 |= buffer >> 4
                    values.append(sign_extend_8bit(v1))
            elif field_type == 3:  # field 16bit
                if nibble_index == 0:
                    v1 = reader.read_byte()
                    v2 = reader.read_byte()
                    values.append(sign_extend_16bit((v1 << 8) | v2))
                else:
                    v1 = reader.read_byte()
                    v2 = reader.read_byte()
                    values.append(sign_extend_16bit(((buffer & 0x0F) << 12) | (v1 << 4) | (v2 >> 4)))
                    buffer = v2
            selector >>= 2
        return values
    
    def read_tag2_3sv(self, reader: LogReader) -> list[int]:
        raise ValueError("TAG2_3SV encoding not implementd")
