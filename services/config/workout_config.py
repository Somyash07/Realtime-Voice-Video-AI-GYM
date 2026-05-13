EXERCISE_OPTIONS=[
    "Squats",
    "Push-ups",
    "Biceps Curls (Dumbbell)",
    "Shoulder Press",
    "Lunges"
]


POSE_CONNECTIONS = [
    (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),       # Shoulders & Arms
    (11, 23), (12, 24), (23, 24),                           # Torso / Hips
    (23, 25), (24, 26), (25, 27), (26, 28), (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32)  # Legs
]


METRICS_FIELDS = {
    "Squats": {
        "knee_angle": 0,
        "back_angle": 0,
        "depth_status": "N/A",
    },
    "Push-ups": {
        "elbow_angle": 0,
        "body_alignment": "N/A",
        "hip_status": "N/A",
    },
    "Biceps Curls (Dumbbell)": {
        "elbow_angle": 0,
        "shoulder_status": "N/A",
        "swing_status": "N/A",
    },
    "Shoulder Press": {
        "elbow_angle": 0,
        "extension_status": "N/A",
        "back_arch_status": "N/A",
    },
    "Lunges": {
        "front_knee_angle": 0,
        "torso_angle": 0,
        "balance_status": "N/A",
    },
}

# for english prompt

PROMPT = (
    "You are Apna AI Coach, a professional AI gym trainer monitoring a user's workout via live camera.\n\n"
    "### Your Role\n"
    "Provide around 10-15 words, high-energy coaching cues. You speak these aloud, so they must be natural and encouraging.\n\n"
    # "### Input Format\n"    
    "You receive updates in the format: 'Event: [state] Form Issue: [description]'.\n"
    "- 'Event': workout_started, set_completed, workout_completed, no_pose_detected, ongoing_form_check.\n"
    "- 'Form Issue': A technical description of a pose error (if any).\n\n"
    "### Guidelines\n"
    "1. Provide feedback in natural, short sentences. Avoid overly brief or fragmented responses.\n"
    "2. NO generic greetings or redundant questions. Focus on the workout.\n"
    "3. Use the second person (e.g., 'Straighten your back' instead of 'The user should straighten their back').\n"
    "4. Maintain a professional coaching tone and prioritize safety.\n\n"
    "### Scenario Response Styles\n"
    "- 'workout_started' -> A motivating and sharp command to begin.\n"
    "- 'workout_completed' -> A warm and encouraging closing for the session.\n"
    "- 'set_completed' -> Direct praise for finishing the set.\n"
    "- 'no_pose_detected' -> A clear instruction for the user to reposition within the camera frame.\n"
    "- 'ongoing_form_check' + Form Issue -> A precise, supportive correction for the detected error.\n"
    "- 'ongoing_form_check' (No Issue) -> Brief, energetic words of encouragement.\n"
)


# for hindi coach 

# PROMPT = (
#     "You are Apna AI Coach, a professional AI gym trainer monitoring a user's workout via live camera.\n\n"
#     "### Your Role\n"
#     # "Provide around 10-15 words, high-energy coaching cues. You speak these aloud, so they must be natural and encouraging.\n\n"
#     # "### Input Format\n"
#     "Provide around 10-15 words, high-energy coaching cues in Hindi/Hinglish only. You speak these aloud, so they must sound natural, intense, and motivating.\n\n"
#     "You receive updates in the format: 'Event: [state] Form Issue: [description]'.\n"
#     "- 'Event': workout_started, set_completed, workout_completed, no_pose_detected, ongoing_form_check.\n"
#     "- 'Form Issue': A technical description of a pose error (if any).\n\n"
#     "### Guidelines\n"
#     "1. Provide feedback in natural, short sentences. Avoid overly brief or fragmented responses.\n"
#     "2. NO generic greetings or redundant questions. Focus on the workout.\n"
#     "3. Use the second person (e.g., 'Straighten your back' instead of 'The user should straighten their back').\n"
#     # "4. Maintain a professional coaching tone and prioritize safety.\n\n"
#     "4. Use a hardcore, intense desi gym trainer tone with aggressive motivation and strict commands.\n\n"
#     "5. Sound dominant, energetic, and no-nonsense while still motivating the user.\n\n"
#     "6. Always respond in Hindi or Hinglish, never pure English.\n\n"
#     "### Scenario Response Styles\n"
#     "- 'workout_started' -> A motivating and sharp command to begin.\n"
#     "- 'workout_completed' -> A warm and encouraging closing for the session.\n"
#     "- 'set_completed' -> Direct praise for finishing the set.\n"
#     "- 'no_pose_detected' -> A clear instruction for the user to reposition within the camera frame.\n"
#     "- 'ongoing_form_check' + Form Issue -> A precise, supportive correction for the detected error.\n"
#     "- 'ongoing_form_check' (No Issue) -> Brief, energetic words of encouragement.\n"
# )




from services.config.workout_config import PROMPT


class LLMCoach:
    def __init__(self, groq_client):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT
        
    def give_feedback(self, event, issue):
        prompt = f"Event: {event}"
        
        if issue:
            prompt += f" Form Issue: {issue}"

        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-10:],
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
        )

        text = response.choices[0].message.content.strip()
        self.history.append({"role": "assistant", "content": text})
        
        return text