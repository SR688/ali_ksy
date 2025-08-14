import os, re, glob
import pandas as pd

# ---------- 1. 路径与映射 ----------
price_dir = r"E:\mini_tencent\ksyun\ksyun_price"
spec_dir = r"E:\mini_tencent\ksyun\ksyun_instance"
output_file = r"E:\mini_tencent\ksyun\merged_summary.csv"

#下面是云服务器技术参数的所有列信息，spec_map对他们进行合并，根据需要修改合并
# 端口数 GPU 显存 (HBM2) VCPU（个） 内存 (DDR4) 弹性端口数（个） 内存 (GiB) 端口队列数（个） 型号 PPS（万）
# 内网吞吐量(Gbps) 连接数（万） GPU 显存 (GDDR6) 云盘IOPS GPU (Tesla V100) vCPU (核) 套餐类型名 数据盘(GB,本地SSD)
# 网络转发包能力(万PPS) vCPU（个） GPU 云盘IOPS(万) 中断队列数 内网带宽（Gbps） 多队列 网络带宽能力 (Gbit/s) vCPU(个) PPS(万) GPU
# (GM302) 弹性通告数(个) 终结名称 定时队列数(个) 内存容量(GB) 云盘带宽（Gbps）单中断IP（个） 内存（GB）
# PPS(W) 连接数(万)云盘(Gbps) 数据盘 （本地SSD）

spec_map = {
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
price_map={
    "中国大陆 Linux/Windows": "中国大陆Linux/Windows",
    "中国大陆 Linux/ Windows": "中国大陆Linux/Windows",
    "中国大陆Linux/ Windows": "中国大陆Linux/Windows",
    "中国大陆linux/Windows": "中国大陆Linux/Windows",
    "中国大陆linux/ Windows": "中国大陆Linux/Windows",
    "新加坡 Windows": "新加坡Windows",
    "新加坡 Linux": "新加坡Linux",
    "中国香港 Windows": "中国香港Windows",
    "中国香港 Linux": "中国香港Linux",
    "CPU©": "vCPU(个)",
    "CPU": "vCPU(个)",
    "内存（G）": "内存容量(GB)",
    "内存(G)": "内存容量(GB)",
    "内存": "内存容量(GB)"

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

all_df = []

price_files = {os.path.basename(f).lower(): f for f in glob.glob(os.path.join(price_dir, "*.csv"))}

for spec_file in glob.glob(os.path.join(spec_dir, "*.csv")):
    base_name = os.path.basename(spec_file).lower()

    # ---------- 读取规格表 ----------
    spec_df = pd.read_csv(spec_file).rename(columns=spec_map)

    # ---------- 读取价格表（找不到就造空表） ----------
    price_path = price_files.get(base_name)
    if price_path:
        price_df = pd.read_csv(price_path).rename(columns=price_map)
    else:
        # 关键字段必须存在，否则 merge 会失败
        price_df = pd.DataFrame(columns=["vCPU(个)", "内存容量(GB)"])
    print("spec列：", spec_df.columns.tolist())
    print("price列：", price_df.columns.tolist())
    print(base_name)
    # ---------- 左连接 ----------
    merged = pd.merge(
        spec_df,
        price_df,
        on=["vCPU(个)", "内存容量(GB)"],
        how="left",
        suffixes=("", "_price")
    )

    all_df.append(merged)

if not all_df:
    print("没有任何文件被合并！")
else:
    summary = pd.concat(all_df, ignore_index=True)

    # 自动合并重复列（取非空值）
    final_df = pd.DataFrame()
    for col in summary.columns.unique():
        same_cols = [c for c in summary.columns if c == col]
        if len(same_cols) > 1:
            # 按行取第一个非空值
            merged_col = summary[same_cols].bfill(axis=1).iloc[:, 0]
        else:
            merged_col = summary[col]
        final_df[col] = merged_col

    # 取 '.' 前面的部分再映射
    first_col_name = final_df.columns[0]
    first_col_prefix = final_df[first_col_name].astype(str).str.split('.').str[0]
    final_df["family_id"] = first_col_prefix.map(exact_map)
    # 调整列顺序：把 family_id 插入到第 3 列位置（索引 2）
    cols = list(final_df.columns)
    cols = cols[:2] + ["family_id"] + cols[2:-1]  # -1 避免重复 family_id
    final_df = final_df[cols]

    final_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"已合并 {len(all_df)} 个文件，生成 {output_file}")