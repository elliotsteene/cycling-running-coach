from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Send
from models.dependencies import Dependencies
from models.schema import TrainingPlan
from models.states import TrainingPlanState
from prompts import HIGH_LEVEL_PLAN_INSTRUCTIONS


class TrainingPlanNode:
    def __init__(self, deps: Dependencies) -> None:
        self.deps = deps

    async def generate_high_level_training_plan(
        self,
        state: TrainingPlanState,
    ):
        # Input
        claude_3_5_sonnet = self.deps.llm_client
        workouts_per_week = state["workouts_per_week"]
        training_goal = state["training_goal"]
        sports = state["sports"]
        experience = state["experience"]
        available_time_per_session = state["available_time_per_session"]
        current_weekly_volume = state["current_weekly_volume"]
        programme_length = state["programme_length"]
        injuries_or_limitations = state["injuries_or_limitations"]

        # Generate high level training plan
        structured_llm = claude_3_5_sonnet.with_structured_output(TrainingPlan)

        # Format system instructions
        system_instructions = HIGH_LEVEL_PLAN_INSTRUCTIONS.format(
            goal=training_goal.value,
            sports=sports,
            experience=experience,
            workouts_per_week=workouts_per_week,
            available_time_per_session=available_time_per_session,
            current_weekly_volume=current_weekly_volume,
            injuries_or_limitations=injuries_or_limitations,
            programme_length=programme_length,
        )

        # Generate high-level training plan
        results = await structured_llm.ainvoke(
            [SystemMessage(content=system_instructions)]
            + [
                HumanMessage(
                    content="Generate a high level training plan that will help in organising the full schedule"
                ),
            ]
        )

        structured_results = cast(TrainingPlan, results)

        return {"training_plan": structured_results}

    def initiate_weekly_workout_planning(
        self, state: TrainingPlanState
    ) -> list:
        return [
            Send(
                "plan_weekly_workouts",
                {
                    "week_index": i,
                    "current_training_plan": state["training_plan"],
                },
            )
            for i in range(1, state["programme_length"] + 1)
        ]

    async def save_to_json(self, state: TrainingPlanState):
        # Input
        current_plan = state["training_plan"]
        planned_workouts = state["planned_workouts"]

        current_plan.weekly_workouts = planned_workouts

        # Save training plan to JSON file
        with open(r"training_plan.json", "w") as f:
            json_data = current_plan.model_dump_json()
            f.write(json_data)

        return {"training_plan": current_plan}
