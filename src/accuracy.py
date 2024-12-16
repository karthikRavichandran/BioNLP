import pandas as pd
final_out_path = "../gen_files/response/cleaned_final_10.csv"
df = pd.read_csv(final_out_path).dropna()
df = df[['chunk_set_id', 'wo_context', 'w_context']]
df["chunk_set_id"] = df["chunk_set_id"].astype(int)
# print(df.colums)
k = []
for i in range(10):
    wo_acc = df[df['chunk_set_id'] == i]["wo_context"].mean()
    w_acc = df[df['chunk_set_id'] == i]["w_context"].mean()
    total_chunks = df[df['chunk_set_id'] == i]["wo_context"].shape[0]
    k.append({"chunk_set_id": i,
              "wo_context_acc": wo_acc,
              "w_context": w_acc,
              "chunks in the set": total_chunks})
final_df = pd.DataFrame(k)
final_df.to_csv("../gen_files/response/acc_set_wise.csv")
print(final_df)


