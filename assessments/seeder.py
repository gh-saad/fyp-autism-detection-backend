# myapp/seeder.py

import random
from assessments.models import AssessmentScenario, Question, RecordingStep
from datetime import timedelta

def run():
    scenarios = [
        {
            "name": "Social Interaction Test",
            "description": "Observe if the child makes regular eye contact when spoken to.",
            "img_path": "images/scenarios/social_interactions.png",
            "level": "Easy",
            "model_name": "social_interaction_model",
            "priority": "1",
        },
        {
            "name": "Response to Name",
            "description": "Call the child's name and see if they respond without visual cues.",
            "img_path": "images/scenarios/speaking.png",
            "level": "Easy",
            "model_name": "response_name_model",
            "priority": "2",
        },
        {
            "name": "Joint Attention Task",
            "description": "Point at a distant object and observe if the child follows your point.",
            "img_path": "images/scenarios/attention-to-detail.png",
            "level": "Medium",
            "model_name": "joint_attention_model",
            "priority": "3",
        },
        {
            "name": "Imitative Behavior",
            "description": "Perform simple gestures like clapping and check if the child imitates.",
            "img_path": "images/scenarios/consumer-behavior.png",
            "level": "Medium",
            "model_name": "imitative_behavior_model",
            "priority": "4",
        },
        {
            "name": "Pretend Play Observation",
            "description": "Offer toys and check if the child engages in pretend play.",
            "img_path": "images/scenarios/playtime.png",
            "level": "Medium",
            "model_name": "pretend_play_model",
            "priority": "5",
        },
        {
            "name": "Unusual Sensory Reaction",
            "description": "Introduce unusual sounds/textures and observe the child's reaction.",
            "img_path": "images/scenarios/feedback.png",
            "level": "Hard",
            "model_name": "sensory_reaction_model",
            "priority": "6",
        }
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
        "question_text": "Does the child show interest in others during interaction?",
        "question_order": "2"
    },
    {
        "question_text": "Does the child respond when called by name?",
        "question_order": "1"
    },
    {
        "question_text": "Does the child respond to different tones of voice?",
        "question_order": "2"
    },
    {
        "question_text": "Does the child follow your gestures, like pointing?",
        "question_order": "1"
    },
    {
        "question_text": "Does the child look where you look or point?",
        "question_order": "1"
    },
    {
        "question_text": "Does the child imitate simple actions like clapping?",
        "question_order": "1"
    },
    {
        "question_text": "Does the child repeat actions after watching you?",
        "question_order": "2"
    },
    {
        "question_text": "Does the child engage in pretend play with toys?",
        "question_order": "1"
    },
    {
        "question_text": "Does the child use toys in creative or symbolic ways?",
        "question_order": "2"
    },
    {
        "question_text": "Does the child show unusual responses to sensory stimuli?",
        "question_order": "1"
    },
    {
        "question_text": "Is the child overly sensitive or under-reactive to sounds or textures?",
        "question_order": "2"
    },
]


    # Optional: Clear existing questions (CAUTION: deletes all!)
    Question.objects.all().delete()

    # Link each question to a random AssessmentScenario (for demonstration)
    question_index = 0
    for scenario in scenarios:
        for _ in range(2):  # Assign 2 questions to each scenario
            q = questions[question_index]
            Question.objects.create(
                question_text=q["question_text"],
                question_order=q["question_order"],
                as_id=scenario  # Make sure this links correctly to your AssessmentScenario instance
            )
            question_index += 1

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
