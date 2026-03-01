import time
import random
import csv
from pathlib import Path
from datetime import datetime

from telemetry.models import TelemetryPacket
from backend.pod_service import get_all_pods
from tracking.default_tracks import get_track

from backend.control_service import get_control_state

LOG_FILE = Path("data/telemetry_log.csv")
SNAPSHOT_FILE = Path("data/latest_snapshot.csv")


# INITIALIZE CSV FILES TO LOG SIMULATED VALUES WHICH WILL BE USED FOR DISPLAYING AND ANALYSIS

def initialize_files():
    headers = [  #headers for the log file
        "pod_name",
        "timestamp",
        "position_m",
        "velocity",
        "current",
        "voltage",
        "levitation_gap",
        "temperature",
        "battery"
    ]

    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

    if not SNAPSHOT_FILE.exists():
        with open(SNAPSHOT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()



# WRITE HISTORY LOG

def append_log(packet: TelemetryPacket):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=packet.to_dict().keys())
        writer.writerow(packet.to_dict())



# UPDATE SNAPSHOT FILE COZ I NEED ONLY THE LATEST TELEMETRY DETAILS FROM ALL PODS .. THIS WAY I DONT HAVE TO READ THE ENTIRE LOG FILE FOR REAL TIME DATA.

def update_snapshot(packets: list):
    """
    Overwrites snapshot file with latest packet for each pod.
    """
    with open(SNAPSHOT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=packets[0].to_dict().keys())
        writer.writeheader()

        for packet in packets:
            writer.writerow(packet.to_dict())



# MAIN SIMULATION LOOP - INCLUDING SOME BASIC PHYSICS

def simulate():
    pods = get_all_pods()

    pod_states = {
        pod["name"]: {
            "position": 0.0, #from start
            "velocity": random.uniform(250, 350),
            "battery": 100.0
        }
        for pod in pods
    }

    initialize_files()

    while True:
        current_cycle_packets = []

        for pod in pods:
            
            track_id = pod["track_id"]
            track = get_track(track_id)
            track_length = track.total_length
            
            state = pod_states[pod["name"]]

            # Position update using basic physics 
            state["position"] += state["velocity"] * 0.5
            state["position"] %= track_length

            # Velocity fluctuation
            state["velocity"] += random.uniform(-2, 2)

            current = 500 + random.uniform(-20, 20)
            voltage = 600 + random.uniform(-10, 10)
            gap = 12 + random.uniform(-0.5, 0.5)
            temperature = 40 + random.uniform(-2, 2)

            state["battery"] -= 0.01
            if state["battery"] < 20:
                state["battery"] = 100

            # ----- CONTROL CONSTANTS -----
            Kp_accel = 0.08        # acceleration gain
            Kp_brake = 0.15        # stronger braking gain
            max_accel = 5.0        # m/s^2 cap
            max_brake = 8.0        # stronger brake cap
            drag_coeff = 0.002     # aerodynamic drag constant

            # -----------------------------

            desired_velocity = get_control_state(pod["name"])

            if desired_velocity is not None:

                error = desired_velocity - state["velocity"]

                # Separate gains for accel and braking
                if error > 0:
                    acceleration = Kp_accel * error
                else:
                    acceleration = Kp_brake * error

                # Acceleration cap
                if acceleration > max_accel:
                    acceleration = max_accel

                if acceleration < -max_brake:
                    acceleration = -max_brake

                # Apply acceleration
                state["velocity"] += acceleration

            # Apply drag always
            state["velocity"] -= drag_coeff * state["velocity"]

            # Prevent negative velocity
            if state["velocity"] < 0:
                state["velocity"] = 0

            packet = TelemetryPacket(
                pod_name=pod["name"],
                timestamp=datetime.utcnow().timestamp(),
                position_m=state["position"],
                velocity=state["velocity"],
                current=current,
                voltage=voltage,
                levitation_gap=gap,
                temperature=temperature,
                battery=state["battery"]
            )

            append_log(packet)
            current_cycle_packets.append(packet)

        update_snapshot(current_cycle_packets)

        time.sleep(0.5)


if __name__ == "__main__":
    simulate()

