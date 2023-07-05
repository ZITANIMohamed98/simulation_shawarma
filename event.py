from entities import *
import time

class Event:
  def __init__(self, event_type, activation_time,employee_id=0):
    self.event_type = event_type
    self.employee_id = employee_id
    self.activation_time = activation_time
    
    
  def execute(self,shawarmaStore):
    # setting up time events execution function
    randomGenerator = RandomGenerator()
    if (self.event_type == "slicing"): 
        # Slicing Event Execution 
        shawarmaStore.clock = self.activation_time
        slicingEvent  = Event("slicing", shawarmaStore.clock+shawarmaStore.slicingPeriod)
        shawarmaStore.agenda.append(slicingEvent)
        print("################################# - slicing event has been scheduled at "+str(slicingEvent.activation_time)+"- #########################################\n") 
        # Slicing Event Execution       
        for chickenStand in shawarmaStore.chicken_meat_stands:
          # Checking the cummulated quantity on all chicken stands
          sum_chicken_quantity = sum(c.current_quantity for c in shawarmaStore.chicken_meat_stands)
          if sum_chicken_quantity < shawarmaStore.number_of_chicken_stands*shawarmaStore.maxQ:
            slicedQuantity = randomGenerator.normal(shawarmaStore.chicken_mean,shawarmaStore.chicken_deviation)
            if slicedQuantity<0.1:
              slicedQuantity=0.1
            chickenStand.storage_time+=chickenStand.current_quantity*shawarmaStore.slicingPeriod           # sum of (quantity before adding the sliced portion * T)
            chickenStand.current_quantity+=slicedQuantity
            print("################################# - chicken meat Stand Id "+str(chickenStand.meat_stand_id)+"- has been added by "+str(slicedQuantity)+" #########################################\n")
          else:
            print("################################# - We've reached the max cummulated quantity of chicken, we should sell some :( #########################################\n")
            break
        for beefStand in shawarmaStore.beef_meat_stands:
          # Checking the cummulated quantity on all beef stands
          sum_beef_quantity = sum(c.current_quantity for c in shawarmaStore.beef_meat_stands)
          if sum_beef_quantity < shawarmaStore.number_of_beef_stands*shawarmaStore.maxQ:
            slicedQuantity = randomGenerator.normal(shawarmaStore.beef_mean,shawarmaStore.beef_deviation)
            if slicedQuantity<0.1:
              slicedQuantity=0.1
            
            beefStand.storage_time+=beefStand.current_quantity*shawarmaStore.slicingPeriod           # sum of (quantity before adding the sliced portion * T)
            beefStand.current_quantity+=slicedQuantity
            print("################################# - beef meat Stand Id "+str(beefStand.meat_stand_id)+"- has been added by "+str(slicedQuantity)+" #########################################\n")
          else:
            print("################################# - We've reached the max cummulated quantity of beef, we should sell some :( #########################################\n")
            break
       
    elif(self.event_type == "customer_arrival"):
      # Customer Arrival Event Execution
        shawarmaStore.clock = self.activation_time
        customerArrivalEvent = Event("customer_arrival", shawarmaStore.clock+randomGenerator.expo(shawarmaStore.arrival_time_mean))
        shawarmaStore.agenda.append(customerArrivalEvent)
        print("################################# - customer Arrival event has been scheduled  at "+str(shawarmaStore.clock+randomGenerator.expo(shawarmaStore.arrival_time_mean))+"- #########################################\n")
        
        customer = Customer("cad"+str(time.localtime().tm_sec), self.activation_time)
        print("################################# - customer cad"+str(shawarmaStore.clock)+" has been created - #########################################\n")
        shawarmaStore.customer_count +=1
        p = randomGenerator.bernoulli()
        if p==0:
          shawarmaStore.chicken_queue.append(customer)
        else:
          shawarmaStore.beef_queue.append(customer)
        
    elif(self.event_type == "employee_freed"):
       # Employee Freed Event Execution
       shawarmaStore.clock = self.activation_time
       for e in shawarmaStore.employees:
         if e.employee_id == self.employee_id:
            e.free_employee(shawarmaStore.clock)
       
    
    