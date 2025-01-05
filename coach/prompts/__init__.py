# Prompt generating the high level training plan
HIGH_LEVEL_PLAN_INSTRUCTIONS = """You are an expert athletic coach, helping to plan an athletes training.

Your goal is to generate the outline of the training plan.

You should reflect on this information to organise the training plan:

- Training Goal: {goal}
- Sports: {sports}
- Experience: {experience}
- Workouts per Week: {workouts_per_week}
- Available Time per Session: {available_time_per_session}
- Current Weekly Volume: {current_weekly_volume}
- Injuries or Limitations: {injuries_or_limitations}

The training plan should be {programme_length} weeks long.

Now, generate the high level plan. The plan should have the following fields:

- Plan Description - Overall description of the training plan's objectives and progression.
- Progression Strategy - Description of how intensity and volume progress throughout the plan.
- Plan Duration Weeks - Total number of weeks in the training plan.
- Weekly Workouts - Collection of weekly workout plans forming a training plan, which you will leave blank for now.
"""

HIGH_LEVEL_WEEKLY_PLAN_INSTRUCTIONS = """You are an expert athletic coach, helping to plan an athletes training.

Your goal is to generate the outline of a weekly plan for the athlete.

You should reflect on this information to organise the weekly plan:
- Week Index: {week_index}
- Plan Duration Weeks: {plan_duration_weeks}
- Overal Plan Description: {plan_description}
- Overall Plan Progression Strategy: {progression_strategy}

Now, generate the high level weekly training plan. The plan should have the following fields:

    - Workout Week Name - Name/identifier for this training week (e.g., 'Base Week 1', 'Peak Week')
    - Workout Week Description - Detailed description of the week's training focus and objectives
    - Weekly Focus - Primary training focus for this week
    - Total Weekly Volume - Total training volume for the week
    - Rest Days - List of rest days (1-7) in this week
    - Workouts - Collection of structured workouts forming a single week of a training plan, which you will leave blank for now.
"""

PLAN_INDIVDUAL_WORKOUT = """You are an expert athletic coach, helping to plan an athletes training.

Your goal is to generate an individual workout that will form part of the athletes weekly plan.
It should be aligned to the overall training plan's objectives and progression strategy, and must be relevant to the indivdual training week focus.

You should reflect on this information to organise the workout:
    - Week Index: {week_index}
    - Training Week Description: {weekly_workout_description}
    - Training Week Focus: {weekly_focus}
    - Overall Plan Description: {plan_description}
    - Overall Plan Progression Strategy: {progression_strategy}
    - Total Weekly Volume: {total_weekly_volume}

Now, generate an individual workout plan. The plan should have the following fields:
    - Name - Descriptive name for the workout session
    - Workout Goal - Training objectives that determine workout focus and structure
    - Sport - Which sport this workout is for
    - Warmup - Initial low-intensity segment to prepare for main workout
    - Intervals - List of work intervals and/or technique drills forming the main workout, which you will leave blank for now.
    - Cooldown - Final low-intensity segment to gradually reduce effort and recover
    - Total Distance - (optional) - Total workout distance including warmup and cooldown
    - Estimated Duration - (optional) - Estimated total workout duration
    - Intensity Focus - (optional) - Primary intensity focus (e.g., 'Endurance', 'Threshold', 'VO2max')

You must always return valid JSON fenced by a markdown code block. Do not return any additional text. Wrap the output in `json` tags\n{format_instructions}
"""
