import asyncio
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from models.dependencies import Dependencies
from models.schema import WeeklyWorkout, Workout
from models.states import WeeklyWorkoutState
from prompts import HIGH_LEVEL_WEEKLY_PLAN_INSTRUCTIONS, PLAN_INDIVDUAL_WORKOUT


class WeeklyWorkoutNode:
    def __init__(self, deps: Dependencies) -> None:
        self.deps = deps

    async def generate_high_level_weekly_plan(self, state: WeeklyWorkoutState):
        # Input
        claude_3_5_sonnet = self.deps.llm_client
        current_training_plan = state["current_training_plan"]
        week_index = state["week_index"]

        # Generate high level weekly level training plan
        structured_llm = claude_3_5_sonnet.with_structured_output(WeeklyWorkout)

        # Format system instructions
        system_instructions = HIGH_LEVEL_WEEKLY_PLAN_INSTRUCTIONS.format(
            week_index=week_index,
            plan_duration_weeks=current_training_plan.plan_duration_weeks,
            plan_description=current_training_plan.plan_description,
            progression_strategy=current_training_plan.progression_strategy,
        )

        # Generate high-level training plan
        results = await structured_llm.ainvoke(
            [SystemMessage(content=system_instructions)]
            + [
                HumanMessage(
                    content="Generate a high level weekly training plan that will help in organising the individual workouts"
                ),
            ]
        )
        structured_results = cast(WeeklyWorkout, results)

        # Create list of coroutines for non-rest days
        workout_coroutines = [
            self.generate_individual_workout(state, structured_results)
            for i in range(1, 8)
            if i not in structured_results.rest_days
        ]

        # Run all workout generations concurrently
        workouts = await asyncio.gather(*workout_coroutines)
        structured_results.workouts = workouts

        structured_results.workouts = workouts

        return {"planned_workouts": [structured_results]}

    async def generate_individual_workout(
        self,
        state: WeeklyWorkoutState,
        weekly_workout: WeeklyWorkout,
    ) -> Workout:
        # Input
        claude_3_5_sonnet = self.deps.llm_client
        current_training_plan = state["current_training_plan"]
        week_index = state["week_index"]
        weekly_workout_description = weekly_workout.weekly_workout_description
        weekly_focus = weekly_workout.weekly_focus
        total_weekly_volume = weekly_workout.total_weekly_volume

        # Generate high level weekly level training plan
        # # Set up a parser + inject instructions into the prompt template.
        parser = PydanticOutputParser(pydantic_object=Workout)
        # structured_llm = claude_3_5_sonnet.with_structured_output(Workout)

        # Format system instructions
        system_instructions = PLAN_INDIVDUAL_WORKOUT.format(
            week_index=week_index,
            weekly_workout_description=weekly_workout_description,
            weekly_focus=weekly_focus,
            plan_description=current_training_plan.plan_description,
            progression_strategy=current_training_plan.progression_strategy,
            total_weekly_volume=total_weekly_volume,
            format_instructions=parser.get_format_instructions(),
        )

        # prompt_template = PromptTemplate(
        #     template=PLAN_INDIVDUAL_WORKOUT,
        #     input_variables=[
        #         "week_index"
        #         "weekly_workout_description"
        #         "weekly_focus"
        #         "plan_description"
        #         "progression_strategy"
        #         "total_weekly_volume"
        #     ],
        #     partial_variables={
        #         "format_instructions": parser.get_format_instructions()
        #     },
        # )

        prompt = ChatPromptTemplate.from_messages(
            [SystemMessage(content=system_instructions)]
            + [
                HumanMessage(content="{query}"),
            ]
        )

        # Generate workout details
        chain = prompt | claude_3_5_sonnet | parser
        results = await chain.ainvoke(
            {
                "query": "Generate an individual workout that fits with the overall training plan and placement within this training week."
            }
        )
        structured_results = cast(Workout, results)

        return structured_results
