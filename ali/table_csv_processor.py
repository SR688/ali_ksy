import pandas as pd
import os

# 设置目录路径和输出文件路径
directory_path = '/Users/chenguanjin/Desktop/ali/aliinstance'
output_file_path = '/Users/chenguanjin/Desktop/ali/ali_table.csv'

# 检查目录是否存在
if not os.path.exists(directory_path):
    print(f"错误：目录 {directory_path} 不存在")
    exit(1)

# 获取目录中的所有CSV文件
csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

if not csv_files:
    print(f"错误：目录 {directory_path} 中没有CSV文件")
    exit(1)

# 存储所有实例信息的字典，用实例规格作为键以避免重复
all_instances = {}

try:
    # 遍历每个CSV文件
    for csv_file in csv_files:
        file_path = os.path.join(directory_path, csv_file)
        print(f"处理文件: {csv_file}")
        
        # 读取CSV文件
        try:
            df1 = pd.read_csv(file_path)
            df1_unique = df1.drop_duplicates(subset=['实例规格'])
            
            # 获取所有实例规格
            instance_types = df1_unique['实例规格'].tolist()
            
            # 遍历 df1 的"实例规格"

            for instance_type in instance_types:
                # 如果已处理过该实例，则跳过
                if instance_type in all_instances:
                    continue
                    
                # 匹配到"实例规格"相同的行
                matching_rows = df1[df1['实例规格'] == instance_type]
                
                if not matching_rows.empty:
                    # 获取列名称中包含"带宽"和"收发包"的所有列的值
                    bandwidth_columns = [col for col in matching_rows.columns if '带宽' in col and '网络' in col]
                    pps_columns = [col for col in matching_rows.columns if 'PPS' in col]
                    disk_iops_col = [col for col in matching_rows.columns if 'IOPS' in col]
                    disk_bandwith_col = [col for col in matching_rows.columns if '带宽' in col and '云盘' in col]
                    
                    # 获取这些列的值
                    network_bandwidth = matching_rows[bandwidth_columns].iloc[0].to_numpy()[0] if bandwidth_columns else None
                    network_pps = matching_rows[pps_columns].iloc[0].to_numpy()[0] if pps_columns else None
                    disk_iops = matching_rows[disk_iops_col].iloc[0].to_numpy()[0] if disk_iops_col else None
                    disk_bandwith = matching_rows[disk_bandwith_col].iloc[0].to_numpy()[0] if disk_bandwith_col else None
                    
                    # 获取 df1 中的其他所需列的值
                    row = df1_unique[df1_unique['实例规格'] == instance_type].iloc[0]
                    cpu = row['vCPU'] if 'vCPU' in row else None
                    memory = row['内存（GiB）'] if '内存（GiB）' in row else None
                    
                    family_id = instance_type.split('.')[1]
                    label = ''
                    print(family_id)
                    if family_id[0] == 'g':
                        label = '通用型'
                    elif family_id[0] == 'c':
                        label = '计算型'
                    elif family_id[0] == 'r':
                        label = '内存型'
                    elif family_id[0] == 'd':
                        label = '大数据型'
                    elif family_id[0] == 'i':
                        label = '本地SSD型'
                    elif family_id[0] == 'h':
                        label = '高主频型'
                    print(label)
                    
                    result_row = {
                        "instance_type": instance_type,
                        "cpu": cpu,
                        "memory": memory,
                        "hourly_price": None,
                        "instance_label": label,
                        "family_id": family_id,
                        "processor_model": None,
                        "network_bandwidth": network_bandwidth,
                        "network_pps": network_pps,
                        "disk": 0,
                        "platform": "aliyun",
                        "l1_cache": None,
                        "l2_cache": None,
                        "l3_cache": None,
                        "processor_base_frequency": None,
                        "processor_turbo_frequency": None,
                        "numa_count": None,
                        "hyper_threading": None,
                        "region": None,
                        "disk_iops": disk_iops,
                        "disk_bandwidth": disk_bandwith,
                    }
                    
                    # 将结果添加到字典中
                    all_instances[instance_type] = result_row
                    
        except Exception as e:
            print(f"处理文件 {csv_file} 时出错: {e}")
            continue
    
    # 将字典转换为列表
    results = list(all_instances.values())
    
    # 将结果列表转换为 DataFrame
    df2 = pd.DataFrame(results,
                    columns=["instance_type",
                            "cpu",
                            "memory",
                            "hourly_price",
                            "instance_label",
                            "family_id",
                            "processor_model",
                            "network_bandwidth",
                            "network_pps",
                            "disk",
                            "platform",
                            "l1_cache",
                            "l2_cache",
                            "l3_cache",
                            "processor_base_frequency",
                            "processor_turbo_frequency",
                            "numa_count",
                            "hyper_threading",
                            "region",
                            "disk_iops",
                            "disk_bandwidth"])
    
    # 打印结果行数
    print(f"共处理了 {len(df2)} 条实例记录")
    
    # 保存到CSV
    df2.to_csv(output_file_path, index=False)
    print(f"处理完成，结果已保存到 {output_file_path}")

except Exception as e:
    print(f"处理过程中出错: {e}")
    import traceback
    traceback.print_exc()