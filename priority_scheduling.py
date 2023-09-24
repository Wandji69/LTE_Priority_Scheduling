import random
import matplotlib.pyplot as plt

class User:
    def __init__(self, id, priority, demand, max_time):
        self.id = id
        self.priority = priority
        self.demand = demand
        self.max_time = max_time
        self.time_on_network = 0
        self.preempted = False

class LTE_Scheduler:
    def __init__(self, total_resources, users):
        self.total_resources = total_resources
        self.users = users
        self.resources_allocated = {user.id: 0 for user in users}

    def preempt_if_needed(self, user, demand):
        if self.resources_allocated[user.id] + demand > self.total_resources:
            preemption_candidates = [u for u in self.users if u.priority == user.priority and u.id != user.id]
            if preemption_candidates:
                preempted_user = random.choice(preemption_candidates)
                self.resources_allocated[preempted_user.id] = 0
                preempted_user.preempted = True

    def allocate_resources(self):
        for user in self.users:
            if user.preempted:
                user.time_on_network = 0
                user.preempted = False
            demand = user.demand
            self.preempt_if_needed(user, demand)
            if self.resources_allocated[user.id] + demand <= self.total_resources:
                self.resources_allocated[user.id] += demand
                user.time_on_network += 1

    def calculate_throughput(self):
        total_throughput = sum(self.resources_allocated.values())
        return total_throughput

    def calculate_fairness(self):
        calculate_fairness_values = [allocated / user.demand for user, allocated in self.resources_allocated.items()]
        fairness = sum(calculate_fairness_values) / len(calculate_fairness_values)
        return fairness

def simulate():
    num_users = 10
    users = [User(id=i, priority=random.randint(1, 5), demand=random.randint(1, 5), max_time=random.randint(1, 5)) for i in range(num_users)]
    
    scheduler = LTE_Scheduler(total_resources=20, users=users)
    
    num_iterations = 100
    throughput_values = []
    fairness_values = []
    
    for _ in range(num_iterations):
        scheduler.allocate_resources(users)
        system_throughput = scheduler.calculate_throughput()
        fairness = scheduler.calculate_fairness()
        throughput_values.append(system_throughput)
        fairness_values.append(fairness)
    
    # Plot System Throughput
    plt.plot(throughput_values)
    plt.title("System Throughput Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("System Throughput")
    plt.show()
    
    # Plot Fairness
    plt.plot(fairness_values)
    plt.title("Fairness Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Fairness")
    plt.show()

if __name__== "__main__":
  simulate()