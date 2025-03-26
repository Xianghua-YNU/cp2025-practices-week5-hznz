import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

def plot_poisson_pmf(lambda_param=8, max_l=20):
    """绘制泊松分布的概率质量函数"""
    l_values = np.arange(0, max_l)  # 生成0到max_l-1的序列
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    
    plt.figure(figsize=(10, 6))
    # 改用plot函数绘制离散点
    plt.plot(l_values, pmf, 'bo', linestyle='-', markersize=6)  
    plt.title('Poisson Probability Mass Function (λ=8)')        # 必须使用英文标题
    plt.xlabel('l (正面次数)')
    plt.ylabel('Probability')
    plt.grid(True)
    return pmf  # 返回PMF供测试验证

def simulate_coin_flips(n_experiments=10000, n_flips=100, p_head=0.08):
    """模拟多组抛硬币实验"""
    if n_experiments == 0 or n_flips == 0:
        return np.array([], dtype=int)
    return np.random.binomial(n=n_flips, p=p_head, size=n_experiments)

def compare_simulation_theory(n_experiments=10000, lambda_param=8):
    """比较实验结果与理论分布"""
    M = simulate_coin_flips(n_experiments)
    
    # 统计信息输出
    print(f"样本均值: {np.mean(M):.3f} (理论值: 8)")
    print(f"样本方差: {np.var(M):.3f} (理论值: 8)")
    
    # 绘制直方图
    plt.figure(figsize=(10, 6))
    bins = np.arange(-0.5, np.max(M)+1.5)
    plt.hist(M, bins=bins, density=False, alpha=0.7, label='实验结果')
    
    # 理论曲线
    l_values = np.arange(0, np.max(M)+1)
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    plt.plot(l_values, pmf * n_experiments, 'r-', label='理论分布')
    plt.legend()
    plt.grid(True)

if __name__ == "__main__":
    np.random.seed(42)
    plot_poisson_pmf()
    compare_simulation_theory()
    plt.show()
