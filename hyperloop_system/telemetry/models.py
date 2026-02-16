from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelemetryPacket: # THIS IS THE DATA CLASS OF THE TELEMETRY PACKET ... EACH PACKET WILL BE AN INSTANCE OF THIS CLASS
    pod_name: str
    timestamp: float
    position_m: float
    velocity: float
    current: float
    voltage: float
    levitation_gap: float
    temperature: float
    battery: float

    def to_dict(self):
        return {
            "pod_name": self.pod_name,
            "timestamp": self.timestamp,
            "position_m": self.position_m,
            "velocity": self.velocity,
            "current": self.current,
            "voltage": self.voltage,
            "levitation_gap": self.levitation_gap,
            "temperature": self.temperature,
            "battery": self.battery
        }

