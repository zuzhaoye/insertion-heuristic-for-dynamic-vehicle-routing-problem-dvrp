# insertion heuristic for Dynamic Vehicle Routing Problem (DVRP)
It is an insertion heuristic designed for dynamic vehicle routing problem (DVRP) with the objective to either minimize the **total travel distance** of the fleet or to minimize the **total waiting time** of customers subject to vehicle capacity and fleet size constraint. The main logic is greedy.

## 1. Sample input:

| node | x | y | label | time |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | -1 |
| 1 | -2.57836 | -2.18999 | 1 | 0 |
| 2 | -3.68228 | -1.40857 | 1 | 1 |
| 3 | 1.848372 | 0.752895 | 1 | 2 |
| 4 | -3.0996 | 4.402963 | 1 | 3 |
| 5 | -1.55185 | -0.26079 | 1 | 4 |
| 6 | 4.211534 | -3.43579 | 2 | 0 |
| 7 | 0.169566 | -0.85443 | 2 | 1 |
| 8 | 3.137681 | 1.081198 | 2 | 2 |
| 9 | -1.42717 | -1.10393 | 2 | 3 |
| 10 | 4.045071 | -1.51968 | 2 | 4 |

Notes:
- x and y are coordinate of the node.
- 'label' 0 means depot, where all the vehicle stored at time = 0
- 'label' 1 means pick-up node
- 'label' 2 means drop-off node
- Pick-up node 1 corresponds to drop-off node 6, i.e. 1 - 6, 2 - 7, ...
- 'time' is the time at which the customer send out a request for pick-up. 
- For drop-off nodes, there is no need to put a value in 'time' column

## 2. Codes
- main_distance: for vehicle routing based on the objective to minimize **total travel distance** of the fleet
- main_waiting_time: for vehicle routing based on the objective to minimize **total waiting time** of customers
- functions: auxilary functions supporting the main function

## 3. Sample outputs
### minimizing total travel distance
![vrp_min_distance.gif](img/vrp_min_distance.gif?raw=true "Minimizing total travel distance")
### minimizing total waiting time
![vrp_min_waiting_time.gif](img/vrp_min_waiting_time.gif?raw=true "Minimizing total waiting time")

