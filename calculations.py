import numpy as np
from config import params
import os

def explicit(folder_path, text_box):
    num_middle = int((params.num_node + 1) / 2)      #middle node 
    t_nodes = np.full(params.num_node + 2, params.t_i, dtype=float)    # initialization of node temperatures
    t_nodes[0] = params.t_press
    t_nodes[-1] = params.t_press

    results = [t_nodes]

    iteration = 0
    while t_nodes[num_middle] < params.t_weld:

        t_new_nodes = np.copy(t_nodes)
        for i in range(1, int(params.num_node) + 1):
            if i == 1:
                t_new_nodes[i] = ((params.ae * t_nodes[i + 1] + params.aw2 * params.t_press) + (params.w - params.ae - params.aw2) * t_nodes[i]) / params.w
            elif i == params.num_node:
                t_new_nodes[i] = ((params.ae6 * params.t_press + params.aw * t_nodes[i - 1]) + (params.w - params.ae6 - params.aw) * t_nodes[i]) / params.w
            else:
                t_new_nodes[i] = ((params.ae * t_nodes[i + 1] + params.aw * t_nodes[i - 1]) + (params.w - params.ae - params.aw) * t_nodes[i]) / params.w

        t_nodes = t_new_nodes
        results.append(t_nodes.copy())
        iteration += 1

    results = np.array(results)

    iterations = np.arange(results.shape[0]).reshape(-1,1)
    results_with_iter = np.hstack((iterations, results))

    welding_time = iteration * params.delta_tau

    file_name = str(params.file_name+".txt")

    header_text = (
        f"The welding time is {welding_time} seconds\n"
        f"Node number: {params.num_node}\n"
        f"Iteration number: {iteration}\n"
        "Calculation method: Explicit\n"
        "ITERATION\t\tNODE TEMPERATURE")
    
    np.savetxt(
        os.path.join(folder_path, file_name),
        results_with_iter,
        delimiter=",",
        fmt=["%d"] + ["%.2f"] * results.shape[1],
        header=header_text,
        comments="")

    text_box.insert("end", f"\nSimulation completed. Results saved to file "+str(file_name))
    text_box.insert("end", f"\nWelding time is "+str(welding_time)+" seconds")
    text_box.insert("end", f"\nIteration number is "+str(iteration))


def implicit(folder_path, text_box):
    num_srod = int((params.num_node + 1) / 2)      #wmiddle node
    t_nodes = np.full(params.num_node + 2, params.t_i, dtype=float)
    t_nodes[0] = params.t_press
    t_nodes[-1] = params.t_press

    results = [t_nodes]
    epsilon_results = []

    iteration = 0
    iteration_in_timestep = 1
    while t_nodes[num_srod] < params.t_weld:

        t_begin = np.copy(t_nodes)   # new temperatures for nodes

        t_guessed = np.copy(t_begin)    # initial temperatures for a given timestep

        epsilon_list = np.full(params.num_node + 2, params.epsilon)

        epsilon_iteration = np.ones(params.num_node + 2)

        while np.any(epsilon_iteration > epsilon_list):
            t_new_iteration = np.copy(t_guessed)
            for i in range(1, int(params.num_node) + 1):
                if i == 1:
                    t_new_iteration[i] = (
                    params.ae * t_guessed[i + 1]
                    + params.aw2 * params.t_press
                    + params.w * t_begin[i]
                ) / (params.w + params.ae + params.aw2)
                elif i == int(params.num_node):
                    t_new_iteration[i] = (
                    params.ae6 * params.t_press
                    + params.aw * t_guessed[i - 1]
                    + params.w * t_begin[i]
                ) / (params.w + params.ae6 + params.aw)
                else:
                    t_new_iteration[i] = (
                    params.ae * t_guessed[i + 1]
                    + params.aw * t_guessed[i - 1]
                    + params.w * t_begin[i]
                ) / (params.w + params.ae + params.aw)

            epsilon_iteration = np.abs(t_guessed - t_new_iteration)
            epsilon_max = np.max(epsilon_iteration)

            epsilon_results.append(epsilon_max)

            t_guessed = np.copy(t_new_iteration)
            iteration_in_timestep += 1

        results.append(t_new_iteration.copy())

        t_nodes = np.copy(t_new_iteration)
        iteration += 1

    results = np.array(results)

    epsilon_results = np.array(epsilon_results)
    epsilon_results = epsilon_results.reshape(-1, 1)

    iterations = np.arange(results.shape[0]).reshape(-1,1)
    results_with_iter = np.hstack((iterations, results))
    epsilon_iterations = np.arange(epsilon_results.shape[0]).reshape(-1,1) + 1
    epsilon_results_with_iter = np.hstack((epsilon_iterations, epsilon_results))

    welding_time = iteration * params.delta_tau

    file_name = str(params.file_name+".txt")
    file_name_epsilon = str(params.file_name+"_epsilon.txt")

    header_text = (
        f"The welding time is {welding_time} seconds\n"
        f"Node number: {params.num_node}\n"
        f"Iteration number: {iteration}; Iteration number with timesteps: {iteration_in_timestep - 1}\n"
        "Calculation method: Implicit\n"
        "ITERATION\t\tNODE TEMPERATURE")
    
    header_text_epsilon = (
        f"The welding time is {welding_time} seconds\n"
        f"Node number: {params.num_node}\n"
        f"Iteration number with timesteps: {iteration_in_timestep - 1}\n"
        "Calculation method: Implicit\n"
        "ITERATION IN TIMESTEP\t\tEPSILON VALUE")

    np.savetxt(
        os.path.join(folder_path, file_name),
        results_with_iter,
        delimiter=",",
        fmt=["%d"] + ["%.2f"] * results.shape[1],
        header=header_text,
        comments="")
    
    np.savetxt(
        os.path.join(folder_path, file_name_epsilon),
        epsilon_results_with_iter,
        delimiter=",",
        fmt=["%d"] + ["%.6f"] * epsilon_results.shape[1],
        header=header_text_epsilon,
        comments="")
    
    text_box.insert("end", f"\nSimulation completed. Results saved to file "+str(file_name))
    text_box.insert("end", f"\nWelding time is "+str(welding_time)+" seconds")
    text_box.insert("end", f"\nIteration number is "+str(iteration))
    text_box.insert("end", f"\nIteration number in timestep is "+str(iteration_in_timestep - 1))