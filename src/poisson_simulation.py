import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

def plot_poisson_pmf(lambda_param=8, max_l=20):
    """绘制泊松分布的概率质量函数"""
    l_values = np.arange(0, max_l + 1)  # l从0到20
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    
    plt.figure(figsize=(10, 6))
    plt.stem(l_values, pmf, linefmt='b-', markerfmt='bo', basefmt=' ')
    plt.title('泊松分布概率质量函数 (λ=8)')
    plt.xlabel('l (正面次数)')
    plt.ylabel('概率')
    plt.grid(True)

def simulate_coin_flips(n_experiments=10000, n_flips=100, p_head=0.08):
    """模拟多组抛硬币实验"""
    # 生成n_experiments组实验，每组n_flips次抛掷，每次成功概率p_head
    experiments = np.random.binomial(n=1, p=p_head, size=(n_experiments, n_flips))
    # 统计每组正面的总次数
    M = np.sum(experiments, axis=1)
    return M

def compare_simulation_theory(n_experiments=10000, lambda_param=8):
    """比较实验结果与理论分布"""
    # 模拟实验
    M = simulate_coin_flips(n_experiments)
    
    # 计算样本均值和方差
    sample_mean = np.mean(M)
    sample_var = np.var(M)
    print(f"样本均值: {sample_mean:.3f} (理论值: 8)")
    print(f"样本方差: {sample_var:.3f} (理论值: 8)")
    
    # 绘制直方图
    plt.figure(figsize=(10, 6))
    max_count = np.max(M)
    bins = np.arange(0, max_count + 2) - 0.5  # 对齐到整数中心
    plt.hist(M, bins=bins, density=False, alpha=0.7, label='实验结果')
    
    # 计算理论分布
    l_values = np.arange(0, max_count + 1)
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    theory_counts = pmf * n_experiments  # 转换为频数
    
    # 绘制理论曲线
    plt.plot(l_values, theory_counts, 'r-', linewidth=2, label='理论分布')
    
    plt.title('实验结果与理论分布对比 (N=10000)')
    plt.xlabel('正面次数')
    plt.ylabel('频数')
    plt.legend()
    plt.grid(True)

if __name__ == "__main__":
    np.random.seed(42)  # 固定随机种子确保结果可重复
    
    plot_poisson_pmf()
    compare_simulation_theory()
    
    plt.show()
