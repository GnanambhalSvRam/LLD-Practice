from collections import defaultdict, deque
from enum import Enum
import threading
from typing import List

class SIZE(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Package:
    def __init__(self, item: str, size: int):
        self.item = item
        self.size = size

class Code:
    def __init__(self, code: str):
        self.code = code


class Slot:
    def __init__(self, size: SIZE):
        self.occupied = False
        self.package = None
        self.code = None
        self.size = size  

    def putPackage(self, package: Package, code: Code):
        self.package = package
        self.code = code
        self.occupied = True

    def takePackage(self, user_code: Code):
        if self.occupied is False or self.code != user_code:
            return None
        
        package = self.package
        self.occupied = False
        self.package = None
        self.code = None

        return package
    
class Order:
    def __init__(self, package: Package, code: Code, slot: Slot):
        self.package = package
        self.code = code
        self.slot = slot

class Locker:
    def __init__(self, slots): #Input a list of slots
        self.slots = {
            SIZE.SMALL: deque(),
            SIZE.MEDIUM: deque(),
            SIZE.LARGE: deque()
        }
        self.packages = {}
        self.lock = threading.Lock()

        for slot in slots:
            self.slots[slot.size].append(slot)

    #utilities:
    def __generateCode(self) -> Code:
        #implement logic to generate a code
        return Code("randomCode1234")

    def __getAvailableSlot(self, package: Package) -> Slot:
        size = package.size

        if size == SIZE.LARGE:
            if self.slots[SIZE.LARGE]:
                return self.slots[SIZE.LARGE].popleft()
            
        if size == SIZE.MEDIUM:
            if self.slots[SIZE.MEDIUM]:
                return self.slots[SIZE.MEDIUM].popleft()
            else:
                return self.slots[SIZE.LARGE].popleft() if self.slots[SIZE.LARGE] else None
            
        if size == SIZE.SMALL:
            if self.slots[SIZE.SMALL]:
                return self.slots[SIZE.SMALL].popleft()
            elif self.slots[SIZE.MEDIUM]:
                return self.slots[SIZE.MEDIUM].popleft()
            else:   
                return self.slots[SIZE.LARGE].popleft() if self.slots[SIZE.LARGE] else None

    #for the delivery agent
    def placePackage(self, package: Package) -> Order:

        with self.lock:
            slot = self.__getAvailableSlot(package)
            code = self.__generateCode()
            if slot is None:
                return None
            slot.putPackage(package, code)
            self.packages[code.code] = slot
            return Order(package, code, slot)

    #for the customer
    def takePackage(self, code: Code) -> Package:
        if code.code not in self.packages:
            return None

        slot = self.packages[code.code]
        package = slot.takePackage(code)
        del self.packages[code.code]
        self.slots[slot.size].append(slot)
        return package
    

class Customer: 
    def __init__(self, name: str, lockers: List[Locker]):
        self.name = name
        self.lockers = lockers

    def collect(self, code, lockerId: int) -> Package:
        return self.lockers[lockerId].takePackage(code)
        
            
class Agent:
    def __init__(self, lockers: List[Locker]):
        self.lockers = lockers

    def deliver(self, package: Package, lockerId: int):
        locker = self.lockers[lockerId]
        order = locker.placePackage(package)

        return order if order else None
