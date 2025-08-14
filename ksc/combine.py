import os
import pandas as pd

# 列名映射表
col_map = {
    # vCPU
    "VCPU（个）": "vCPU(个)",
    "vCPU (核)": "vCPU(个)",
    "vCPU（个）": "vCPU(个)",
    "vCPU(个)": "vCPU(个)",

    # 内存容量
    "内存 (DDR4)": "内存容量(GB)",
    #这个单位不一样
    "内存 (GiB)": "内存容量(GB)",
    "内存容量(GB)": "内存容量(GB)",
    "内存容量（GB）": "内存容量(GB)",

    # GPU显存
    "GPU显存 (HBM2)": "GPU显存",
    "GPU显存 (GDDR6)": "GPU显存",

    # GPU型号/数量
    "GPU (Tesla V100)": "GPU",
    "GPU (GM302)": "GPU",
    "GPU": "GPU",

    # 弹性网卡数
    "弹性网卡数（个）": "弹性网卡数",
    "弹性网卡数(个)": "弹性网卡数",

    # 单网卡私有IP数
    "单网卡私有IP(个)": "单网卡私有IP数",
    "单网卡私有IP（个）": "单网卡私有IP数",

    # 网卡队列数
    "网卡队列数（个）": "网卡队列数",
    "网卡队列数": "网卡队列数",
    "网卡队列数(个)": "网卡队列数",

    # PPS
    "PPS（万）": "PPS(万)",
    "PPS(万)": "PPS(万)",
    "PPS(W)": "PPS(万)",

    # 内网带宽/吞吐量
    "内网吞吐量(Gbps)": "内网带宽(Gbps)",
    "内网吞吐量（Gbps）": "内网带宽(Gbps)",
    "网络带宽能力 (Gbit/s)": "内网带宽(Gbps)",

    # 网络收发包能力（归到PPS）
    "网络收发包能力 (万PPS)": "PPS(万)",

    # 云盘带宽
    "云盘带宽（Gbps）": "云盘带宽(Gbps)",
    "云盘(Gbps)": "云盘带宽(Gbps)",

    # 云盘IOPS
    "云盘IOPS": "云盘IOPS",
    "云盘IOPS(万)": "云盘IOPS",

    # 连接数
    "连接数（万）": "连接数(万)",
    "连接数(万)": "连接数(万)",

    # 数据盘容量
    "数据盘容量(GB,本地SSD)": "数据盘容量(GB,本地SSD)",
    "数据盘 (本地SSD)": "数据盘容量(GB,本地SSD)",

    "套餐类型名":"套餐类型名",
    "套餐名称":"套餐类型名",
    "型号":"套餐类型名"
}
exact_map = {

    "SE9": "高效型",

    "X9a": "性能保障型",
    "X8": "性能保障型",
    "X7": "性能保障型",
    "X6S": "性能增强型",
    "X6": "性能保障型",

    "N3": "通用型",
    "S6": "标准型",
    "S4E": "标准型",
    "S4": "标准型",
    "S3": "标准型",

    "I6": "I0优化型",
    "I4": "I0优化型",
    "I3": "I0优化型",

    "C9a": "计算优化型",
    "C7": "计算优化型",
    "C5": "计算优化型",
    "C4": "计算优化型",

    "HKEC": "星河型",

    "AC4": "ARM计算型",
    "AC5": "ARM计算型",

    "P4V": "GPU通用计算型",
    "P6V": "GPU高效计算型",
    "GN6I": "GPU推理型",
    "GN7I": "GPU通用计算型",
    "GN8I": "GPU通用计算型",
}
#  输入输出路径
input_dir = r"E:\mini_tencent\ksyun\ksyun_instance"  # CSV文件夹
output_file = r"E:\mini_tencent\ksyun\merged_summary.csv"

# 获取CSV文件列表
csv_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(".csv")]
if not csv_files:
    print("目录中没有找到 CSV 文件")
    exit()

# 读取并合并所有CSV
dfs = []
for file in csv_files:
    df = pd.read_csv(file)

    # 统一列名
    df = df.rename(columns=col_map)
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)

# 自动合并重复列（取非空值）
final_df = pd.DataFrame()
for col in merged_df.columns.unique():
    same_cols = [c for c in merged_df.columns if c == col]
    if len(same_cols) > 1:
        # 按行取第一个非空值
        merged_col = merged_df[same_cols].bfill(axis=1).iloc[:, 0]
    else:
        merged_col = merged_df[col]
    final_df[col] = merged_col
first_col_name = final_df.columns[0]  # 第一列列名

# 取 '.' 前面的部分再映射
first_col_prefix = final_df[first_col_name].astype(str).str.split('.').str[0]
final_df["family_id"] = first_col_prefix.map(exact_map)

# 调整列顺序：把 family_id 插入到第 3 列位置（索引 2）
cols = list(final_df.columns)
cols = cols[:2] + ["family_id"] + cols[2:-1]  # -1 避免重复 family_id
final_df = final_df[cols]
# 保存结果
final_df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"已合并 {len(csv_files)} 个文件，生成 {output_file}")
