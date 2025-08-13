import pandas as pd
import os

# 第一步：读取 vol_price.csv 文件并处理
vol_price_path = '/Users/davilli/Desktop/ali_price.csv'
df1 = pd.read_csv(vol_price_path)

# 使得“实例规格”列的值唯一，如果出现相同的情况，选取"按量计费 (小时)"最小值
idx = df1.groupby('实例规格')['按量目录价'].idxmin()
df1_unique = df1.loc[idx].reset_index(drop=True)

# 第二步：遍历 df1 的“实例规格”，并遍历读取指定目录中的所有 CSV 文件
volc_test_dir = '/Users/chenguanjin/Desktop/ali/aliinstance'
instance_types = df1_unique['实例规格'].tolist()

# 创建一个空的列表来存储结果
results = []

# 遍历 df1 的“实例规格”
for instance_type in instance_types:
    # 遍历指定目录中的所有 CSV 文件
    for file_name in os.listdir(volc_test_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(volc_test_dir, file_name)
            try:
                df_temp = pd.read_csv(file_path, on_bad_lines='skip')
            except pd.errors.ParserError as e:
                print(f"Error parsing {file_path}: {e}")
                continue

            # 匹配到“实例规格”相同的行
            matching_rows = df_temp[df_temp['实例规格'] == instance_type]

            if not matching_rows.empty:
                # 获取列名称中包含“带宽”和“收发包”的所有列的值
                bandwidth_columns = [col for col in matching_rows.columns if '带宽' in col and '网络' in col]
                pps_columns = [col for col in matching_rows.columns if 'PPS' in col]
                disk_iops_col = [col for col in matching_rows.columns if 'IOPS' in col]
                disk_bandwith_col = [col for col in matching_rows.columns if '带宽' in col and '云盘' in col]

                # 获取这些列的值
                network_bandwidth = matching_rows[bandwidth_columns].iloc[0].values[0] if bandwidth_columns else None
                network_pps = matching_rows[pps_columns].iloc[0].values[0] if pps_columns else None
                disk_iops = matching_rows[disk_iops_col].iloc[0].values[0] if disk_iops_col else None
                disk_bandwith = matching_rows[disk_bandwith_col].iloc[0].values[0] if disk_bandwith_col else None

                # label = matching_rows['family_id'].iloc[0]

                # 获取 df1 中的其他所需列的值
                row = df1_unique[df1_unique['实例规格'] == instance_type].iloc[0]
                cpu = row['vCPUs']
                memory = row['内存(GiB)']
                hourly_price = row['按量目录价']
                processor_model = row['处理器']
                region = row['地域']

                family_id = instance_type.split('.')[0]
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



                # 创建一个字典来存储所有值
                # result_row = {
                #     "instance_type": instance_type,
                #     "cpu": cpu,
                #     "memory": memory,
                #     "hourly_price": hourly_price,
                #     "processor_model": processor_model,
                #     "network_bandwidth": network_bandwidth,
                #     "network_pps": network_pps,
                #     "region": region
                # }

                result_row = {
                    # "id", 不写
                    "instance_type": instance_type,
                    "cpu": cpu,
                    "memory": memory,
                    "hourly_price": hourly_price,
                    "instance_label": label,
                    "family_id": instance_type.split('.')[1],
                    "processor_model": processor_model,
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
                    "region": region,
                    "disk_iops": disk_iops,
                    "disk_bandwidth": disk_bandwith,
                    # "created": 不写
                    # "modified": 不写
                }

                # 将结果添加到列表中
                results.append(result_row)

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

# 打印结果
print(df2)
df2.to_csv('/Users/chenguanjin/Desktop/ali/ali_table.csv', index=False)
