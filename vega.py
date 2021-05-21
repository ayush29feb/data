import os
import json
import sys

RE10K_VALID_INDICIES = [
   0,  2,  4,  5,  6,  10,  11,  14,  18,  19,  21,  22,  24,  25,  27,  28,  29,  32,
   33,  36,  37,  40,  41,  43,  44,  45,  48,  50,  52,  54,  57,  58,  59,  61,  62,  65,
   68,  69,  70,  77,  78,  83,  84,  85,  86,  88,  90,  91,  93,  94,  98,  99, 104, 106,
   112, 115, 121, 123, 125, 128, 129, 131, 135, 137, 138, 144, 145, 146, 148, 150, 151, 153,
   154, 155, 156, 159, 160, 161, 163, 165, 168, 172, 173, 175, 176, 179, 180, 181, 183, 184,
   185, 187, 188, 189, 190, 191, 193, 195, 198, 200, 202, 203, 209, 211, 212, 214, 215, 217,
   219, 222, 225, 228, 229, 236, 238, 239, 240, 243, 245, 246, 248, 249, 250, 251, 252, 255,
   256, 257, 259, 262, 263, 268, 271, 273, 274, 276, 277, 278, 279, 280, 287, 289, 290, 294,
   295, 296, 299, 303, 307, 310, 314, 315, 319, 322, 323, 324, 325, 327, 328, 332, 333, 334,
   335, 337, 338, 339, 341, 342, 346, 348, 351, 352, 355, 357, 359, 362, 364, 365, 366, 369,
   370, 371, 373, 374, 376, 377, 379, 381, 382, 383, 385, 387, 388, 389, 390, 394, 396, 397,
   398, 399
]

def is_valid():
    return True


# Data Row
"""
{
    "dataset",
    "pair",
    "metric",
    "method_*"
}
"""

def load_metrics(path, agg="median"):
    data = {}
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
            for metric, value in metrics.items():
                key = (dataset, pair, metric)
                if key not in data:
                    data[key] = {
                        "dataset": dataset,
                        "pair": pair,
                        "metric": metric,
                    }
                data[key][method] = value
    return data.values()

if __name__ == "__main__":
    data = load_metrics(sys.argv[1], agg="median")
    with open('vega-metrics/data2.json', 'w') as json_file:
        json.dump(data, json_file)
