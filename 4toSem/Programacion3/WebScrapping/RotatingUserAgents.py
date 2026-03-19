import random

def get_random_user_agent():
    fp = "user_agents.txt"
    with open(fp,'r',encoding='utf-8') as f:
        user_agent = [line.strip() for line in f if line.strip()]
        return random.choice(user_agent) if user_agent else ''