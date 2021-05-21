import os
import json
import sys

def load_metrics(path, agg="median"):
    data = []
    for r in os.listdir(path):
        rpath = os.path.join(path, r) # run path
        if not os.path.isdir(rpath):
            continue
        for j in os.listdir(rpath):
            if os.path.splitext(j)[1] == ".json":
                break
        jpath = os.path.join(rpath, j) # path to metrics json
        data_json = json.load(open(jpath, "r"))
        method = data_json['config']['data']['method'][:-4]
        dataset = data_json['config']['data']['dataset']
        for pair, metrics in data_json['detailed'].items():
            sample = {
                "dataset": dataset,
                "method": method,
                "pair": pair,
            }
            sample.update(metrics)
            data.append(sample)
    return data

if __name__ == "__main__":
    data = load_metrics(sys.argv[1], agg="median")
    with open('vega-metrics/data2.json', 'w') as json_file:
        json.dump(data, json_file)
