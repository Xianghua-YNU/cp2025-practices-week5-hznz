import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

def plot_poisson_pmf(lambda_param=8, max_l=20):
    """绘制泊松分布的概率质量函数"""
    l_values = np.arange(0, max_l)  # 调整为0到max_l-1
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    
    plt.figure(figsize=(10, 6))
    plt.stem(l_values, pmf, linefmt='b-', markerfmt='bo', basefmt=' ')
    plt.title('Poisson Probability Mass Function (λ=8)')  # 标题改为英文
    plt.xlabel('l (正面次数)')
    plt.ylabel('Probability')
    plt.grid(True)
    return pmf  # 返回计算好的PMF数组

def simulate_coin_flips(n_experiments=10000, n_flips=100, p_head=0.08):
    """模拟多组抛硬币实验"""
    if n_experiments == 0 or n_flips == 0:
        return np.array([], dtype=int)
    
    # 直接使用二项分布生成结果
    M = np.random.binomial(n=n_flips, p=p_head, size=n_experiments)
    return M

def compare_simulation_theory(n_experiments=10000, lambda_param=8):
    """比较实验结果与理论分布"""
    M = simulate_coin_flips(n_experiments)
    
    # 计算统计量
    sample_mean = np.mean(M)
    sample_var = np.var(M)
    print(f"样本均值: {sample_mean:.3f} (理论值: 8)")
    print(f"样本方差: {sample_var:.3f} (理论值: 8)")
    
    # 绘制直方图
    plt.figure(figsize=(10, 6))
    bins = np.arange(0, np.max(M)+2) - 0.5
    plt.hist(M, bins=bins, density=False, alpha=0.7, label='实验结果')
    
    # 计算理论分布
    l_values = np.arange(0, np.max(M)+1)
    pmf = (lambda_param**l_values * np.exp(-lambda_param)) / factorial(l_values)
    theory_counts = pmf * n_experiments
    
    plt.plot(l_values, theory_counts, 'r-', label='理论分布')
    plt.title('实验与理论分布对比 (λ=8)')
    plt.legend()
    plt.grid(True)

if __name__ == "__main__":
    np.random.seed(42)
    plot_poisson_pmf()
    compare_simulation_theory()
    plt.show()
