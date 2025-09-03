#Decorator Pattern

'''
Component
Concrete Component | Decorator Component
Concrete Decorator Components
'''

from abc import ABC, abstractmethod

#1. Base Component
class Coffee(ABC):
    
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass
    
#2. Concrete Component 
class PlainCoffee(Coffee):
    
    def cost(self) -> float:
        return 5.0
        
    def description(self) -> str:
        return "Plain Coffee"
        
# order1 = PlainCoffee()
# print(f'Order 1: {order1.description()} for ${order1.cost()}')

#3. Decorator Component
class CoffeeDecorator(Coffee):
    
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
        
    def cost(self) -> float:
        return self._coffee.cost()
        
    def description(self) -> str:
        return self._coffee.description()
        
#4. Concrete Decorator Components
class MilkDecorator(CoffeeDecorator):
    
    def cost(self) -> float:
        return self._coffee.cost() + 2.0
        
    def description(self) -> str:
        return self._coffee.description() + ", Milk"
        
class CaramelDecorator(CoffeeDecorator):
    
    def cost(self) -> float:
        return self._coffee.cost() + 4.0
        
    def description(self) -> str:
        return self._coffee.description() + ", Caramel"
        
class SeaSaltDecorator(CoffeeDecorator):
    
    def cost(self) -> float:
        return self._coffee.cost() + 3.0
        
    def description(self) -> str:
        return self._coffee.description() + ", Sea Salt"
    
order1 = SeaSaltDecorator(MilkDecorator(PlainCoffee()))
print(f'Order 1: {order1.description()} for ${order1.cost()}')


