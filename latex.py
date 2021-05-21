import os
import json
import sys
import numpy as np

from vega import valid

"""
data[method][dataset][m] = [p]
"""

def load_metrics(path, agg):
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

        if method not in data:
            data[method] = {}
        data[method][dataset] = {}
        for pair, metrics in data_json['detailed'].items():
            if not valid(dataset, pair):
                continue
            for m, v in metrics.items():
                if m not in data[method][dataset]:
                    data[method][dataset][m] = []
                data[method][dataset][m].append(v)

    for method in data.keys():
        for dataset in data[method].keys():
            for m in data[method][dataset].keys():
                data[method][dataset][m] = np.array(data[method][dataset][m])
                if agg == "median":
                    data[method][dataset][m] = np.median(data[method][dataset][m])
                elif agg == "mean":
                    data[method][dataset][m] = np.mean(data[method][dataset][m])

    return data


def load_metrics_from_summary(path, agg):
    data = {} # method => metrics x datasets
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

        if method not in data:
            data[method] = {}
        data[method][dataset] = {}
        for m, v in data_json["summary"][agg].items():
            if m in ["psnr", "ssim", "lpips"]:
                data[method][dataset][m] = v
    return data

def print_latex_table(data, table="eval"):
    metrics = ["psnr_masked", "ssim", "lpips"]
    if table == "eval":
        methods = ["si_mpi", "synsin", "photo3d", "shih", "ours"]
        datasets = ["spaces", "mc", "re10k"]
    elif table == "cnn":
        datasets = ["spaces"]
        methods = [
            "ours_100k",
            "ours_f274140538",
            "ours_f274140594",
            "ours_f274140638",
            "ours_f274140566",
            "ours_f274140522",
        ]
    elif table == "feat":
        datasets = ["spaces"]
        methods = [
            "ours_100k",
            "ours_f268032071",
            "ours_f274151488",
            "ours_f274151551",
            "ours_f274163133",
            "ours_f274163161"
        ]

    top = {}
    second = {}
    for method in methods:
        for dataset in datasets:
            if dataset not in top and dataset not in top:
                top[dataset] = {}
                second[dataset] = {}
            for metric in metrics:
                value = data[method][dataset][metric]
                # Seeing for the first time
                if metric not in top[dataset]:
                    if metric in ["psnr_masked", "ssim"]:
                        top[dataset][metric] = (sys.float_info.min, None)
                        second[dataset][metric] = (sys.float_info.min, None)
                    else:
                        top[dataset][metric] = (sys.float_info.max, None)
                        second[dataset][metric] = (sys.float_info.max, None)

                if metric in ["psnr_masked", "ssim"]:
                    if value > top[dataset][metric][0]:
                        second[dataset][metric] = top[dataset][metric]
                        top[dataset][metric] = (value, method)
                    elif value > second[dataset][metric][0]:
                        second[dataset][metric] = (value, method)
                else:
                    if value < top[dataset][metric][0]:
                        second[dataset][metric] = top[dataset][metric]
                        top[dataset][metric] = (value, method)
                    elif value < second[dataset][metric][0]:
                        second[dataset][metric] = (value, method)
    print(json.dumps(top, indent=2))
    print(json.dumps(second, indent=2))
    for method in methods:
        if method == "photo3d":
            print("One-shot 3D Photos~\\cite{kopf2020one}")
        elif method == "si_mpi":
            print("Single-view MPI~\\cite{tucker2020single}")
        elif method == "synsin":
            print("SynSin~\\cite{wiles2020synsin}")
        elif method == "shih":
            print("3D Photos Inpainting~\cite{shih20203d}")
        elif method == "ours":
            print("\\emph{Ours}")
        elif method == "ours_100k":
            if table == "cnn":
                print("MiDaS2")
            elif table == "feat":
                print("Learned + depths + dirs.\\ + color $(\\feat_\\refview, z_\\refview, \\direction_\\refview, \\col_\\refview)$")
        elif method == "ours_f274140538":
            print("MiDaS0 (f274140538)")
        elif method == "ours_f274140594":
            print("U-Net (f274140594)")
        elif method == "ours_f274140638":
            print("No Feature (f274140638)")
        elif method == "ours_f274140566":
            print("Hourglass (f274140566)")
        elif method == "ours_f274140522":
            print("MiDaS1 (f274140522)")
        elif method == "ours_f268032071":
            print(method)
        elif method == "ours_f274151488":
            print(method)
        elif method == "ours_f274151551":
            print(method)
        elif method == "ours_f274163133":
            print(method)
        elif method == "ours_f274163161":
            print(method)

        s = f"   "
        for dataset in datasets:
            for metric in metrics:
                value = data[method][dataset][metric]
                if top[dataset][metric][1] == method:
                    lb, rb = "\\textbf{", "}"
                elif second[dataset][metric][1] == method:
                    lb, rb = "\\underline{", "}"
                else:
                    lb, rb = "", ""
                s += f" & {lb}{value:0.3f}{rb}"
        s += "\\\\"
        print(s)


if __name__ == "__main__":
    data = load_metrics(sys.argv[1], agg="median")
    print_latex_table(data, sys.argv[2])
