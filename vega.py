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

SPACES_VALID_INDICIES = [
   0,  1,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
  19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
  38, 40, 41, 42, 43, 45, 47, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
  63, 64, 65, 67, 68, 69, 70, 71, 72, 74, 75, 76, 77, 78, 79, 80, 81, 82,
  83, 84, 85, 86, 87, 88, 90, 91, 92, 94, 95, 96, 97, 98, 99,100,101,102,
 103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,
 121,122,124,125,126,127,128,129,130,132,133,134,135,137,138,139,140,141,
 142,143,144,145,146,147,148,149,150,151,153,154,155,156,157,158,159,160,
 161,162,163,164,165,166,167,168,169,170,171,172,174,175,176,177,178,179,
 180,181,182,184,185,186,187,188,189,191,192,193,194,195,196,197,198,199,
 201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,
 219,220
]

def valid(dataset, pair):
    if dataset == "spaces":
        return pair in [f"pair_{p:06}" for p in SPACES_VALID_INDICIES]
    elif dataset == "re10k":
        return pair in [f"pair_{p:06}" for p in RE10K_VALID_INDICIES]
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
            if not valid(dataset, pair):
                continue
            for metric, value in metrics.items():
                key = (dataset, pair, metric)
                if key not in data:
                    data[key] = {
                        "dataset": dataset,
                        "pair": pair,
                        "metric": metric,
                    }
                data[key][method] = value
    return list(data.values())

if __name__ == "__main__":
    data = load_metrics(sys.argv[1], agg="median")
    with open(f'vega-metrics/{sys.argv[2]}.json', 'w') as json_file:
        json.dump(data, json_file)
