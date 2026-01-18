
def determine_intent_keyword(message: str) -> str:
    message = message.lower()
    if any(word in message for word in ["plan", "schedule", "routine", "timetable", "study"]):
        return "study_planning"
    if any(word in message for word in ["time", "waste", "manage", "hours"]):
        return "time_management"
    if any(word in message for word in ["exam", "test", "revise", "revision", "prepare"]):
        return "exam_preparation"
    if any(word in message for word in ["practice", "question", "quiz", "problem"]):
        return "practice_questions"
    if any(word in message for word in ["stress", "anxious", "tired", "worry", "help", "tip"]):
        return "stress_relief"
    return "study_planning" # Default

def generate_practice_questions(subject: str = "biology") -> str:
    # Simulating specific knowledge for the demo
    # In a real app, this would query a vector DB or LLM
    
    if "biology" in subject.lower():
        return (
            "**No problem!** Here are some practice questions for your biology exam:\n\n"
            "1. What is the function of mitochondria in cells?\n"
            "2. Explain the process of photosynthesis."
        )
    else:
         return (
            f"**Sure!** Here are some practice questions for {subject}:\n\n"
            "1. Describe the core concepts of this topic.\n"
            "2. How does this subject relate to real-world applications?"
        )

def generate_stress_relief() -> str:
    return (
        "**Take a deep breath!** Try to study in short, focused sessions, and remember\n"
        "to take breaks. You've got this! 👍"
    )

def generate_study_plan(student_data: dict) -> str:
    # student_data keys: education_level, subjects_count, study_hours, exam_timeline, study_habit
    
    plan = []
    plan.append(f"Here is your personalized study guidance for {student_data.get('education_level', 'your level')}:")
    
    try:
        days_remaining = int(student_data.get('exam_timeline', 30))
        hours = float(student_data.get('study_hours', 2))
        subjects = int(student_data.get('subjects_count', 1))
        habit = student_data.get('study_habit', 'consistent').lower()
    except ValueError:
        return "I had trouble understanding your numbers. However, generally, consistency is key! Try to study a little every day."

    # Decision Logic
    
    # 1. Timeline Strategy
    if days_remaining < 15:
        plan.append("\n**🚨 Critical Exam Mode**")
        plan.append("- **Focus**: 70% Revision / 30% New Topics.")
        plan.append("- **Technique**: Use Active Recall and Past Papers immediately.")
    elif days_remaining < 45:
        plan.append("\n**⚠️ Balanced Prep Mode**")
        plan.append("- **Focus**: Finish syllabus in 2 weeks, then switch to revision.")
        plan.append("- **Technique**: Try the Pomodoro technique (25m work / 5m break).")
    else:
        plan.append("\n**🌱 Long-Term Growth Mode**")
        plan.append("- **Focus**: Deep understanding of concepts.")
        plan.append("- **Technique**: Spaced Repetition to ensure long-term retention.")

    # 2. Daily Schedule (based on hours)
    plan.append(f"\n**📅 Daily Schedule ({hours} hours/day)**")
    session_length = 45 if hours >= 3 else 30
    sessions = int((hours * 60) // session_length)
    
    plan.append(f"- Split your time into {sessions} sessions of {session_length} minutes each.")
    if subjects > 4:
         plan.append("- **Subject Rotation**: Study 2 different subjects per day to keep things fresh.")
    else:
         plan.append("- **Deep Dive**: Focus on 1 major subject per day.")

    # 3. Habit Correction
    if "irregular" in habit or "last-minute" in habit:
        plan.append("\n**💡 Productivity Fix**")
        plan.append("- Since your habit is irregular, start with just 15 minutes today. Do not break the chain!")
        plan.append("- Set a fixed alarm for study time, even if you don't feel like it.")
    
    plan.append("\nGood luck! You've got this. 🚀")
    
    return "\n".join(plan)
