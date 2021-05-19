import os
import json
import sys

def load_metrics(path, agg="median"):
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

def print_latex_table(data):
    methods = ["si_mpi", "synsin", "photo3d", "ours"]
    datasets = ["spaces", "mc", "re10k"]
    metrics = ["psnr", "ssim", "lpips"]

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
                    if metric in ["psnr", "ssim"]:
                        top[dataset][metric] = (sys.float_info.min, None)
                        second[dataset][metric] = (sys.float_info.min, None)
                    else:
                        top[dataset][metric] = (sys.float_info.max, None)
                        second[dataset][metric] = (sys.float_info.max, None)

                if metric in ["psnr", "ssim"]:
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
        elif method == "ours":
            print("\\emph{Ours}")
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
    print_latex_table(data)
