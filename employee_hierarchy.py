'''
Employee
    - name : str
    - position : str
    - reports_to : Employee
    - direct_reports : List[Employee]
    
Department
    - name : str
    - head : Employee
    
Hub
    - employees : defaultDict(Employee)
    - head : Employee

'''

class Employee:
    
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.reports_to = None
        self.direct_reports = set()
        
    def set_manager(self, manager : Employee):
        self.reports_to = manager
        
    def add_direct_reports(self, member: Employee):
        self.direct_reports.add(member)
        
    def description(self):
        return f'{self.name}, {self.position}'
        
    def manager(self) -> Employee:
        return self.reports_to
        
    def get_senior_hierarchy(self):
        
        seniority = set()
        senior = self.reports_to
        while senior is not senior.manager():
            if senior in seniority:
                break
            seniority.add(senior)
            senior = senior.manager()
            
        return seniority
            
        
class Hub:
    
    def __init__(self):
        self.leader = None
        
    def set_leader(self, leader : Employee):
        self.leader = leader
        
    def add_subordinate(self, manager, member):
        hierarchy = manager.get_senior_hierarchy()
        if member in hierarchy:
            return "Cannot add subordinate, dependency error!"
        
        manager.direct_reports.append(member)
        if member.reports_to is not None:
            member.reports_to.direct_reports.remove(member)
            
        manager.add_direct_reports(member)
        member.reports_to = manager
        
        return f"Added {member.description()} to {manager.description()} team."
