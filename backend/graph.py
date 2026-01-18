from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List
from .ai_agent import ai_agent
from .db import save_study_plan

class AgentState(TypedDict):
    messages: List[str]
    intent: Optional[str]
    student_data: dict
    next_question: Optional[str]
    plan_generated: bool

# --- NODES ---

def start_node(state: AgentState):
    # Just an entry point/pass-through
    if not state.get("student_data"):
        state["student_data"] = {}
    return state

async def intent_router_node(state: AgentState):
    # Short-circuit: if we are mid-conversation for data collection, stick to it.
    if state.get("next_question"):
        state["intent"] = "study_planning"
        return state

    last_message = state["messages"][-1]
    
    # AI-based intent classification
    intent = await ai_agent.detect_intent(last_message)
    state["intent"] = intent
    return state

def data_collection_node(state: AgentState):
    student_data = state["student_data"]
    last_message = state["messages"][-1]
    
    # Existing basic state machine for data collection
    # (We can enhance this with AI extraction later if needed)
    last_question = state.get("next_question")
    
    if last_question:
        # Map the previous question to a data field
        # Simple heuristic mapping
        lower_q = last_question.lower()
        if "level" in lower_q:
            student_data["education_level"] = last_message
        elif "subjects" in lower_q:
            student_data["subjects_count"] = last_message
        elif "hours" in lower_q:
            student_data["study_hours"] = last_message
        elif "exam" in lower_q and "days" not in lower_q: 
            # Ambiguous case, but usually follows order
            pass 
        elif "days" in lower_q or "when" in lower_q or "timeline" in lower_q:
             student_data["exam_timeline"] = last_message
        elif "habit" in lower_q:
             student_data["study_habit"] = last_message

    # Determine what is missing
    required_fields = [
        ("education_level", "What is your current education level? (e.g., High School, College)"),
        ("subjects_count", "How many subjects are you focusing on?"),
        ("study_hours", "How many hours can you dedicate to studying daily?"),
        ("exam_timeline", "When are your exams starting? (e.g., in 2 weeks, 10 days)"),
        ("study_habit", "How would you describe your study habits? (e.g., Consistent, Last-minute, Procrastinator)")
    ]
    
    next_q = None
    for field, question in required_fields:
        if field not in student_data:
            next_q = question
            break
            
    state["next_question"] = next_q
    state["student_data"] = student_data
    return state

async def study_plan_generator_node(state: AgentState):
    plan = await ai_agent.generate_study_plan(state["student_data"])
    save_study_plan(state["student_data"], plan)
    state["plan_generated"] = True
    state["messages"].append(plan) 
    return state

async def practice_node(state: AgentState):
    last_message = state["messages"][-1]
    # Use the message as the topic
    response = await ai_agent.generate_practice_questions(last_message)
    state["messages"].append(response)
    return state

async def stress_node(state: AgentState):
    last_message = state["messages"][-1]
    response = await ai_agent.generate_stress_relief_tips(last_message)
    state["messages"].append(response)
    return state

async def general_chat_node(state: AgentState):
    last_message = state["messages"][-1]
    response = await ai_agent.generate_response(last_message, context="User is interacting with the study bot.")
    state["messages"].append(response)
    return state

# --- EDGES ---

def check_data_completeness(state: AgentState):
    if state.get("next_question"):
        return "ask_question"
    return "generate_plan"

def route_after_intent(state: AgentState):
    intent = state.get("intent")
    if intent == "practice_questions":
        return "practice_questions"
    elif intent == "stress_relief":
        return "stress_relief"
    elif intent == "study_planning":
        return "collect_data"
    else:
        return "general_chat"

# --- GRAPH ---

workflow = StateGraph(AgentState)

workflow.add_node("start", start_node)
workflow.add_node("classify_intent", intent_router_node)
workflow.add_node("collect_data", data_collection_node)
workflow.add_node("generate_plan", study_plan_generator_node)
workflow.add_node("practice_questions", practice_node)
workflow.add_node("stress_relief", stress_node)
workflow.add_node("general_chat", general_chat_node) # New node

workflow.set_entry_point("start")

workflow.add_edge("start", "classify_intent")

workflow.add_conditional_edges(
    "classify_intent",
    route_after_intent,
    {
        "collect_data": "collect_data",
        "practice_questions": "practice_questions",
        "stress_relief": "stress_relief",
        "general_chat": "general_chat"
    }
)

workflow.add_conditional_edges(
    "collect_data",
    check_data_completeness,
    {
        "ask_question": END, 
        "generate_plan": "generate_plan"
    }
)

workflow.add_edge("generate_plan", END)
workflow.add_edge("practice_questions", END)
workflow.add_edge("stress_relief", END)
workflow.add_edge("general_chat", END)

app_graph = workflow.compile()

async def run_chat_workflow(message: str, thread_id: str):
    # In-memory state storage (demo only)
    if not hasattr(run_chat_workflow, "state_store"):
        run_chat_workflow.state_store = {}
    
    current_state = run_chat_workflow.state_store.get(thread_id, {
        "messages": [],
        "intent": None,
        "student_data": {},
        "next_question": None,
        "plan_generated": False
    })
    
    current_state["messages"].append(message)
    
    # We always start from 'start' in this stateless REST wrapper usage, 
    # effectively reloading the 'persisted' state into the graph run.
    # Note: real LangGraph with Checkpointer handles this better.
    
    # If we are in the middle of data collection
    # (next_question was set in previous turn), we might want to ensure we go back to collect_data?
    # Actually, the 'classify_intent' node will run again.
    # If the user answers "High School", 'detect_intent' might say "general_chat" or "study_planning".
    # If it says "general_chat", we break the flow.
    # FIX: We should check if we are in data collection mode and skip intent detection?
    
    # Simple fix for demo: If next_question is set, force intent to study_planning
    if current_state.get("next_question"):
        current_state["intent"] = "study_planning" # Force it back to collection flow
        # But we can't easily jump to a node in this simple setup without using the graph's memory features fully.
        # However, our 'classify_intent' uses the *last message* to detect intent.
        # If I answer "3 hours", AI might thinks it's 'general'.
        
        # Override intent detection logic: if we have pending questions, assume we are answering them.
        pass # We'll handle this by letting the graph run, but maybe we should inject context or bypass?
        
    # To properly support the flow "User answers question -> Graph processes answer", 
    # we can modify 'intent_router_node' to check state logic too, handled below in 'input_config' or just rely on state.

    # Let's trust the graph edges. 
    # But wait! If we start at 'start' -> 'classify_intent', the AI sees "3 hours". 
    # It might classify as 'general_chat' -> 'general_chat_node'. The flow breaks.
    
    # WORKAROUND: In run_chat_workflow, if we expect an answer, we can pre-set the intent?
    # Or better: Update 'intent_router_node' to respect existing unfinished business? -> Modified intent_router_node above?
    # No, I can't access 'state' easily outside the node function inside the node definition.
    # But I can modify the state PASSED IN.
    
    if current_state.get("next_question"):
        # We are expecting an answer.
        # We can bypass classification?
        # LangGraph entry point is 'start'.
        # We can add a conditional edge from 'start' to 'collect_data' if student_data incomplete?
        # That would be a better graph design.
        pass 

    # For now, let's keep it simple. If we are collecting data, we loop back to collect_data logic.
    # But the GRAPH defines the flow.
    # If I add logic to 'intent_router_node' to check `state.get("next_question")`?
    # YES. I will update intent_router_node in the replacement content to handle this.
    
    input_config = {"recursion_limit": 10}
    result = await app_graph.ainvoke(current_state, input_config)
    
    run_chat_workflow.state_store[thread_id] = result
    
    if result.get("plan_generated"):
         return result["messages"][-1]
    elif result.get("next_question"):
         return result["next_question"]
    else:
         return result["messages"][-1]
