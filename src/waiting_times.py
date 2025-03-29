import numpy as np
import matplotlib.pyplot as plt

def generate_coin_sequence(n_flips, p_head=0.08):
    """生成硬币抛掷序列
    参数:
        n_flips (int): 总抛掷次数
        p_head (float): 正面概率，默认0.08
        
    返回:
        ndarray: 由0（反面）和1（正面）组成的序列，长度等于n_flips
    """
    # 使用np.random.choice生成符合概率分布的随机序列
    return np.random.choice([0, 1], size=n_flips, p=[1 - p_head, p_head])

def calculate_waiting_times(coin_sequence):
    """计算两次连续正面之间的反面次数
    参数:
        coin_sequence (ndarray): 硬币抛掷序列
        
    返回:
        ndarray: 各次等待时间组成的数组（空数组表示无法计算）
    """
    # 定位所有正面出现的位置索引
    positions = np.nonzero(coin_sequence == 1)[0]
    # 需要至少两个正面才能计算间隔
    if len(positions) < 2:
        return np.array([])
    # 计算相邻正面间隔并减1得到中间的反面次数
    return np.diff(positions) - 1  

def plot_waiting_time_histogram(waiting_times, log_scale=False, n_flips=None):
    """绘制等待时间分布直方图
    参数:
        waiting_times (ndarray): 等待时间数组
        log_scale (bool): 是否对y轴使用对数刻度
        n_flips (int): 总抛掷次数（用于标题显示）
    """
    plt.figure(figsize=(10, 6))
    # 动态分箱策略：数据量大时自动分箱，小时减少分箱数
    bins = np.arange(0, max_wait + 2) - 0.5  # 确保每个整数值有一个bin
    
    # 绘制概率密度直方图
    counts, bins, _ = plt.hist(
        waiting_times, 
        bins=bins, 
        density=True,       # 归一化为概率密度
        alpha=0.7,         # 设置透明度
        color='green' if log_scale else 'blue',
        log=log_scale      # 控制y轴对数刻度
    )
    
    # 动态生成标题
    title = f'等待时间分布 (n={n_flips})' if n_flips else '等待时间分布'
    if log_scale:
        title = '半对数坐标' + title
    
    # 设置图形元素
    plt.title(title)
    plt.xlabel('Waiting Time (Number of Tails)')
    plt.ylabel('Frequency' if not log_scale else 'Frequency (Log Scale)')
    plt.grid(True, alpha=0.3)  # 显示网格线
    plt.show()

def analyze_waiting_time(waiting_times, p=0.08):
    """分析等待时间的统计特性
    参数:
        waiting_times (ndarray): 等待时间数组
        p (float): 正面概率
        
    返回:
        dict: 包含以下统计量的字典:
            - mean: 样本均值
            - std: 样本标准差
            - theoretical_mean: 几何分布理论均值 (1-p)/p
            - exponential_mean: 指数分布理论均值 1/p
    """
    stats = {}
    if len(waiting_times) == 0:  # 处理空输入
        stats["mean"] = np.nan    # 使用NaN表示无效值
        stats["std"] = np.nan
    else:
        stats["mean"] = np.mean(waiting_times)
        stats["std"] = np.std(waiting_times)
    
    # 计算理论值
    stats["theoretical_mean"] = (1 - p) / p   # 几何分布期望公式
    stats["exponential_mean"] = 1 / p         # 指数分布期望公式
    return stats

def run_experiment(n_flips, title):
    """执行完整实验流程
    参数:
        n_flips (int): 总抛掷次数
        title (str): 实验标题
        
    返回:
        tuple: (等待时间数组, 统计字典)
    """
    print(f"\n{title}")
    print("-"*50)
    
    # 生成硬币序列
    sequence = generate_coin_sequence(n_flips)
    # 计算等待时间
    waiting_times = calculate_waiting_times(sequence)
    
    # 处理无效情况
    if len(waiting_times) == 0:
        print("无法计算等待时间：正面出现次数不足")
        return (np.array([]), {})
    
    # 进行统计分析
    stats = analyze_waiting_time(waiting_times)
    
    # 输出统计结果
    print(f"实验平均等待时间: {stats['mean']:.2f}")
    print(f"理论均值（几何分布）: {stats['theoretical_mean']:.2f}")
    print(f"理论均值（指数分布）: {stats['exponential_mean']:.2f}")
    print(f"样本标准差: {stats['std']:.2f}")
    
    # 绘制双版本直方图
    plot_waiting_time_histogram(waiting_times, n_flips=n_flips)        # 普通坐标
    plot_waiting_time_histogram(waiting_times, log_scale=True, n_flips=n_flips)  # 对数坐标
    
    return (waiting_times, stats)

if __name__ == "__main__":
    np.random.seed(42)  # 设置随机种子保证结果可复现
    
    # 执行两个不同规模的实验
    waiting_times_1k, stats_1k = run_experiment(1000, "任务一：1000次抛掷实验")
    waiting_times_1m, stats_1m = run_experiment(1000000, "\n任务二：1,000,000次抛掷实验")
