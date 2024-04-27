import subprocess
import itertools
import multiprocessing

def run_main_with_inputs(task, model, src, trg):
    command = ["python", "main.py"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.stdin.write(f"{task}\n{model}\n{src}\n{trg}\n")
    process.stdin.flush()
    stdout, stderr = process.communicate()
    return stdout, stderr

def run_in_parallel(inputs):
    print(f"Running main.py with inputs: {inputs}")
    stdout, stderr = run_main_with_inputs(*inputs)  
    if stderr:
        print(f"Error occurred while running with inputs {inputs}:")
        print(stderr)
    else:
        print(f"Output for inputs {inputs}:")
        print(stdout)

if __name__ == '__main__':
    tasks = ["1", "2"]
    models = ["1","2", "3"]
    src = ["1"]
    targets = ["2", "3", "4", "5", "6", "7"]

    input_combinations = list(itertools.product(tasks, models, src, targets)) + list(itertools.product(tasks, models, targets, src))

    with multiprocessing.Pool() as pool:
        pool.map(run_in_parallel, input_combinations)
