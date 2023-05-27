from entities import *
from event    import *
import time

def main():
    
    startTime = time.localtime().tm_min*60+time.localtime().tm_sec  # Time of starting the simulation 
    simulationDuration =   40          # Simulation Duration in minutes
    
  #  print("################################# - Initializing the model - #########################################\n")
    shawarmaStore = ShawarmaStore(2, 1.1, 0.5, 2, 3, 0.5**2, 1, 3, 0.8**2, 4, 5)
    randomGenerator = RandomGenerator()
    for i in range (0, shawarmaStore.number_of_chicken_stands, 1):
        chicken_meat_stand = MeatStand("cms"+str(i), True)
     #   print("################################# - chicken stand cms"+str(i)+" has been created - #########################################\n")
        shawarmaStore.chicken_meat_stands.append(chicken_meat_stand)

    for i in range (0, shawarmaStore.number_of_beef_stands, 1):
        beef_meat_stand = MeatStand("bms"+str(i), True)
     #   print("################################# - beef stand bms"+str(i)+" has been created - #########################################\n")
        shawarmaStore.beef_meat_stands.append(beef_meat_stand) 

    for i in range (0, shawarmaStore.number_of_employees, 1):
        employee = Employee("emp"+str(i))
      #  print("################################# - employee emp"+str(i)+" has been created - #########################################\n")
        shawarmaStore.employees.append(employee)
    # Event Scheduling 
    slicingEvent  = Event("slicing", shawarmaStore.clock+shawarmaStore.slicingPeriod)
    shawarmaStore.agenda.append(slicingEvent)
  #  print("################################# - slicing event has been scheduled at "+str(slicingEvent.activation_time)+"- #########################################\n")
    # Event Scheduling 
    customerArrivalEvent = Event("customer_arrival", shawarmaStore.clock+randomGenerator.expo(shawarmaStore.arrival_time_mean))
    shawarmaStore.agenda.append(customerArrivalEvent)
   # print("################################# - customer Arrival event has been scheduled  at "+str(shawarmaStore.clock+randomGenerator.expo(shawarmaStore.arrival_time_mean))+"- #########################################\n")
       
    while (shawarmaStore.clock <= simulationDuration):
        # Agenda Sorting
        shawarmaStore.agenda = sorted(shawarmaStore.agenda, key=lambda p: p.activation_time)
        # Time Events Execution 
        if len(shawarmaStore.agenda)!=0:
            shawarmaStore.agenda[0].execute(shawarmaStore)
           # print("################################# - "+shawarmaStore.agenda[0].event_type+" event has been executed  at "+str(shawarmaStore.clock)+"- #########################################\n")
            shawarmaStore.agenda.pop(0)
            # Service Start Conditional Event Implementation
            for e in shawarmaStore.employees:
                if e.is_free:
                    p = randomGenerator.bernoulli
                    # bernoulli distribution to decide which queue to serve
                    if len(shawarmaStore.chicken_queue)!=0 and len(shawarmaStore.beef_queue)!=0:
                        if p==0:
                            e.is_free = False
                            e.free_time += shawarmaStore.clock-e.freed_time
                            shawarmaStore.chicken_queue[0].departure_time = shawarmaStore.clock + shawarmaStore.wrapping_time
                            shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                            chickenStand = max(shawarmaStore.chicken_meat_stands, key=lambda p: p.current_quantity)
                            if(chickenStand.current_quantity>=1):
                                chickenStand.current_quantity-=1
                                shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                                shawarmaStore.chicken_queue.pop(0)
                                shawarmaStore.served_customer_count +=1
                            else:
                               print("cutomer dropped ---- not enough chicken meat")
                        else:
                            e.is_free = False
                            e.free_time += shawarmaStore.clock-e.freed_time
                            shawarmaStore.beef_queue[0].departure_time = shawarmaStore.clock+shawarmaStore.wrapping_time
                            beefStand = max(shawarmaStore.beef_meat_stands, key=lambda p: p.current_quantity)
                            if(beefStand.current_quantity>=1):
                                beefStand.current_quantity-=1
                                shawarmaStore.total_waiting_time += shawarmaStore.beef_queue[0].departure_time - shawarmaStore.beef_queue[0].arrival_time
                                shawarmaStore.beef_queue.pop(0)
                                shawarmaStore.served_customer_count +=1
                            else:
                                print("cutomer dropped ---- not enough beef meat")
                        employeeFreedEvent = Event("employee_freed", shawarmaStore.clock+shawarmaStore.wrapping_time, e.employee_id)
                        shawarmaStore.agenda.append(employeeFreedEvent)
                     #   print("################################# - employee End of Service event has been scheduled  at "+str(shawarmaStore.clock+shawarmaStore.wrapping_time)+"- #########################################\n")
                    # Chicken queue served
                    elif len(shawarmaStore.chicken_queue)!=0 and len(shawarmaStore.beef_queue)==0:
                        e.is_free = False
                        e.free_time += shawarmaStore.clock-e.freed_time
                        shawarmaStore.chicken_queue[0].departure_time = shawarmaStore.clock +shawarmaStore.wrapping_time
                        shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                        chickenStand = max(shawarmaStore.chicken_meat_stands, key=lambda p: p.current_quantity)
                        if(chickenStand.current_quantity>=1):
                                chickenStand.current_quantity-=1
                                shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                                shawarmaStore.chicken_queue.pop(0)
                                shawarmaStore.served_customer_count +=1
                        else:
                               print("cutomer dropped ---- not enough chicken meat")
                        employeeFreedEvent = Event("employee_freed", shawarmaStore.clock +shawarmaStore.wrapping_time, e.employee_id)
                        shawarmaStore.agenda.append(employeeFreedEvent)
                     #   print("################################# - employee End of Service event has been scheduled  at "+str(time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time)+"- #########################################\n")
                    # Beef queue served
                    elif len(shawarmaStore.beef_queue)!=0 and len(shawarmaStore.chicken_queue)==0:
                            e.is_free = False
                            e.free_time += shawarmaStore.clock-e.freed_time
                            shawarmaStore.beef_queue[0].departure_time = shawarmaStore.clock +shawarmaStore.wrapping_time
                            shawarmaStore.total_waiting_time += shawarmaStore.beef_queue[0].departure_time - shawarmaStore.beef_queue[0].arrival_time
                            beefStand = max(shawarmaStore.beef_meat_stands, key=lambda p: p.current_quantity)
                            if(beefStand.current_quantity>=1):
                                beefStand.current_quantity-=1
                                shawarmaStore.total_waiting_time += shawarmaStore.beef_queue[0].departure_time - shawarmaStore.beef_queue[0].arrival_time
                                shawarmaStore.beef_queue.pop(0)
                                shawarmaStore.served_customer_count +=1
                            else:
                                print("cutomer dropped ---- not enough beef meat")
                            employeeFreedEvent = Event("employee_freed", shawarmaStore.clock + shawarmaStore.wrapping_time, e.employee_id)
                            shawarmaStore.agenda.append(employeeFreedEvent)
                      #      print("################################# - employee End of Service event has been scheduled  at "+str(shawarmaStore.clock+shawarmaStore.wrapping_time)+"- #########################################\n")
                    elif len(shawarmaStore.beef_queue)==0 and len(shawarmaStore.chicken_queue)==0:
                        print("################################# - the customer queues are still empty  #########################################\n")
                    
         
                
       
    shawarmaStore.total_free_time = sum(e.free_time for e in shawarmaStore.employees)/len(shawarmaStore.employees)          
    shawarmaStore.chicken_storage_time = sum(c.storage_time/simulationDuration for c in shawarmaStore.chicken_meat_stands) 
    shawarmaStore.beef_storage_time = sum(b.storage_time/simulationDuration for b in shawarmaStore.beef_meat_stands) 
    shawarmaStore.total_waiting_time = shawarmaStore.total_waiting_time/shawarmaStore.customer_count 
   
   
    print("-----------------------Simulation Finished --------------------")
    print("-------------------------------------------------------------")
    print("-----------------------Simulation Results  --------------------")
    print("| total customer waiting time         |  ",shawarmaStore.total_waiting_time,"       | ")
    print("-------------------------------------------------------------")
    print("| total beef meat storage time         |  ",shawarmaStore.beef_storage_time,"      | ")
    print("-------------------------------------------------------------")
    print("| total chicken meat storage time         |  ",shawarmaStore.chicken_storage_time,"   | ")
    print("-------------------------------------------------------------")
    print("| Number of served customers       |  ",shawarmaStore.served_customer_count,"                      | ")
    print("-------------------------------------------------------------")
    print("| Total Number of customers       |  ",shawarmaStore.customer_count,"                              | ")
    print("-------------------------------------------------------------")
    print("| total employees Free time         |  ",shawarmaStore.total_free_time,"       |")

if __name__ == "__main__":
    main()