class ShawarmaStore:
  def __init__(self, number_of_employees, wrapping_time, arrival_time_mean, number_of_chicken_stands, chicken_mean, chicken_deviation, number_of_beef_stands, beef_mean, beef_deviation, slicingPeriod, maxQ):
    
    self.number_of_employees      = number_of_employees
    self.wrapping_time            = wrapping_time
    self.arrival_time_mean        = arrival_time_mean
    self.number_of_chicken_stands = number_of_chicken_stands
    self.chicken_mean             = chicken_mean
    self.chicken_deviation        = chicken_deviation
    self.number_of_beef_stands    = number_of_beef_stands
    self.beef_mean                = beef_mean
    self.beef_deviation           = beef_deviation
    self.slicingPeriod            = slicingPeriod
    self.maxQ                     = maxQ
    self.chicken_meat_stands = []
    self.beef_meat_stands = []
    self.employees = []
    self.chicken_queue = []
    self.beef_queue = []
    self.agenda = []
    self.clock  = 0
    self.customer_count         = 0 
    self.served_customer_count         = 0 
    self.total_waiting_time     = 0
    self.chicken_storage_time     = 0
    self.beef_storage_time     = 0
    self.total_storage_time     = 0
    self.total_free_time        = 0
    
class Customer:
  def __init__(self, customer_id, arrival_time):
    self.customer_id = customer_id
    self.arrival_time = arrival_time
    self.departure_time = -1

class MeatStand:
  def __init__(self, meat_stand_id, is_chicken):
    self.meat_stand_id        = meat_stand_id
    self.sliced_meat_quantity = 0
    self.is_chicken           = is_chicken
    self.current_quantity     = 0
    self.storage_time         = 0      # sum of (quantity before adding the sliced portion * T)
    
class Employee:
  def __init__(self, employee_id):
    self.employee_id = employee_id
    self.is_free = True
    self.freed_time = 0
    self.free_time = 0
  def free_employee(self,clock):
      self.is_free = True
      self.freed_time = clock
    
    
import random
import numpy as np
class RandomGenerator:
    
    def normal(self, mean, std_deviation):
        return np.random.normal(mean, std_deviation)
    
    def expo(self, mean):
        # Generate one random value
        return np.random.exponential(scale=mean)
    
    def bernoulli(self):
        return random.randint(0, 1)

