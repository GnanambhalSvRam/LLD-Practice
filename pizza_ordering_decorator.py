#Pizza Ordering System

from abc import ABC, abstractmethod

class Order(ABC): #Component Interface
    
    @abstractmethod
    def description(self):
        pass
    
    def cost(self):
        pass
    
class Pizza(Order): #Concrete Class
    
    def __init__(self, size: str):
        self.size = size
    
    def description(self) -> str:
        return f"{self.size} size Pizza"
        
    def cost(self):
        if self.size.lower() == 'small':
            return 5.0
        if self.size.lower() == 'medium':
            return 7.5
        if self.size.lower() == 'large':
            return 11.0
        
class PizzaDecorator(Order): #Decorator Interface
    
    def __init__(self, pizza: Pizza):
        self._pizza = pizza
        
    def description(self):
        return self._pizza.description()
        
    def cost(self):
        return self._pizza.cost()
        
class Cheese(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", Cheese"
        
    def cost(self):
        return self._pizza.cost() + 1.5
        
class Pepperoni(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", Pepperoni"
        
    def cost(self):
        return self._pizza.cost() + 3.0
        
class Olives(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", Olives"
        
    def cost(self):
        return self._pizza.cost() + 1.0
        
class Jalapenos(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", Jalapenos"
        
    def cost(self):
        return self._pizza.cost() + 0.5
        
class ThinCrust(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", on a Thin Crust"
        
    def cost(self):
        return self._pizza.cost() + 1.99
        
class Regular(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", on a Regular Crust"
        
    def cost(self):
        return self._pizza.cost() + 0.0
        
class Stuffed(PizzaDecorator):
    
    def description(self):
        return self._pizza.description() + ", on a Stuffed Crust"
        
    def cost(self):
        return self._pizza.cost() + 2.99
        
order = (Pepperoni(Cheese(Olives(ThinCrust(Pizza('medium'))))))
print(f'Placed an order for {order.description()}. Total amount: {order.cost()}')
