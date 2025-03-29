import numpy as np
import matplotlib.pyplot as plt

def generate_coin_sequence(n_flips, p_head=0.08):
    """生成硬币序列，1表示正面，0表示反面"""
    return np.random.choice([0, 1], size=n_flips, p=[1 - p_head, p_head])

def calculate_waiting_times(coin_sequence):
    """计算两次正面之间的等待时间（反面次数）"""
    positions = np.nonzero(coin_sequence == 1)[0]
    if len(positions) < 2:
        return np.array([])
    return np.diff(positions) - 1

def plot_waiting_time_histogram(waiting_times, log_scale=False, n_flips=None):
    """绘制等待时间直方图"""
    plt.figure(figsize=(10, 6))
    bins = 'auto' if len(waiting_times) > 100 else max(1, len(waiting_times)//5)
    
    counts, bins, _ = plt.hist(
        waiting_times, 
        bins=bins, 
        density=True, 
        alpha=0.7, 
        color='green' if log_scale else 'blue',
        log=log_scale
    )
    
    title = f'等待时间分布 (n={n_flips})' if n_flips else '等待时间分布'
    if log_scale:
        title = '半对数坐标' + title
    plt.title(title)
    plt.xlabel('两次正面之间的反面次数')
    plt.ylabel('概率密度' + ('（对数刻度）' if log_scale else ''))
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.show()

def analyze_waiting_time(waiting_times, p=0.08):
    """分析等待时间的统计特性"""
    stats = {}
    if len(waiting_times) == 0:  # 修复括号错误
        stats["mean"] = np.nan
        stats["std"] = np.nan
    else:
        stats["mean"] = np.mean(waiting_times)
        stats["std"] = np.std(waiting_times)
    stats["theoretical_mean"] = (1 - p) / p
    stats["exponential_mean"] = 1 / p
    return stats

def run_experiment(n_flips, title):
    """运行一次等待时间实验"""
    print(f"\n{title}")
    print("-"*50)
    
    sequence = generate_coin_sequence(n_flips)
    waiting_times = calculate_waiting_times(sequence)
    
    if len(waiting_times) == 0:
        print("无法计算等待时间：正面出现次数不足")
        return (np.array([]), {}
    
    stats = analyze_waiting_time(waiting_times)
    
    print(f"实验平均等待时间: {stats['mean']:.2f}")
    print(f"理论均值（几何分布）: {stats['theoretical_mean']:.2f}")
    print(f"理论均值（指数分布）: {stats['exponential_mean']:.2f}")
    print(f"样本标准差: {stats['std']:.2f}")
    
    plot_waiting_time_histogram(waiting_times, n_flips=n_flips)
    plot_waiting_time_histogram(waiting_times, log_scale=True, n_flips=n_flips)
    
    return (waiting_times, stats)

if __name__ == "__main__":
    np.random.seed(42)
    
    waiting_times_1k, stats_1k = run_experiment(1000, "任务一：1000次抛掷实验")
    waiting_times_1m, stats_1m = run_experiment(1000000, "\n任务二：1,000,000次抛掷实验")
