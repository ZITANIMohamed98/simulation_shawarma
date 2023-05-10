from entities import *
from event    import *
import time

def main():
    
    startTime = time.localtime().tm_min*60+time.localtime().tm_sec  # Time of starting the simulation 
    simulationDuration = 10              # Simulation Duration in minutes
    
    print("################################# - Initializing the model - #########################################\n")
    shawarmaStore = ShawarmaStore(2, 1.1, 0.5, 2, 3, 0.5**2, 1, 3, 0.8**2, 4, 5)
    randomGenerator = RandomGenerator()
    for i in range (0, shawarmaStore.number_of_chicken_stands, 1):
        chicken_meat_stand = MeatStand("cms"+str(i), True)
        print("################################# - chicken stand cms"+str(i)+" has been created - #########################################\n")
        shawarmaStore.chicken_meat_stands.append(chicken_meat_stand)

    for i in range (0, shawarmaStore.number_of_beef_stands, 1):
        beef_meat_stand = MeatStand("bms"+str(i), True)
        print("################################# - beef stand bms"+str(i)+" has been created - #########################################\n")
        shawarmaStore.beef_meat_stands.append(beef_meat_stand) 

    for i in range (0, shawarmaStore.number_of_employees, 1):
        employee = Employee("emp"+str(i))
        print("################################# - employee emp"+str(i)+" has been created - #########################################\n")
        shawarmaStore.employees.append(employee)
    # Event Scheduling 
    slicingEvent  = Event("slicing", time.localtime().tm_min*60+time.localtime().tm_sec+shawarmaStore.slicingPeriod)
    shawarmaStore.agenda.append(slicingEvent)
    print("################################# - slicing event has been scheduled at "+str(slicingEvent.activation_time)+"- #########################################\n")
    
    while (time.localtime().tm_min*60+time.localtime().tm_sec <= (startTime+simulationDuration*60)):
        # Event Scheduling 
        customerArrivalEvent = Event("customer_arrival", time.localtime().tm_min*60+time.localtime().tm_sec+randomGenerator.expo(shawarmaStore.arrival_time_mean))
        shawarmaStore.agenda.append(customerArrivalEvent)
        print("################################# - customer Arrival event has been scheduled  at "+str(customerArrivalEvent.activation_time)+"- #########################################\n")
        # Agenda Sorting
        shawarmaStore.agenda = sorted(shawarmaStore.agenda, key=lambda p: p.activation_time)
        # Time Events Execution 
        if len(shawarmaStore.agenda)!=0:
            if round(shawarmaStore.agenda[0].activation_time) == time.localtime().tm_min*60+time.localtime().tm_sec:
                shawarmaStore.agenda[0].execute(shawarmaStore)
                print("################################# - "+str(shawarmaStore.agenda[0].event_type)+" event has been executed  at "+str(time.localtime().tm_min*60+time.localtime().tm_sec)+"- #########################################\n")
                shawarmaStore.agenda.pop(0)
            # Service Start Conditional Event Implementation
            for e in shawarmaStore.employees:
                if e.is_free:
                    e.free_time = (e.free_time+time.localtime().tm_min*60+time.localtime().tm_sec-e.freed_time)/2
                    e.is_free = False
                    p = randomGenerator.bernoulli
                    if len(shawarmaStore.chicken_queue)!=0 and len(shawarmaStore.beef_queue)!=0:
                        if p==0:
                            shawarmaStore.chicken_queue[0].departure_time = time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time
                            shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                            shawarmaStore.chicken_queue.pop(0)
                        else:
                            shawarmaStore.beef_queue[0].departure_time = time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time
                            shawarmaStore.total_waiting_time += shawarmaStore.beef_queue[0].departure_time - shawarmaStore.beef_queue[0].arrival_time
                            shawarmaStore.beef_queue.pop(0)
                        employeeFreedEvent = Event("employee_freed", time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time, e.employee_id)
                        shawarmaStore.agenda.append(employeeFreedEvent)
                        print("################################# - employee End of Service event has been scheduled  at "+str(time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time)+"- #########################################\n")
                    elif len(shawarmaStore.chicken_queue)!=0 and len(shawarmaStore.beef_queue)==0:
                        shawarmaStore.chicken_queue[0].departure_time = time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time
                        shawarmaStore.total_waiting_time += shawarmaStore.chicken_queue[0].departure_time - shawarmaStore.chicken_queue[0].arrival_time
                        shawarmaStore.chicken_queue.pop(0)
                        employeeFreedEvent = Event("employee_freed", time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time, e.employee_id)
                        shawarmaStore.agenda.append(employeeFreedEvent)
                        print("################################# - employee End of Service event has been scheduled  at "+str(time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time)+"- #########################################\n")
                    elif len(shawarmaStore.beef_queue)!=0 and len(shawarmaStore.chicken_queue)==0:
                            shawarmaStore.beef_queue[0].departure_time = time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time
                            shawarmaStore.total_waiting_time += shawarmaStore.beef_queue[0].departure_time - shawarmaStore.beef_queue[0].arrival_time
                            shawarmaStore.beef_queue.pop(0)
                            employeeFreedEvent = Event("employee_freed", time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time, e.employee_id)
                            shawarmaStore.agenda.append(employeeFreedEvent)
                            print("################################# - employee End of Service event has been scheduled  at "+str(time.localtime().tm_min*60 + time.localtime().tm_sec+shawarmaStore.wrapping_time)+"- #########################################\n")
                    elif len(shawarmaStore.beef_queue)==0 and len(shawarmaStore.chicken_queue)==0:
                        print("################################# - the customer queues are still empty  #########################################\n")
                    
        time.sleep(1) 
                
       
    shawarmaStore.total_free_time = sum(e.free_time for e in shawarmaStore.employees)/len(shawarmaStore.employees)          
    shawarmaStore.chicken_storage_time = sum(c.storage_time/simulationDuration*60 for c in shawarmaStore.chicken_meat_stands) 
    shawarmaStore.beef_storage_time = sum(b.storage_time/simulationDuration*60 for b in shawarmaStore.beef_meat_stands) 
    shawarmaStore.total_waiting_time = shawarmaStore.total_waiting_time/shawarmaStore.customer_count 


if __name__ == "__main__":
    main()