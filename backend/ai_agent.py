import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class AIAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GOOGLE_API_KEY not found in environment variables.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')

    def is_configured(self):
        return self.model is not None

    async def detect_intent(self, message: str, previous_messages: list = None) -> str:
        """
        Determines the user's intent from the message using Gemini.
        Returns one of: study_planning, practice_questions, stress_relief, general_chat
        """
        if not self.model:
            return "general_chat" # Fallback

        prompt = f"""
        Analyze the following user message and classify the intent into EXACTLY ONE of these categories:
        - study_planning (if the user wants a schedule, plan, timetable, or advice on how to study)
        - practice_questions (if the user wants a quiz, specific questions, or to test their knowledge)
        - stress_relief (if the user expresses anxiety, stress, or asks for motivation)
        - general_chat (for greetings, thanks, or unclear queries)

        User Message: "{message}"
        
        Return ONLY the category name.
        """
        
        try:
            response = self.model.generate_content(prompt)
            intent = response.text.strip().lower()
            valid_intents = ["study_planning", "practice_questions", "stress_relief", "general_chat"]
            if intent not in valid_intents:
                return "general_chat"
            return intent
        except Exception as e:
            print(f"Error checking intent: {e}")
            return "general_chat"

    async def generate_response(self, message: str, context: str = "") -> str:
        """
        Generates a natural language response.
        """
        if not self.model:
            return "I need a Google API Key to think! Please configure it."

        prompt = f"""
        You are StudyBot, a helpful and empathetic study companion.
        Context: {context}
        User says: "{message}"
        
        Provide a helpful, encouraging, and concise response. Use Markdown for formatting.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    async def generate_study_plan(self, student_data: dict) -> str:
        """
        Generates a personalized study plan based on student data.
        """
        if not self.model:
            return "Cannot generate plan without API key."

        prompt = f"""
        Create a detailed, motivational study plan for a student with the following profile:
        - Education Level: {student_data.get('education_level', 'Unknown')}
        - Number of Subjects: {student_data.get('subjects_count', 'Unknown')}
        - Available Study Hours/Day: {student_data.get('study_hours', 'Unknown')}
        - Time until Exams: {student_data.get('exam_timeline', 'Unknown')}
        - Study Habit: {student_data.get('study_habit', 'Unknown')}

        Output a structured plan in Markdown. 
        formatting rules:
        - Use `##` for main sections.
        - Use `###` for subsections.
        - Use `-` for bullet points.
        - **IMPORTANT**: Add empty lines between paragraphs and sections for readability.
        - Bold important keywords using `**text**`.
        - Use emojis to make it engaging.

        Include:
        1. A motivating intro.
        2. A strategy based on their timeline.
        3. A proposed daily schedule split into sessions.
        4. Specific advice for their study habit.
        
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Sorry, I couldn't generate a plan right now."

    async def generate_practice_questions(self, topic: str) -> str:
        if not self.model:
            return "Cannot generate questions without API key."

        prompt = f"""
        Generate 3 practice questions for the topic: "{topic}".
        Format as a numbered list.
        After the questions, provide the correct answers hidden or at the bottom.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Sorry, I couldn't generate questions."

    async def generate_stress_relief_tips(self, message: str) -> str:
        if not self.model:
            return "Breathe in, breathe out..."

        prompt = f"""
        The user is feeling: "{message}".
        Provide 3 short, actionable stress relief tips or motivational quotes.
        Be empathetic and calm.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "Take a deep breath. You've got this."

# Singleton instance
ai_agent = AIAgent()
