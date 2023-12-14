
from typing import Any, Dict

def handler(input: Dict[str, Any], context: object) -> Dict[str, Any]:
    # Extract data from input
    timestamp = input['timestamp']
    cpu_count = 16

    # host = context.get("host")
    # port = context.get("port")
    # input_key = context.get("input_key")
    # output_key = context.get("output_key")
    # function_getmtime = context.get("function_getmtime")
    # last_execution = context.get("last_execution")
    # env = context.get("env", {})

    # Compute metrics
    percent_network_egress = calculate_percent_network_egress(input)
    percent_memory_caching = calculate_percent_memory_caching(input)
    avg_cpu_utilization = calculate_avg_cpu_utilization(cpu_count, context, input)

    # Prepare output dictionary
    output_metrics = {
        'timestamp': timestamp,
        'percent_network_egress': percent_network_egress,
        'percent_memory_caching': percent_memory_caching,
        'avg_cpu_utilization': avg_cpu_utilization
    }

    # Add CPU-specific metrics
    for i in range(cpu_count):
        cpu_utilization_key = f'avg-util-cpu{i}-60sec'
        output_metrics[cpu_utilization_key] = context.env.get(cpu_utilization_key, 0.0)

    return output_metrics

def calculate_percent_network_egress(input) -> float:
    # Calculate percentage of outgoing traffic bytes
    bytes_sent = input['net_io_counters_eth0-bytes_sent']
    bytes_recv = input['net_io_counters_eth0-bytes_recv']

    total_bytes = bytes_sent + bytes_recv

    if total_bytes == 0:
        return 0.0

    percent_egress = (bytes_sent / total_bytes) * 100
    return round(percent_egress, 2)

def calculate_percent_memory_caching(input) -> float:
    # Calculate percentage of memory caching content
    cached_memory = input['virtual_memory-cached']
    buffer_memory = input['virtual_memory-buffers']
    total_memory = input['virtual_memory-total']

    percent_caching = ((cached_memory + buffer_memory) / total_memory) * 100
    return round(percent_caching, 2)

def calculate_avg_cpu_utilization(cpu_count: int, context, input) -> float:
    last_utilizations = [context.env.get(f'avg-util-cpu{i}', 0.0) for i in range(cpu_count)]

    for i in range(cpu_count):
        last_utilizations[i] = (last_utilizations[i] * 59 + input[f'cpu_percent-{i}']) / 60

    for i in range(cpu_count):
        context.env[f'avg-util-cpu{i}-60sec'] = last_utilizations[i]

    return round(sum(last_utilizations) / cpu_count, 2)



# if __name__ == '__main__':

#     handler('', {'env': {}})

