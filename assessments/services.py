import google.generativeai as genai
from django.conf import settings

def initialize_gemini():
    genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_autism_traits_with_gemini(user_answers):
    initialize_gemini()
    model_name = "gemini-1.5-flash" # Or "gemini-1.5-pro" if you need more reasoning
    model = genai.GenerativeModel(model_name)

    # Craft a very careful and specific prompt for the LLM
    prompt = f"""
    The user has provided answers to a set of questions designed to explore potential autistic traits.
    Here are their responses:
    {user_answers}

    Based ONLY on these responses, and generally understood characteristics of Autism Spectrum Disorder (ASD) (which include challenges in social communication and interaction, and restricted, repetitive patterns of behavior, interests, or activities, as outlined in diagnostic manuals like the DSM-5), please provide a neutral, informative summary.

    **CRITICAL GUIDELINES:**
    1.  **DO NOT make any form of medical diagnosis.**
    2.  **DO NOT assign a "level of autism" (Level 1, 2, or 3).**
    3.  **DO NOT use language that implies certainty about a diagnosis.**
    4.  **Clearly state that this tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.**
    5.  **Encourage the user to consult with a qualified healthcare professional (e.g., a doctor, psychologist, or developmental specialist) for an accurate assessment.**
    6.  Focus on providing general insights into how the responses might align with common characteristics sometimes associated with ASD, without confirming or denying a diagnosis.
    7.  Maintain a supportive, non-judgmental, and empathetic tone.
    8.  Suggest that the user discusses these observations with a professional.

    Example of a desired response format (adapt as needed):
    'Based on your answers, some of the patterns described, such as [mention a few specific areas like 'difficulties with back-and-forth conversation' or 'strong adherence to routines'], are sometimes observed in individuals with characteristics related to autism spectrum disorder. It's important to remember that this tool cannot provide a diagnosis. For a comprehensive evaluation and personalized guidance, we strongly recommend consulting a healthcare professional who specializes in developmental conditions.'
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for analysis: {e}")
        return "An error occurred while processing your request. Please try again later. Remember, this tool is for informational purposes only and not for diagnosis."

# Keep other functions like initialize_gemini if you use them elsewhere.