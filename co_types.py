from enum import IntEnum, IntFlag
#from include.bt_types import *

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

class uint16_be(uint16):
    pass
    
class uint32_be(uint32):
    pass
    
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

