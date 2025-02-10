import random
from datetime import datetime

class Task:
    def __init__(self, task_id, description, deadline):
        self.task_id = task_id
        self.description = description
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.bids = []
        self.winner = None
        # Inherent priority mapping: lower numeric value = higher priority
        priority_mapping = {
            "Search and Rescue": 1,
            "Medical Assistance": 2,
            "Shelter Management": 3,
            "Food Distribution": 4,
            "Logistics": 5
        }
        self.priority = priority_mapping.get(description, 5)
    
    @property
    def formatted_deadline(self):
        return self.deadline.strftime("%Y-%m-%d")

class Agent:
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities
    
    def bid(self, task):
        if task.description in self.capabilities:
            bid_value = random.randint(1, 10)  # Simulate a bid value
            task.bids.append((self, bid_value))
    
    def execute_task(self, task, log):
        # Execution logic can be expanded as needed
        log(f"Agent {self.agent_id} executing Task {task.task_id}: {task.description}")

class CoordinationCenter:
    def __init__(self, agents):
        self.agents = agents
        self.tasks = []
    
    def announce_task(self, task, log):
        self.tasks.append(task)
        log(f"Task {task.task_id}: {task.description} (Due: {task.formatted_deadline}) announced")
        for agent in self.agents:
            agent.bid(task)
        self.evaluate_bids(task, log)
    
    def evaluate_bids(self, task, log):
        if task.bids:
            winning_bid = max(task.bids, key=lambda bid: bid[1])
            task.winner = winning_bid[0]
            bid_value = winning_bid[1]
            log(f"Task {task.task_id}: {task.description} (Due: {task.formatted_deadline} | Priority: {task.priority}) announced and assigned to Agent {task.winner.agent_id} with bid {bid_value}")
            task.winner.execute_task(task, log)
        else:
            log(f"Task {task.task_id}: {task.description} (Due: {task.formatted_deadline} | Priority: {task.priority}) announced but received no bids")
