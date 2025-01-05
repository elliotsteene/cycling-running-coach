from typing import Union

from models.enums import DistanceUnit, EffortZone, Goal, Sport
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class Interval(BaseModel):
    """Represents a single training interval with distance and intensity parameters"""

    distance: PositiveInt = Field(
        description="Distance to cover in this interval segment"
    )
    distance_unit: DistanceUnit = Field(
        description="Unit of measurement (kilometers or meters) for the distance"
    )
    effort: EffortZone = Field(
        description="Target intensity zone (1-5) for this interval"
    )
    duration_estimate: PositiveFloat | None = Field(
        description="Estimated time to complete this interval at target effort",
        default=None,
    )
    recovery_time: PositiveFloat | None = Field(
        description="Rest/recovery time after this interval", default=None
    )


class DrillInterval(Interval):
    """Technical or form-focused training interval with specific instructions"""

    drill_description: str = Field(
        description="Specific technical exercise or form drill instructions for this interval"
    )
    equipment_needed: list[str] = Field(
        description="Any special equipment required for this drill",
        default_factory=list,
    )


class Workout(BaseModel):
    """Complete workout session including warmup, main set, and cooldown"""

    name: str = Field(description="Descriptive name for the workout session")
    sport: Sport = Field(description="Which sport this workout is for")
    warmup: Interval = Field(
        description="Initial low-intensity segment to prepare for main workout"
    )
    intervals: list[Union[Interval, DrillInterval]] = Field(
        description="Sequence of work intervals and/or technique drills forming the main workout"
    )
    cooldown: Interval = Field(
        description="Final low-intensity segment to gradually reduce effort and recover"
    )
    workout_goal: Goal = Field(
        description="Training objectives that determine workout focus and structure"
    )
    total_distance: PositiveInt | None = Field(
        description="Total workout distance including warmup and cooldown",
        default=None,
    )
    estimated_duration: PositiveInt | None = Field(
        description="Estimated total workout duration", default=None
    )
    intensity_focus: str | None = Field(
        description="Primary intensity focus (e.g., 'Endurance', 'Threshold', 'VO2max')",
        default=None,
    )


# class WorkoutPlan(BaseModel):
#     workout_plan = str
#     number_of_intervals = int


class WeeklyWorkout(BaseModel):
    """Collection of workouts forming a complete training week"""

    workouts: list[Workout] = Field(
        description="Collection of structured workouts forming a single week of a training plan"
    )
    weekly_workout_description: str = Field(
        description="Detailed description of the week's training focus and objectives"
    )
    workout_week_name: str = Field(
        description="Name/identifier for this training week (e.g., 'Base Week 1', 'Peak Week')"
    )
    total_weekly_volume: PositiveInt | None = Field(
        description="Total training volume for the week", default=None
    )
    rest_days: list[int] = Field(
        description="List of rest days (1-7) in this week", default_factory=list
    )
    weekly_focus: str | None = Field(
        description="Primary training focus for this week", default=None
    )


class TrainingPlan(BaseModel):
    """Complete training plan composed of multiple weekly workout plans"""

    weekly_workouts: list[WeeklyWorkout] = Field(
        description="Collection of weekly workout plans forming a training plan"
    )
    plan_duration_weeks: PositiveInt = Field(
        description="Total number of weeks in the training plan"
    )
    plan_description: str = Field(
        description="Overall description of the training plan's objectives and progression"
    )
    progression_strategy: str | None = Field(
        description="Description of how intensity and volume progress throughout the plan",
        default=None,
    )
