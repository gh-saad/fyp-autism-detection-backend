# myapp/seeder.py

import random
from assessments.models import AssessmentScenario, Question, RecordingStep
from datetime import timedelta

def run():
    scenarios = [
        {
            "name": "Social Interaction Test",
            "description": "Observe if the child makes regular eye contact when spoken to.",
            "img_path": "images/scenarios/social_interaction.jpg",
            "level": "Easy",
            "model_name": "social_interaction_model",
            "priority": "1",
        },
        {
            "name": "Response to Name",
            "description": "Call the child's name and see if they respond without visual cues.",
            "img_path": "images/scenarios/response_to_name.jpg",
            "level": "Easy",
            "model_name": "response_name_model",
            "priority": "2",
        },
        {
            "name": "Joint Attention Task",
            "description": "Point at a distant object and observe if the child follows your point.",
            "img_path": "images/scenarios/joint_attention.jpg",
            "level": "Medium",
            "model_name": "joint_attention_model",
            "priority": "3",
        },
        {
            "name": "Imitative Behavior",
            "description": "Perform simple gestures like clapping and check if the child imitates.",
            "img_path": "images/scenarios/imitative_behavior.jpg",
            "level": "Medium",
            "model_name": "imitative_behavior_model",
            "priority": "4",
        },
        {
            "name": "Pretend Play Observation",
            "description": "Offer toys and check if the child engages in pretend play.",
            "img_path": "images/scenarios/pretend_play.jpg",
            "level": "Medium",
            "model_name": "pretend_play_model",
            "priority": "5",
        },
        {
            "name": "Unusual Sensory Reaction",
            "description": "Introduce unusual sounds/textures and observe the child's reaction.",
            "img_path": "images/scenarios/sensory_reaction.jpg",
            "level": "Hard",
            "model_name": "sensory_reaction_model",
            "priority": "6",
        },
        {
            "name": "Repetitive Behavior Monitoring",
            "description": "Watch for repetitive movements like hand flapping or rocking.",
            "img_path": "images/scenarios/repetitive_behavior.jpg",
            "level": "Hard",
            "model_name": "repetitive_behavior_model",
            "priority": "7",
        },
        {
            "name": "Language and Communication",
            "description": "Initiate conversation and assess back-and-forth communication ability.",
            "img_path": "images/scenarios/language_communication.jpg",
            "level": "Medium",
            "model_name": "language_communication_model",
            "priority": "8",
        },
        {
            "name": "Emotional Response to Situations",
            "description": "Pretend scenarios like hurting yourself and observe emotional responses.",
            "img_path": "images/scenarios/emotional_response.jpg",
            "level": "Hard",
            "model_name": "emotional_response_model",
            "priority": "9",
        },
        {
            "name": "Routine Change Tolerance",
            "description": "Change a small routine and observe if the child shows distress.",
            "img_path": "images/scenarios/routine_change.jpg",
            "level": "Hard",
            "model_name": "routine_change_model",
            "priority": "10",
        },
    ]

    # Optional: Clear previous entries (WARNING: will delete all existing!)
    AssessmentScenario.objects.all().delete()

    # Insert new scenarios
    for scenario in scenarios:
        AssessmentScenario.objects.create(
            name=scenario["name"],
            description=scenario["description"],
            img_path=scenario["img_path"],
            level=scenario["level"],
            model_name=scenario["model_name"],
            priority=scenario["priority"]
        )

    print(f"✅ Seeded {len(scenarios)} Assessment Scenarios successfully.")


    # Retrieve all AssessmentScenario objects for linking
    scenarios = AssessmentScenario.objects.all()

    questions = [
        {
            "question_text": "Does the child make regular eye contact?",
            "question_order": "1"
        },
        {
            "question_text": "Does the child respond when called by name?",
            "question_order": "2"
        },
        {
            "question_text": "Does the child follow your gestures, like pointing?",
            "question_order": "3"
        },
        {
            "question_text": "Does the child imitate simple actions like clapping?",
            "question_order": "4"
        },
        {
            "question_text": "Does the child engage in pretend play with toys?",
            "question_order": "5"
        },
        {
            "question_text": "Does the child show unusual responses to sensory stimuli?",
            "question_order": "6"
        },
        {
            "question_text": "Does the child show repetitive behaviors, like hand flapping?",
            "question_order": "7"
        },
        {
            "question_text": "Can the child hold a basic conversation or exchange words?",
            "question_order": "8"
        },
        {
            "question_text": "Does the child respond with empathy when someone is hurt?",
            "question_order": "9"
        },
        {
            "question_text": "Does the child show distress when there is a change in routine?",
            "question_order": "10"
        },
    ]

    # Optional: Clear existing questions (CAUTION: deletes all!)
    Question.objects.all().delete()

    # Link each question to a random AssessmentScenario (for demonstration)
    for q in questions:
        scenario = random.choice(scenarios)  # Link to a random AssessmentScenario
        
        Question.objects.create(
            question_text=q["question_text"],
            question_order=q["question_order"],
            as_id=scenario
        )

    print(f"✅ Seeded {len(questions)} questions successfully.")

    # Retrieve all AssessmentScenario objects for linking
    scenarios = AssessmentScenario.objects.all()

    questions = [
        {
            "question_text": "Does the child make regular eye contact?",
            "question_order": "1"
        },
        {
            "question_text": "Does the child respond when called by name?",
            "question_order": "2"
        },
        {
            "question_text": "Does the child follow your gestures, like pointing?",
            "question_order": "3"
        },
        {
            "question_text": "Does the child imitate simple actions like clapping?",
            "question_order": "4"
        },
        {
            "question_text": "Does the child engage in pretend play with toys?",
            "question_order": "5"
        },
        {
            "question_text": "Does the child show unusual responses to sensory stimuli?",
            "question_order": "6"
        },
        {
            "question_text": "Does the child show repetitive behaviors, like hand flapping?",
            "question_order": "7"
        },
        {
            "question_text": "Can the child hold a basic conversation or exchange words?",
            "question_order": "8"
        },
        {
            "question_text": "Does the child respond with empathy when someone is hurt?",
            "question_order": "9"
        },
        {
            "question_text": "Does the child show distress when there is a change in routine?",
            "question_order": "10"
        },
    ]

    # Optional: Clear existing questions (CAUTION: deletes all!)
    Question.objects.all().delete()

    # Link each question to a random AssessmentScenario (for demonstration)
    for q in questions:
        scenario = random.choice(scenarios)  # Link to a random AssessmentScenario
        
        Question.objects.create(
            question_text=q["question_text"],
            question_order=q["question_order"],
            as_id=scenario
        )

    print(f"✅ Seeded {len(questions)} questions successfully.")

    # Seeder for RecordingStep
    RecordingStep.objects.all().delete()

    # Example steps for each scenario (customize as needed)
    step_templates = [
        {
            "number": 1,
            "name": "Preparation",
            "description": "Prepare the environment and ensure the child is comfortable.",
            "img_path": "images/steps/preparation.jpg",
            "expected_duration": "00:01:00",
        },
        {
            "number": 2,
            "name": "Instruction",
            "description": "Explain the task to the child in simple terms.",
            "img_path": "images/steps/instruction.jpg",
            "expected_duration": "00:00:30",
        },
        {
            "number": 3,
            "name": "Observation",
            "description": "Observe and record the child's behavior during the task.",
            "img_path": "images/steps/observation.jpg",
            "expected_duration": "00:02:00",
        },
    ]


    total_steps_created = 0
    for scenario in scenarios:
        for step in step_templates:
            RecordingStep.objects.create(
                as_id=scenario,
                number=step["number"],
                name=step["name"],
                description=step["description"],
                img_path=step["img_path"],
                expected_duration=timedelta(
                    minutes=int(step["expected_duration"].split(":")[1]),
                    seconds=int(step["expected_duration"].split(":")[2])
                ),
            )
            total_steps_created += 1

    print(f"✅ Seeded {total_steps_created} Recording Steps successfully.")
