from abc import abstractmethod
from collections import defaultdict, deque
from enum import Enum
import threading

class VEHICLE_TYPE(Enum):
    CAR = "CAR"
    TRUCK = "TRUCK"
    MOTORCYCLE = "MOTORCYCLE"

class Spot:
    def __init__(self, vehicle_type: VEHICLE_TYPE):
        self.vehicle_type = vehicle_type
        self.occupied = False
        self.occupied_by = None

    def park_vehicle(self, vehicle):
        self.occupied = True
        self.occupied_by = vehicle

    def unpark_vehicle(self):
        self.occupied = False
        self.occupied_by = None
        
class ParkingLot: #singleton class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParkingLot, cls).__new__(cls)
        return cls._instance

    def __init__(self, levels: list):
        if not hasattr(self, "_initialized"):   # Guard to prevent re-init
            self.levels = levels
            self._initialized = True

    def find_spot(self, vehicle):
        for i in range(len(self.levels)):
            spot = self.levels[i].find_spot(vehicle)
            if spot:
                return (i, spot)
        return None
    
    def return_spot(self, level: int, spot: Spot):
        self.levels[level].return_spot(spot)

class Level:
    def __init__(self, spots: list):
        self.spots = spots
        self.hashmap = defaultdict(list)

        for spot in spots:
            if spot.vehicle_type not in self.hashmap:
                self.hashmap[spot.vehicle_type] = deque()
            self.hashmap[spot.vehicle_type].append(spot)

    def find_spot(self, vehicle) -> Spot:
        if vehicle.type in self.hashmap and self.hashmap[vehicle.type]:
            spot = self.hashmap[vehicle.type].popleft()
            spot.park_vehicle(vehicle)
            return spot
        return None
    
    def return_spot(self, spot: Spot) -> None:
        self.hashmap[spot.vehicle_type].append(spot)
        spot.unpark_vehicle()

class Ticket:
    def __init__(self, vehicle, level, spot, fee):
        self.vehicle = vehicle
        self.level = level
        self.spot = spot
        self.fee = fee

class Vehicle:
    def __init__(self, type: VEHICLE_TYPE, number):
        self.type = type
        self.number = number

class FeeStrategy:
    @abstractmethod
    def calculate_fee(self, vehicle_type):
        pass

class FlatFeeStrategy(FeeStrategy):
    def __init__(self, flat_fee):
        self.flat_fee = flat_fee

    def calculate_fee(self, vehicle_type):
        return self.flat_fee
    
class HourlyFeeStrategy(FeeStrategy):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate

    def calculate_fee(self, vehicle_type):
        return self.hourly_rate

class DailyFeeStrategy(FeeStrategy):
    def __init__(self, daily_fee):
        self.daily_fee = daily_fee

    def calculate_fee(self, vehicle_type):
        return self.daily_fee
    
class ParkingLotManager: #singleton class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParkingLotManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, parkingLot: ParkingLot, feeStrategy: FeeStrategy):
        if not hasattr(self, "_initialized"):  # Guard to prevent re-init
            if parkingLot:
                self.parking_lot = parkingLot
            else:
                self.parking_lot = ParkingLot([])
            self.fee_strategy = feeStrategy
            self.lock = threading.Lock()
            self._initialized = True

    def assign_parking_spot(self, vehicle):

        with self.lock:
            level, spot = self.parking_lot.find_spot(vehicle)
            if level is not None and spot is not None:
                ticket = Ticket(vehicle, level, spot, self.fee_strategy.calculate_fee(vehicle.type))
                return ticket
        
    def release_parking_spot(self, ticket):
        with self.lock:
            self.parking_lot.return_spot(ticket.level, ticket.spot)
