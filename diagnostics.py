from environment.dashboard import Dashboard

dash = Dashboard()

dash.plot_rewards(
    ["logs/data/Curriculum + Softmax", "logs/data/No curriculum + Softmax", "logs/data/No curriculum + eps-greedy", "logs/data/Curriculum + eps-greedy"])
