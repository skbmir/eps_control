# eps_control
Electronic Power System control package for ROS

## Nodes

### eps_control_node.py

#### Parameters:
* ~port : string - serial port of EPS, default: /dev/ttyUSB0
* ~baud_rate : int - EPS serial communication baud rate, default: 3000000
* ~steering_rate : int - EPS steering rate in [0, 100] range, default: 10
* ~telemetry_period : float - telemetry request period in seconds, default: 0.2
* ~max_steering_angle : float - maximum steering angle of vehicle, default: 32
* ~max_eps_position : int - maximum EPS position, default: 1500
* ~middle_eps_position : int - middle EPS position, default: 1000
