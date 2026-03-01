# Hyperloop Operations System

A modular real-time monitoring dashboard for a simulated Hyperloop
network. Built using Streamlit with a clean separation between UI,
backend services, telemetry simulation, and track modeling.

## ONE SMALL NOTE : I WAS MAINLY FOCUSED ON FUNCTIONALITY AND SIMULATIONS MIMICING REAL SYSTEMS SO THAT IT CAN BE INTEGRATED INTO ONE EASILY LATER. UI CAN BE DEVELOPED FURTHER TO LOOK GOOD. I FOCUSED ON MODULARITY AND FUNCTIONALITY MAINLY WITH A LOT OF EFFORS INTO MAKING THIS TRACK MODEL AND LIVE MAP
------------------------------------------------------------------------

## 1. Project Overview

This system simulates a Hyperloop fleet and provides:

-   Role-based login (Viewer, Operator, Controller)
-   Real-time telemetry streaming ( With some physics)
-   Live map tracking with pod following
-   Weather risk integration
-   Safety limit computation
-   Centralized alert panel
-   Real geographic track modeling using Haversine distance
-   Modular backend architecture

Currently, the system focuses on monitoring (Viewer role) and operating the pod ( Operator role). Controller features are under development.

------------------------------------------------------------------------

## 2. Project Structure

Project root directory:

hyperloop_system
│   ├── analysis
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── safety_limits.py
│   ├── app.py
│   ├── backend
│   │   ├── auth_service.py
│   │   ├── control_service.py
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── lock_service.py
│   │   ├── pod_service.py
│   │   ├── __pycache__
│   │   ├── session_service.py
│   │   ├── telemetry_service.py
│   │   └── user_service.py
│   ├── data
│   │   ├── latest_snapshot.csv
│   │   ├── telemetry_log.csv
│   │   └── users.db
│   ├── __init__.py
│   ├── integration
│   │   ├── energy_tips.py
│   │   ├── fun_facts.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── weather.py
│   │   └── weather_test.py
│   ├── __pycache__
│   │   └── __init__.cpython-312.pyc
│   ├── README.md
│   ├── requirements.txt
│   ├── setup.py
│   ├── telemetry
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── __pycache__
│   │   └── simulator.py
│   ├── test_auth.py
│   ├── tracking
│   │   ├── default_tracks.py
│   │   ├── __init__.py
│   │   ├── mapper.py
│   │   ├── __pycache__
│   │   ├── track_model.py
│   │   └── waypoint.py
│   └── venv
│       ├── bin
│       ├── etc
│       ├── include
│       ├── lib
│       ├── lib64 -> lib
│       ├── pyvenv.cfg
│       └── share
├── notes.txt
└── paho-mqtt_communication
    ├── mqtt.png
    ├── publisher.py
    └── subscriber.py

33 directories, 52 files

All commands must be executed from the project root directory:

cd hyperloop_system

------------------------------------------------------------------------

## 3. Setup Instructions

Even if a venv folder exists, creating a fresh virtual environment is
recommended.

Step 1: Navigate to project root

cd hyperloop_system

Step 2: Create virtual environment

python3 -m venv venv

Step 3: Activate virtual environment

Linux / macOS: source venv/bin/activate

Windows: venv`\Scripts`{=tex}`\activate`{=tex}

Step 4: Install dependencies

pip install -r requirements.txt
------------------------------------------------------------------------

## 4. Running the Application

From the project root directory:
First run this command :

python3 setup.py 

This initializes the required database , users and pods .. this is crucial 

streamlit run app.py

Also open a new terminal in the same directory and activate venv... 
Now run the following command to run the simulator . THIS IS VERY VERY IMPORTANT IF YOU FORGET THEN DATA WONT BE GENERATED ... LEADING TO SOME ERRORS WHICH ARENT HANDLED CURRENTLY ( LIKE NONETYPE ERRORS )

PLS RUN THIS IN THE NEW TERMINAL 

python3 -m telemetry.simulator 

The application will start and display a local URL in the terminal.

------------------------------------------------------------------------

## 5. Database Structure

The system uses SQLite for authentication.

Database location: data/users.db

Users Table Schema:

users id INTEGER PRIMARY KEY username TEXT password TEXT role TEXT
pods td INTEGER PRIMARY KEY name TEXT track_id TEXT ststus TEXT
operator_sessions

Default Accounts:

-   viewer1
-   operator1
-   controller1

For now use:

Username: viewer1 Password: viewerpass   for Viewer account
and
Username: operator1 Password: operatorpass   for Operator account

Viewer dashboard is almost fully functional at this stage and the Operator dashboard is also pretty functional with limited speed control.

Dynamic user creation is not yet implemented.

------------------------------------------------------------------------
## 6. Pods and Tracks

Pods and tracks are currently statically defined.

Each pod includes: - name - status - track_id

Dynamic creation of pods, tracks, and waypoints is not yet supported.
These will be integrated into the Controller UI in future updates.

------------------------------------------------------------------------

## 7. Real Track Modeling

Tracks are defined using multiple geographic waypoints.

Waypoint Structure:

Waypoint(lat: float, lon: float)

Each track is constructed using: - Waypoint class - TrackModel class

TrackModel computes: - Distance between consecutive waypoints -
Cumulative segment distances - Total track length in meters -
Interpolated coordinates for any position along the track

------------------------------------------------------------------------

## 8. Distance Scaling Using Haversine Formula

The system uses the Haversine formula to compute real Earth-surface
distance between waypoints.

This enables:  Accurate geographic scaling , Realistic track length
measurement , Proper interpolation along curved paths , Foundation for
ETA and energy modeling which will be integrated in future.

Distance is calculated in metres using Earth radius approximation.

------------------------------------------------------------------------

## 9. Creating Realistic Curved Tracks

Tracks can be made more realistic by: - Adding multiple intermediate
waypoints - Using real GPS coordinates between cities - Increasing
waypoint density for smoother curves

Because interpolation is based on cumulative geographic distance,
curvature is preserved automatically as the number of waypoints increase.

------------------------------------------------------------------------

## 10. Weather and Safety System

Weather risk is computed per track using midpoint sampling ( 3 samples in total).

Safety limits are calculated using:  Current velocity , Weather risk ,
Operational thresholds

Alerts are centralized and displayed in a dedicated dashboard panel.

------------------------------------------------------------------------

## 11. Telemetry Simulation

Telemetry simulation is implemented in:

telemetry/simulator.py

It generates: - Velocity - Battery level - Position along track -
Current - Levitation gap

The simulator respects real track length using TrackModel.total_length.

ALSO THE SIMULATOR GENERATES VELOCITY VALUE BASED ON A PROPORTIONAL FEEDBACK CONTROLLER TO MIMIC PHYSICS ... IN THIS CASE P CONTROLLER IS ENOUGH AS THERE IS NO INERTIA .. JUST SIMULATIONS

------------------------------------------------------------------------

## 12. Current Limitations

The following features are not yet implemented:

-   Dynamic user creation
-   Dynamic pod creation
-   Dynamic track creation
-   Waypoint editing from UI
-   Database-driven fleet management
-   Controller fleet-wide analytics dashboard
-   The operator locking system should be strengthened further
-   Direct weather updates should be displayed in a separate page ... currently its used only internally to compute safe speeds 


These will be integrated in future updates.

------------------------------------------------------------------------

## 13. Scalability and Architecture

The system is modular:

-   backend/ handles services and data access
-   tracking/ handles geometry and interpolation
-   integration/ handles external logic and apis
-   analysis/ handles safety computations

This architecture allows future integration with:

-   FastAPI backend ( which im hugely interested in and i think will be a better architecture )
-   MQTT telemetry ingestion
-   Distributed systems -- dont need to run all these systems on same computer which will be helpful in future
-   Production databases

------------------------------------------------------------------------

## 14. Planned Enhancements

Upcoming improvements include:

-   Controller fleet overview
-   Dynamic entity management
-   ETA calculation
-   Energy consumption modeling
-   Realistic pod wear simulation

------------------------------------------------------------------------

## 15. Summary

This project demonstrates:

-   Modular system design
-   Real-time dashboard development
-   Geographic modeling using Haversine distance
-   Role-based authentication
-   Clean dashboard UI architecture
-   Backend-ready scalable structure

The system is designed to evolve into a realistic Hyperloop monitoring
and control platform.
