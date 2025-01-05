import operator
from collections.abc import Sequence
from typing import Annotated

from models.enums import Experience, Goal, Sport
from models.schema import TrainingPlan, WeeklyWorkout, Workout
from pydantic import Field, PositiveInt
from typing_extensions import TypedDict


class TrainingPlanInput(TypedDict):
    """Input parameters for generating a personalized training plan"""

    workouts_per_week: Annotated[
        int, Field(strict=True, ge=1, le=7)
    ]  # Constrained to realistic weekly frequency
    training_goal: Goal  # Primary training objective
    sports: Sequence[Sport]  # List of sports to include in plan
    experience: Experience  # Athlete experience level
    available_time_per_session: (
        int  # Time available for each training session in minutes
    )
    current_weekly_volume: (
        PositiveInt  # Current training volume in minutes/week
    )
    programme_length: Annotated[
        int, Field(strict=True, ge=1, le=12)
    ]  # Number of weeks for programme
    injuries_or_limitations: (
        Sequence[str] | None
    )  # Any physical limitations to consider


class TrainingPlanOutput(TypedDict):
    """Generated training plan and supporting information"""

    final_training_plan: str  # Detailed weekly training schedule
    total_weekly_volume: PositiveInt  # Total training minutes per week
    progression_strategy: str  # Description of how intensity/volume progress
    key_workouts_explanation: str  # Explanation of crucial sessions
    recovery_guidelines: str  # Recovery and adaptation guidelines


class TrainingPlanState(TypedDict):
    workouts_per_week: Annotated[
        int, Field(strict=True, ge=1, le=7)
    ]  # Constrained to realistic weekly frequency
    training_goal: Goal  # Primary training objective
    sports: Sequence[Sport]  # List of sports to include in plan
    experience: Experience  # Athlete experience level
    available_time_per_session: (
        int  # Time available for each training session in minutes
    )
    current_weekly_volume: (
        PositiveInt  # Current training volume in minutes/week
    )
    programme_length: Annotated[
        int, Field(strict=True, ge=1, le=12)
    ]  # Number of weeks for programme
    injuries_or_limitations: Sequence[
        str
    ]  # Any physical limitations to consider
    training_plan: TrainingPlan
    planned_workouts: Annotated[list, operator.add]


class WeeklyWorkoutState(TypedDict):
    week_index: int  # Which week in the training plan
    current_training_plan: TrainingPlan
    planned_workouts: list[WeeklyWorkout]


class WeeklyWorkoutInput(TypedDict):
    week_index: int  # Which week in the training plan
    current_training_plan: TrainingPlan


class WeeklyWorkoutOutput(TypedDict):
    planned_workouts: list[WeeklyWorkout]


class WorkoutState(TypedDict):
    workout: Workout
    completed_workouts: list[Workout]
