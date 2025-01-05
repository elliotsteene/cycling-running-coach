from enum import Enum


class EffortZone(Enum):
    ZONE1 = 1  # Recovery/Easy
    ZONE2 = 2  # Endurance/Aerobic
    ZONE3 = 3  # Tempo/Threshold
    ZONE4 = 4  # Interval/VO2max
    ZONE5 = 5  # Sprint/Anaerobic


class DistanceUnit(Enum):
    KM = "KILOMETERS"  # Kilometers for longer distances
    M = "METERS"  # Meters for shorter distances/intervals


class Goal(Enum):
    """Training objectives that determine workout focus and structure"""

    ENDURANCE = "ENDURANCE"  # Long distance, aerobic fitness
    SPEED = "SPEED"  # High intensity, anaerobic power
    RECOVERY = "RECOVERY"  # Active recovery, injury prevention
    THRESHOLD = "THRESHOLD"  # Lactate threshold improvement
    BASE = "BASE"  # Building aerobic base
    TECHNIQUE = "TECHNIQUE"  # Build technique


class Experience(Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    ELITE = "ELITE"


class Sport(Enum):
    """Supported sports for training plans"""

    CYCLING = "CYCLING"
    RUNNING = "RUNNING"
    SWIMMING = "SWIMMING"
    TRIATHLON = "TRIATHLON"
