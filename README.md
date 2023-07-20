<a name="br1"></a> 

Poznan University of Technology

Faculty of Computing and Telecommunications

Simulation Techniques

Project

Final Project Report

Mohammed ZITANI | 154705



<a name="br2"></a> 

1\. Simulation Model Scheme



<a name="br3"></a> 

2\. Objects Description

Object

Class name

Attributes | types

Description

Shawarma Store

ShawarmaStore

numberOfChickenStands int Instance to introduce

numberOfBeefStands

numberOfEmployees

wrappingTime

int

int

int

int

int

int

input parameters and

create the initial

state of the

simulation and store

output parameters

averageWaitingTime

averageStorageTime

averageFreeTime

Customer

Employee

Customer

Employee

customerId

arrival\_time

serviced\_time

int

int

int

Instance to manage

the customers

attributes

employeeId

isFree

int

Instance to manage

bool the employees

freeTime

int

attributes

MeatStand

MeatStand

meatStandId

slicedMeatQuantity

isChicken

int

int

Instance to manage

the meat stands

bool attributes

currentQuantity

storageTime

int

int



<a name="br4"></a> 

3\. Event Description

· Time Events

\- Meat Slicing (each T)

\- Customer appearance (each ts: exponential distribution)

\- Free Employee (start service+tw: wrapping time)

· Conditional Events

·

Begin of Service (if customer queue is not empty)

\- Employee Serving choice (to serve either chicken or meat queue)

\- Enough meat on the queue to make a wrap

·

Begin of Meat Slicing

\- Checking the Meat queue (Excess Meat) before slicing.

4\. Processes Description

· Customer Process

\- Start: Customer arrives

\- waits until: Customer starts service

\- End: Customer completion

· Meat Slicing Process

\- Start: Each period T.

\- waits if storedMeatQuantity==max (N)

\- End: End of Simulation



<a name="br5"></a> 

· Block Diagram



<a name="br6"></a> 

3\. Simulation Progress

Since the Simulation Technique used for the implementation is Event Scheduling,

which means that we have to manage events inside an agenda where each time we

execute the first on the sorted agenda in activation time, meaning that we execute

always the smallest value of the clock, we have three time events which are :

· Customer arrival: when executed a customer is created and added to the

customers queue (chicken or beef) and schedule the next customer arrival

event as shown in the prints resulted when running the simulation shown in

the next figure:

· Employee Freed or Employee end of service: scheduled when the conditional

event Start of Service is executed which activation time is the sum of the

current clock and wrapping time, when executed it checks the meat stands

quantity to start serving the customer, as shown in the print of the following

Figure:

· Slicing Event: scheduled each period T and when executed it checks the

cummulated quantity in meat stands if it’s smaller than the maximum allowed

quantity, as shown in the print of the following Figure:



<a name="br7"></a> 

4\. Simulation Final Result

Finally we print the most important statistics of the simulation as shown in the next

figure, we notice that the difference between the total number of clients and the

number of served client is big, and this is caused by the low frequency of slicing meat

when not enough beef meat quantity is available (beef meat stands) the customers

are not served, since it doesn’t produce enough sliced quantity to serve the clients.

5\. Random Generators description

• Exponential distribution generator: generates each time a value from an

exponential according to the inputed mean and deviation.

• Normal distribution generator: generates each time a value from a normal

according to the inputed mean and deviation.

• Bernoulli distribution generator: generates each time a value either 0 or 1 with

an equal probability (p=0.5).

6\. Initial parameters description

• Simulation Duration

• Frequency of Customer Appearance (customer appearance time)



<a name="br8"></a> 

• Frequency of meat Slicing (Slicing Period)

• number of meat stands

• number of employees


