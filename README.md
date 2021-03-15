# VirualEngine
Simulates an engine and reports PID data over an OBD-II compliant server connection. Useful for debugging new OBD-II hardware or just generally playing around with OBD-II in comfort. 

Accepts CSV exports of HPTuners log files as data sources. The data is then loaded into the virtual engine and played back in real time

This is an internal tool for a project I am working on but figured I would share it in-case it is useful for someone else! 

Features
  - Parse and load HPTuners log file in CSV format
  - Simulate the data running by in real time
  - Query engine for a PID from the simulation data

In Progress
  - Accept OBD-II requests over network
  - Add more common PIDs
  - Web UI to control simulation parameters
  - Whatever else I need to add
