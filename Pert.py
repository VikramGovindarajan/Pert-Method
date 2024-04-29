
import math
import pandas as pd
from graphviz import Digraph


def pert(tasks, dependencies):
    task_data={}
    #Calculate the expected time, variance and standard deviation of each task
    for task, times in tasks.items():
        O, P, M = times
        expected_time = (O + M*4 + P)/6
        variance = ((P-O)**2)/36
        standard_deviation = math.sqrt(variance)
        # Convert to float and round to two
        float(expected_time)
        float(variance)
        float(standard_deviation)
        expected_time = round(expected_time, 2)
        variance = round(variance, 2)
        standard_deviation = round(standard_deviation, 2)
        # Add the task data to the currently empty dictionary
        task_data[task] = {
            "expected_time": float(expected_time),
            "variance": float(variance),
            "standard_deviation": float(standard_deviation),
            "earliest_start": 0,
            "latest_start": None,
            "earliest_finish": float(expected_time),
            "latest_finish": None,
            "slack": 0
        }


    dependencies = {key: [dep] if isinstance(dep, str) else dep for key, dep in dependencies.items()}
    #Calculate the earliest start and earliest finish of each task
    for _ in range(len(task_data)):
        for task in task_data:
            if task in dependencies:
                earliest_start = max([task_data[dep]["earliest_finish"] for dep in dependencies[task]], default=0)
                task_data[task]["earliest_start"] = earliest_start
                task_data[task]["earliest_finish"] = earliest_start + task_data[task]["expected_time"]

    project_duration = max(task_data[task]["earliest_finish"] for task in task_data)


    for task in task_data:
        task_data[task]["latest_finish"] = project_duration

    # Calculate the latest start, finish and slack of each task
    for _ in range(len(task_data)):
        for task in task_data:
            if task not in dependencies or not dependencies[task]:
                continue
            for dep in dependencies[task]:
                task_data[dep]["latest_finish"] = min(task_data[dep]["latest_finish"], task_data[task]["earliest_start"])
                task_data[dep]["latest_start"] = task_data[dep]["latest_finish"] - task_data[dep]["expected_time"]
                task_data[dep]["slack"] = task_data[dep]["latest_start"] - task_data[dep]["earliest_start"]
                task_data[dep]["slack"] = round(task_data[dep]["slack"], 2)


    return task_data

def create_pert_graph(task_data):
    dot = Digraph()

    for task, data in task_data.items():
        dot.node(task, label=f"{task}\nExpected time: {data['expected_time']} (SD: {data['standard_deviation']})")

    for task, deps in dependencies.items():
        for dep in deps:
            label = str(task_data[dep]['expected_time'])
            dot.edge(dep, task, label=label)

    return dot


#Define the tasks
tasks = {
    "1":  (0, 0, 0),
    "2":  (3, 3, 3),
    "3":  (2, 2, 2),
    "4":  (2, 2, 2),
    "5":  (3, 3, 3),
    "6":  (2, 2, 2),
    "7":  (2, 2, 2),
    "8":  (3, 3, 3),
    "9":  (1, 1, 1),
    "10": (2, 2, 2),
    "11": (6, 6, 6),
    "12": (6, 6, 6),
    "13": (6, 6, 6),
    "14": (5, 5, 5),
    "15": (6, 6, 6),
    "16": (2, 2, 2),
    "17": (2, 2, 2),
    "18": (2, 2, 2),
    "19": (2, 2, 2),
    "20": (0, 0, 0),
}

# Define the dependencies
dependencies = {
    "1": [],
    "2": ["1"],
    "3": ["1"],
    "4": [],
    "5": ["3","4"],
    "6": [],
    "7": ["6"],
    "8": ["7"],
    "9": [],
    "10": ["9"],
    "11": ["2","4","10","8","5"],
    "12": [],
    "13": ["12"],
    "14": [],
    "15": [],
    "16": [],
    "17": [],
    "18": [],
    "19": [],
    "20": ["13", "14","15","16","17"],
}


results = pert(tasks, dependencies)

pert_graph = create_pert_graph(results)
pert_graph.render("pert_graph.png")

#Print the results
results_df = pd.DataFrame.from_dict(results, orient='index')
print(results_df)
#save to csv file
results_df.to_csv('results.csv')

