from utils import chat_completion, read_json, save_json
from prompts import get_slm_output_parser
import pandas as pd
from tqdm import tqdm
import json

class slm_parser:
    def __init__(self):
        self.response_dir = '../response/'
        self.file_root_path = "../gen_files/cqad_set_v4"
        self.slm_parsed = "../gen_files/slm_parsed"
        # TODO replace above it with SLM reason output
        csv_dir = self.response_dir + 'final_cs_Meta-Llama-3.1-8B-Instruct_10.csv'
        self.vLLM_resp = pd.read_csv(csv_dir)
        self.chuck_count = len(self.vLLM_resp['chunk_set_id'].unique())
    def slm_output_parser(self, chunk_id):

        json_path = f'{self.file_root_path}/Instruction_{str(chunk_id)}_version4.json'
        json_data = read_json(json_path)


        resp = self.vLLM_resp[self.vLLM_resp['chunk_set_id']==chunk_id]['full_option'].to_list() #

        #=================

        retry = 0
        llm_parser = []
        for i, resp_i in enumerate(resp):
            context = json_data[i]['actual_context']
            sys_pt, usr_pt = get_slm_output_parser(slm_full_option=resp_i,
                                                   context=context)
            retry = 0
            while retry < 5:
                out = chat_completion(system_pt=sys_pt, user_pt=usr_pt)
                try:
                    out = json.loads(out)
                    retry = 100
                except:
                    print(f"retry : {retry}")
                    retry += 1

            llm_parser.append(out)

        save_json(data_dict=llm_parser,
                  file_path=f'{self.slm_parsed}/slm_parsed_chunk_id_{str(chunk_id)}.json')

    def itr_chuck(self):
        for i in tqdm(range(self.chuck_count)):
            self.slm_output_parser(i)


if __name__ == '__main__':
    slm_parser_obj = slm_parser()
    slm_parser_obj.itr_chuck()