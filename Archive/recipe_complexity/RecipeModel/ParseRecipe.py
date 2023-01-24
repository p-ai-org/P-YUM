# %%
import argparse
import json
import sys
import subprocess
import tempfile
import importlib
import CleanData
importlib.reload(CleanData)


# def _exec_crf_test(input_text, model_path):
#     print(CleanData.export_data(input_text))


# def _convert_crf_output_to_json(crf_output):
#     return json.dumps(CleanData.import_data(crf_output), indent=2, sort_keys=True)


# def analyze_recipe(path_in):
#     recipe_file = open(path_in, "r")
#     #read whole file to a string
#     ingredient_text = recipe_file.read().split('\n')
#     recipe_file.close()
#     print(ingredient_text)
    
#     model = "RecipeParse.crfmodel"
#     crf_output = _exec_crf_test(ingredient_text, model)
#     print(_convert_crf_output_to_json(crf_output.split('\n')))
# %%

def _exec_crf_test(input_text, model_path):
    with tempfile.NamedTemporaryFile(mode='w') as input_file:
        input_file.write(CleanData.export_data(input_text))
        print(CleanData.export_data(input_text))
        input_file.flush()
        print(input_file.name)
        return subprocess.check_output(
            ['CRF++-0.58\\crf_test', '--verbose=1', '--model', model_path,
             input_file.name]).decode('utf-8')


def _convert_crf_output_to_json(crf_output):
    return json.dumps(CleanData.import_data(crf_output), indent=2, sort_keys=True)


def main(args):
    raw_ingredient_lines = [x for x in sys.stdin.readlines() if x]
    crf_output = _exec_crf_test(raw_ingredient_lines, args.model_file)
    print(_convert_crf_output_to_json(crf_output.split('\n')))


def analyze_recipe(path_in):
    recipe_file = open(path_in, "r")
    #read whole file to a string
    ingredient_text = [x for x in recipe_file.readlines() if x]
    recipe_file.close()
    crf_output = _exec_crf_test(ingredient_text, "RecipeParse.crfmodel")
    print(_convert_crf_output_to_json(crf_output.split('\n')))
    
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         prog='Ingredient Phrase Tagger',
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('-m', '--model-file', required=True)
#     main(parser.parse_args())

# %%
analyze_recipe("lasagna_sample.txt")
# %%
