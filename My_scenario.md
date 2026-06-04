Team 6: Muhammad Aamir Ejaz Ejaz
Scenario: Forming a Truck Platoon (Setup Phase)
Participants:
•	The lead truck is operated by a human driver.
•	The following trucks operate autonomously once the platoon is established.
•	A fleet manager monitors all vehicles remotely from an off-site control location.
•	The trucks communicate through a Vehicle-to-Vehicle (V2V) communication system.
•	Both the lead truck and the following trucks rely on the V2V system to exchange operational signals.
•	The fleet manager uses the same communication infrastructure to supervise the platoon.
Pre-conditions:
•	All trucks are already travelling on the road network.
•	Each truck is equipped with interoperable V2V communication capabilities.
•	All radar units and sensor systems are fully operational.
•	The fleet manager has authorised the formation of the platoon.
Process Flow:
1.	The driver of the lead truck initiates the process by pressing the “Form Platoon” button.
2.	The lead truck sends a V2V join request to nearby compatible trucks.
3.	Each candidate truck responds with its identification details and brake system status.
4.	The system verifies whether each truck is authorised and confirms that its braking system is functioning correctly.
5.	Any unauthorised or faulty truck is excluded from the platoon formation process.
6.	The system assigns operational roles, designating the lead truck as Vehicle 1 and the following trucks as Vehicles 2, 3, 4, and so on.
7.	The required inter-vehicle gap is configured within a range of 8 to 15 metres.
8.	Cooperative Adaptive Cruise Control (CACC) is activated in all following trucks.
9.	Each truck transmits a readiness confirmation signal.
10.	The system checks that all confirmations have been received; if any truck fails to confirm, the platoon does not start.
11.	Once all checks are complete, the platoon is officially established and the following trucks enter autonomous mode.
Timing Requirements:
•	The entire setup process must be completed in less than 30 seconds.
•	Authentication of each truck must be completed within 2 seconds.
•	Any truck that fails to respond within 5 seconds is rejected from the platoon.
Post-conditions:
•	The platoon is active and operating in motion.
•	The lead driver retains full control of the convoy’s speed and direction.
•	The following trucks are operating automatically within the platoon.
•	The fleet manager can monitor the platoon status through the control dashboard.
Exceptions and Failure Conditions:
•	If a truck fails authentication, it is rejected and the platoon proceeds without it.
•	If a truck’s sensors are not functioning correctly, it cannot join until the fault has been resolved.
•	If the setup process exceeds 30 seconds, the formation procedure must be restarted.
•	If the V2V signal is too weak, the affected truck cannot join the platoon.
