from enum import IntEnum, IntFlag

class int8(int):    
    def __len__(self):
        return 1

class int16(int):    
    def __len__(self):
        return 2

class int32(int):    
    def __len__(self):
        return 4

class uint8(int):    
    def __repr__(self):
        self.repr = '0x{:02x}({})'.format(self, self)
        return self.repr

    def __len__(self):
        return 1

class uint16(int):    
    def __repr__(self):
        self.repr = '0x{:04x}({})'.format(self, self)
        return self.repr

    def __len__(self):
        return 2

class uint24(int):    
    def __repr__(self):
        self.repr = '0x{:06x}({})'.format(self, self)
        return self.repr

    def __len__(self):
        return 3

class uint32(int):    
    def __repr__(self):
        self.repr = '0x{:08x}({})'.format(self, self)
        return self.repr

    def __len__(self):
        return 4

class bdaddr_t(bytearray):
    def __repr__(self):
        self.repr = '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(self[5],self[4],self[3],self[2],self[1],self[0])
        return self.repr

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return 6    
        
class IntEnum8(IntEnum):    
    def __len__(self):
        return 1   

class IntEnum16(IntEnum):    
    def __len__(self):
        return 2
        
class IntFlag8(IntFlag):    
    def __len__(self):
        return 1

class IntFlag16(IntFlag):    
    def __len__(self):
        return 2

class IntFlag32(IntFlag):    
    def __len__(self):
        return 4


