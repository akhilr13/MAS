import uuid
from flask import Flask, render_template, request
from simulation import Task, Agent, CoordinationCenter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['GET', 'POST'])
def simulate():
    if request.method == 'POST':
        # Retrieve lists of task descriptions and deadlines from the form
        descriptions = request.form.getlist('description')
        deadlines = request.form.getlist('deadline')
        
        # Temporary log list to capture simulation messages
        temp_logs = []
        def log(message):
            temp_logs.append(message)
        
        # Create agents with predefined capabilities
        agent1 = Agent("A1", ["Search and Rescue", "Medical Assistance"])
        agent2 = Agent("A2", ["Shelter Management", "Food Distribution"])
        agent3 = Agent("A3", ["Search and Rescue", "Logistics"])
        agent4 = Agent("A4", ["Medical Assistance", "Logistics"])
        agent5 = Agent("A5", ["Food Distribution", "Shelter Management"])
        
        # Create the Coordination Center with the agents
        coordination_center = CoordinationCenter([agent1, agent2, agent3, agent4, agent5])
        
        # Announce each task (with auto-generated task IDs)
        for i, description in enumerate(descriptions):
            if not description or not deadlines[i]:
                continue
            task_id = "T" + uuid.uuid4().hex[:4].upper()
            new_task = Task(task_id, description, deadlines[i])
            coordination_center.announce_task(new_task, log)
        
        # Sort tasks by deadline (earlier first) then by inherent priority
        sorted_tasks = sorted(coordination_center.tasks, key=lambda t: (t.deadline, t.priority))
        
        # Convert numeric priority into a friendly label
        def priority_label(priority):
            if priority == 1:
                return "High"
            elif priority in [2, 3]:
                return "Medium"
            else:
                return "Low"
        
        # Generate summary messages for each task (all details on one line)
        task_summaries = []
        for task in sorted_tasks:
            if task.winner:
                bid_value = next(bid for agent, bid in task.bids if agent == task.winner)
                summary = (
                    f"Task {task.task_id}: {task.description} (Due: {task.formatted_deadline} | "
                    f"Priority: {priority_label(task.priority)}) announced and assigned to Agent {task.winner.agent_id} with bid {bid_value}"
                )
                task_summaries.append(summary)
            else:
                summary = (
                    f"Task {task.task_id}: {task.description} (Due: {task.formatted_deadline} | "
                    f"Priority: {priority_label(task.priority)}) announced but received no bids"
                )
                task_summaries.append(summary)
        
        # Group tasks by agent to indicate execution order
        agent_tasks = {}
        for task in coordination_center.tasks:
            if task.winner:
                agent_tasks.setdefault(task.winner.agent_id, []).append(task)
        
        execution_messages = []
        for agent_id, tasks in agent_tasks.items():
            if len(tasks) > 1:
                execution_messages.append(f"Agent {agent_id} is executing tasks sequentially.")
            else:
                execution_messages.append(f"Agent {agent_id} is executing task concurrently.")
        
        # Combine the task summaries and execution messages
        logs = task_summaries + execution_messages
        
        return render_template('simulation.html', logs=logs)
    
    # GET request: show the multi-task announcement form
    return render_template('simulate_form.html')

if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get('PORT', 8000)))
