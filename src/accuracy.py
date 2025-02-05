import pandas as pd
from utils import plot_acc
models = ['final_cs_Meta-Llama-3.1-8B-Instruct_10',
          'final_cs_Mistral-7B-Instruct-v0.2_10',
          'final_cs_Phi-3-mini-128k-instruct_10',
          'final_cs_Qwen2-7B-Instruct_10']
for m in models:
    final_out_path = f"../response/{m}_matched.csv"
    df = pd.read_csv(final_out_path).dropna()
    df = df[['chunk_set_id', 'match_w', 'match_wo']]
    df["chunk_set_id"] = df["chunk_set_id"].astype(int)
    # print(df.colums)
    k = []
    for i in range(10):
        wo_acc = df[df['chunk_set_id'] == i]["match_wo"].mean()
        w_acc = df[df['chunk_set_id'] == i]["match_w"].mean()
        total_chunks = df[df['chunk_set_id'] == i]["match_wo"].shape[0]
        k.append({"chunk_set_id": i,
                  "wo_context_acc": wo_acc,
                  "w_context": w_acc,
                  "chunks in the set": total_chunks})
    final_df = pd.DataFrame(k)
    # plot_acc(final_df,m.split("final_cs_")[1] )
    final_df.to_csv("../response/acc_set_wise.csv")
    wo = final_df["wo_context_acc"].describe().filter(['mean', 'std', 'min', 'max'])
    w = final_df["w_context"].describe().filter(['mean', 'std', 'min', 'max'])
    print(f"{m.split('final_cs_')[1]}")
    print(pd.concat([wo, w], axis=1))
    # print(final_df)



