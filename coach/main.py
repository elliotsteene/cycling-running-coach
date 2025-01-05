import asyncio

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from models.dependencies import Dependencies
from models.enums import Experience, Goal, Sport
from models.states import (
    TrainingPlanInput,
    TrainingPlanOutput,
    TrainingPlanState,
    WeeklyWorkoutInput,
    WeeklyWorkoutOutput,
    WeeklyWorkoutState,
)
from nodes.training_plan import TrainingPlanNode
from nodes.weekly import WeeklyWorkoutNode

"""
- Describe trainging plan requirements: length, aim, sports, frequency
- Plan out broad themes for training plan with 1 theme per week
- For each workout in each week, create a detailed workout schedule
- should include warm-up, drills/session, cooldown + rest days
- Brind each week, then all weeks back together
- Compile the final results
"""


def build_weekly_workout_graph(deps: Dependencies) -> StateGraph:
    node = WeeklyWorkoutNode(deps=deps)

    weekly_workout_builder = StateGraph(
        WeeklyWorkoutState,
        input=WeeklyWorkoutInput,
        output=WeeklyWorkoutOutput,
    )

    weekly_workout_builder.add_node(
        "generate_weekly_workout_plan", node.generate_high_level_weekly_plan
    )

    weekly_workout_builder.add_edge(START, "generate_weekly_workout_plan")

    return weekly_workout_builder


def build_training_plan_graph(
    deps: Dependencies, weekly_graph: StateGraph
) -> StateGraph:
    training_node = TrainingPlanNode(deps=deps)

    training_plan_builder = StateGraph(
        TrainingPlanState,
        input=TrainingPlanInput,
        output=TrainingPlanOutput,
    )

    training_plan_builder.add_node(
        "generate_high_level_plan",
        training_node.generate_high_level_training_plan,
    )
    training_plan_builder.add_node("save_to_json", training_node.save_to_json)
    training_plan_builder.add_node(
        "plan_weekly_workouts",
        weekly_graph.compile(),
    )

    training_plan_builder.add_edge(START, "generate_high_level_plan")
    training_plan_builder.add_conditional_edges(
        "generate_high_level_plan",
        training_node.initiate_weekly_workout_planning,
        ["plan_weekly_workouts"],
    )
    training_plan_builder.add_edge("plan_weekly_workouts", "save_to_json")
    training_plan_builder.add_edge("save_to_json", END)

    return training_plan_builder


async def run_coach():
    deps = Dependencies(model_name="claude-3-5-haiku-latest")

    weekly_graph = build_weekly_workout_graph(deps=deps)

    training_plan_builder = build_training_plan_graph(
        deps=deps,
        weekly_graph=weekly_graph,
    )

    graph = training_plan_builder.compile()

    input = TrainingPlanInput(
        workouts_per_week=4,
        training_goal=Goal.ENDURANCE,
        sports=(
            Sport.SWIMMING,
            Sport.RUNNING,
        ),
        experience=Experience.INTERMEDIATE,
        available_time_per_session=45,
        current_weekly_volume=0,
        programme_length=10,
        injuries_or_limitations=None,
    )

    async for event in graph.astream_events(input, version="v1"):
        kind = event["event"]
        print(f"{kind}: {event['name']}")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(run_coach())
