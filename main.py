import sys
import os
import numpy as np
from base import *

import matplotlib.pyplot as plt

class Node:
    def __init__(self, win_size, pos, type="mp"):
        self.win_size = win_size
        self.pos = pos
        self.type = type

    def __str__(self):
        return "{"+f"win:{self.win_size},pos:{self.pos},type:{self.type}"+"}"

class Cluster:
    def __init__(self, node, fft_win_size, threshold=150):
        self.max_value = node.pos
        self.min_value = node.pos
        self.node_list = [node]
        self.fft_win_size = fft_win_size
        self.threshold = threshold
        
        self.has_lu = False
        self.mp_d = {}
        self.hs_d = {}

        self.mp_cnt = 0
        self.hs_cnt = 0

        self._update_LRH(node)
    
    def calc_score(self):
        score = 0

        score += self.mp_cnt * 0.5

        score += self.hs_cnt * 1.25

        if self.has_lu:
            score += 1.5

        if self.has_lu and self.hs_cnt >= 2 and self.mp_cnt >= 5:
            score += 3 # 95 <= 50

        if self.mp_cnt >= 4:
            score += 0.5 # 55 <= 150

        if self.fft_win_size > 250 and self.fft_win_size <= 500:
            if self.hs_cnt >= 4:
                score += 2 # 62
        
        if self.fft_win_size <= 50:
            if self.mp_cnt >= 3:
                score += 1 # 150

        if self.fft_win_size <= 150 and self.fft_win_size > 50:
            if self.mp_cnt >= 7:
                score += 0.5 # 70

        return score


    def _update_LRH(self, node):
        if node.type == "lu":
            self.has_lu = True

        if node.type == 'mp':
            self.mp_d[node.win_size] = 1
            self.mp_cnt += 1

        if node.type == 'hs':
            self.hs_d[node.win_size] = 1
            self.hs_cnt += 1

    def __str__(self):
        n_l_str = '['+','.join([str(n) for n in self.node_list])+']'
        return f'score:{self.calc_score()}, lu:{self.has_lu}, ' + f'node_cnt:{self.node_count()}'+', nl:'+ n_l_str

    def node_count(self):
        return len(self.node_list)

    def dist(self, pos):
        if self.max_value == -1:
            return 0
        else:
            if pos > self.max_value:
                return pos - self.max_value
            elif pos <= self.max_value and pos >= self.min_value:
                return 0
            else: #pos < self.min_value:
                return self.min_value - pos

    def add(self, node):
        if self.dist(node.pos) > self.threshold:
            return False

        if node.pos > self.max_value:
            self.max_value = node.pos
        if node.pos < self.min_value:
            self.min_value = node.pos
        self.node_list.append(node)

        self._update_LRH(node)

        return True

    def get_mean_pos(self):
        l = [n.pos for n in self.node_list]
        return int(np.mean(l))

    def get_min_mp_pos(self):
        print("==========>get_min_mp_pos")
        ret = -1
        for n in self.node_list:
            if n.type == 'mp':
                if ret == -1:
                    ret = n.pos
                else:
                    if n.pos < ret:
                        ret = n.pos
        return ret



def topk(s, k, win_size):
    ret = []
    s = np.array(s).copy()

    for _ in range(k):
        max_value_idx = np.argmax(s)
        if s[max_value_idx] == -np.inf:
            break

        ret.append(max_value_idx)

        left = max(0, int(max_value_idx-win_size*2))
        right = min(len(s), int(max_value_idx+win_size*2))
        s[left:right] = -np.inf
    
    return ret

class WinData:
    def __init__(self, win_size):
        self.win_size = win_size
        self.mp = []
        self.max_k_idx_l = []

        self.hs = None

    def gen_mp(self, train_size, train, test, fft_win_size):
        _, _, self.mp = mp_detect_abjoin(test, train, self.win_size)

        k = 3
        factor = 0.9
        if fft_win_size <= 50:
            factor = 0.8 # 8

        if fft_win_size > 550:
            k = 2
            factor = 0.8

        max_k_idx_l = topk(self.mp, k, self.win_size)

        max_value = self.mp[max_k_idx_l[0]]

        self.max_k_idx_l = []
        for idx in max_k_idx_l:
            value = self.mp[idx]
            if value >= factor * max_value:
                self.max_k_idx_l.append(idx + self.win_size//2)


class HotsaxData:
    def __init__(self, win_size):
        self.win_size = win_size
        self.hs = None

    def gen_hs(self, file_no):
        self.hs = read_hotsax(self.win_size, file_no)


def prepare(ctx):
    win_size_l = ctx['win_size_l']
    all_data = ctx['all_data']
    train = ctx['train']
    test = ctx['test']
    train_size = ctx['train_size']
    file_no = ctx['file_no']
    fft_win_size = ctx['fft_win_size']

    win_data_l = []
    for win_size in win_size_l:
        wd = WinData(win_size)
        wd.gen_mp(train_size, train, test, fft_win_size)
        win_data_l.append(wd)
    ctx['win_data_l'] = win_data_l

    hs_win_data_l = []
    hs_win_size_l = ctx['hs_win_size_l']
    for win_size in hs_win_size_l:
        hd = HotsaxData(win_size)
        hd.gen_hs(file_no)
        hs_win_data_l.append(hd)
    ctx['hs_win_data_l'] = hs_win_data_l

    
    lu_score_l = read_lu_dd_02(file_no)
    ctx['lu_score'] = lu_score_l
    ctx['lu_max_score_pos'] = train_size + np.argmax(lu_score_l)
    ctx['lu_score_0.2'] = lu_score_l



def _mp_cluster_add_node(cluster_l, node, fft_win_size, distance_threshold):
    has_added_to_cluster = False
    for c in cluster_l:
        if c.add(node):
            has_added_to_cluster = True
    if not has_added_to_cluster:
        cluster_l.append(Cluster(node, fft_win_size, distance_threshold))

def mp_cluster(ctx):
    train_size = ctx['train_size']
    train = ctx['train']
    test = ctx['test']
    win_size_l = ctx['win_size_l']
    fft_win_size = ctx['fft_win_size']
    win_data_l = ctx['win_data_l']
    hs_win_data_l = ctx['hs_win_data_l']

    distance_threshold = (fft_win_size//100 + 1)*100
    if distance_threshold < 100: distance_threshold = 100
    if distance_threshold > 300: distance_threshold = 300

    distance_threshold = 200
    if fft_win_size <= 450 and fft_win_size > 350:
        distance_threshold = 400
    elif fft_win_size > 550:
        distance_threshold = 550
    print ("distance_threshold:", distance_threshold)

    cluster_l = []
    _mp_cluster_add_node(cluster_l, Node(-1, ctx['lu_max_score_pos'], "lu"), fft_win_size, distance_threshold)

    for wd in win_data_l:
        for pos in wd.max_k_idx_l:
            node = Node(wd.win_size, pos + train_size, "mp")
            _mp_cluster_add_node(cluster_l, node, fft_win_size, distance_threshold)

    for hd in hs_win_data_l:
        node = Node(hd.win_size, hd.hs[0] + train_size, "hs")
        _mp_cluster_add_node(cluster_l, node, fft_win_size, distance_threshold)

    
    cluster_l.sort(key=lambda n: n.node_count(), reverse=True)
    
    ctx['cluster_l'] = cluster_l

    for c in cluster_l:
        print(c)


def adjust_good_lu(ctx):
    fft_win_size = ctx['fft_win_size']
    train_size = ctx['train_size']
    ctx['good_lu'] = False
    lu_score = ctx['lu_score']
    
    two_side_win = 100
    factor = 0.8

    if lu_score is not None:
        good_lu = True
        lu_max_v_idx = np.argmax(lu_score)
        lu_max_v = lu_score[lu_max_v_idx]
        for i in range(lu_max_v_idx+two_side_win, len(lu_score)):
            v = lu_score[i]
            if v > lu_max_v * factor:
                good_lu = False
                break
        if good_lu:
            for i in range(0, lu_max_v_idx-two_side_win):
                v = lu_score[i]
                if v > lu_max_v * factor:
                    good_lu = False
                    break
        
        if good_lu:
            ctx['good_lu'] = True
            ctx['good_lu_opos'] = lu_max_v_idx + train_size

    print("good_lu:", ctx['good_lu'])

def adjust_good_test_1(ctx):
    test = ctx['test']
    train_size = ctx['train_size']

    good_test_1 = True
    max_v_idx = np.argmax(test)
    max_v = test[max_v_idx]
    for i in range(max_v_idx+100, len(test)):
            v = test[i]
            if v > max_v * 0.8:
                good_test_1 = False
                break
    if good_test_1:
        for i in range(0, max_v_idx-100):
            v = test[i]
            if v > max_v * 0.8:
                good_test_1 = False
                break
    if good_test_1:
        ctx['good_test_1'] = True
        ctx['good_test_1_opos'] = max_v_idx + train_size
    else:
        ctx['good_test_1'] = False
    print("good_test_1:", ctx['good_test_1'])

def _adjust_by_min_mp_pos(ctx, cluster):
    ctx['outlier_pos'] = cluster.get_min_mp_pos()
    if ctx['outlier_pos'] < 0:
        print ("warning: outlier_pos < 0", ctx['outlier_pos'])
        ctx['outlier_pos'] = cluster.get_mean_pos()

def _adjust_pos_cause_lu(ctx, cluster):
    fft_win_size = ctx['fft_win_size']

    if cluster.has_lu:
        pos = 0
        for n in cluster.node_list:
            if n.type == 'lu':
                pos = n.pos
                break
        ctx['outlier_pos'] = pos
    else:
        if fft_win_size > 550:
            _adjust_by_min_mp_pos(ctx, cluster)
        else:
            ctx['outlier_pos'] = cluster.get_mean_pos()


def _select_max_cluster(ctx, cluster_l):
    max_score = cluster_l[0].calc_score()
    max_cluster = cluster_l[0]
    for c in cluster_l[1:]:
        if c.calc_score() > max_score:
            max_score = c.calc_score()
            max_cluster = c

    _adjust_pos_cause_lu(ctx, max_cluster)

def _find_cluster_contains_lu(cluster_l):
    for c in cluster_l:
        for n in c.node_list:
            if n.type == 'lu':
                return c
    return None

def select_outlier_pos(ctx):
    win_size_l = ctx['win_size_l']
    cluster_l = ctx['cluster_l']
    fft_win_size = ctx['fft_win_size']

    if 'good_test_1' in ctx and ctx['good_test_1']:
        ctx['outlier_pos'] = ctx['good_test_1_opos']
        ctx['outlier_pos_color'] = "red"
        return 

    ctx['outlier_pos_color'] = "black"
    # check c is good
    yellow_l = []
    for c in cluster_l:
        if len(c.mp_d) == len(win_size_l) and (c.has_lu or len(c.hs_d) >= 2):
            yellow_l.append(c)
            
    if len(yellow_l) > 0:
        _select_max_cluster(ctx, yellow_l)
        ctx['outlier_pos_color'] = "yellow"
        return

    max_score = cluster_l[0].calc_score()
    max_cluster = cluster_l[0]
    for c in cluster_l[1:]:
        if c.calc_score() > max_score:
            max_score = c.calc_score()
            max_cluster = c

    if ctx['good_lu']:
        c = _find_cluster_contains_lu(cluster_l)
        if len(c.node_list) == 1 and len(max_cluster.hs_d) >= 4 and fft_win_size > 450 and fft_win_size <= 550:
            # 186
            pass
        else:
            ctx['outlier_pos'] = ctx['good_lu_opos']
            ctx['outlier_pos_color'] = "red"
            return

    _adjust_pos_cause_lu(ctx, max_cluster)



def visualize_lu(ctx, lu_score, ylabel, subfigure_count, fig_no):
    file_no = ctx['file_no']
    train_size = ctx['train_size']
    train = ctx['train']
    test = ctx['test']

    if lu_score is not None:
        plt.subplot(subfigure_count, 1, fig_no)
        plt.ylabel(ylabel, rotation=0, ha='right')
        plt.plot([i for i in range(len(train))], zl(len(train)))
        plt.plot([i + train_size for i in range(len(lu_score))], lu_score)
        if len(lu_score) < len(test):
                plt.plot([i + train_size + len(lu_score) for i in range(len(test)- len(lu_score))], 
                            zl(len(test)- len(lu_score)))
        lu_anomaly_score_max_index = np.argmax(lu_score) + train_size
        plt.axvline(lu_anomaly_score_max_index, color="black")
        plt.yticks([])

def visualize(ctx):
    file_no = ctx['file_no']
    train_size = ctx['train_size']
    train = ctx['train']
    test = ctx['test']
    all_data = ctx['all_data']
    win_size_l = ctx['win_size_l']

    hs_win_size_l = ctx['hs_win_size_l']
    
    fft_win_size = ctx['fft_win_size']
    

    subfigure_count = len(win_size_l) + len(hs_win_size_l) + 2 + 1 # train, test, lu, hs, rra

    plt.cla()
    plt.subplot(subfigure_count, 1, 1)
    plt.title(f"{file_no} - fft_win_size={fft_win_size}")
    plt.plot([i for i in range(len(train))], train, color="green")
    plt.plot([i + train_size for i in range(len(test))], zl(len(test)), color="white")

    plt.yticks([])

    visualize_lu(ctx, ctx['lu_score_0.2'], "lu2", subfigure_count, 3)

    fig_no = 4
    hs_win_data_l = ctx['hs_win_data_l']
    for hd in hs_win_data_l:
        if hd.hs is not None:
            plt.subplot(subfigure_count, 1, fig_no)
            plt.ylabel(f"h{hd.win_size}", rotation=0, ha='right')
            plt.plot([i for i in range(len(all_data))], zl(len(all_data)))
            plt.axvline(hd.hs[0] + train_size, color="black")
            plt.yticks([])
            fig_no += 1


    win_data_l = ctx['win_data_l']
    for idx, wd in enumerate(win_data_l):
        profile = wd.mp
        plt.subplot(subfigure_count, 1, fig_no+idx)
        plt.ylabel(f"{wd.win_size}", rotation=0, ha='right')
        plt.plot([i for i in range(len(train))], zl(len(train)))
        plt.plot([i + train_size for i in range(len(profile))], profile)
        if len(profile) < len(test):
            plt.plot([i + train_size + len(profile) for i in range(len(test)- len(profile))], zl(len(test)- len(profile)))

        for pos in wd.max_k_idx_l:
            plt.axvline(train_size + pos, color="black")
        plt.yticks([])
        

    plt.subplot(subfigure_count, 1, 2)
    plt.plot([i for i in range(len(train))], zl(len(train)), color="white")
    plt.plot([i + train_size for i in range(len(test))], test, color="blue")


    plt.axvline(ctx['outlier_pos'], color=ctx["outlier_pos_color"])

    plt.xticks([])
    plt.show()


def finish(ctx, file_no, pos):
    out_f = ctx['out_file']
    out_f.write(f"{file_no},{pos}\n")
    out_f.flush()
    print(f"{file_no},{pos}")
    sys.stdout.flush()


if __name__ == "__main__":
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "samples"))
    result_file_name_prefix = sys.argv[0].split(".")[0]
    start_file_no = int(sys.argv[1])

    output_file_path = os.path.join("output", result_file_name_prefix+".csv")
    of = open(output_file_path, "a+")
    of.write("No.,location\n")

    file_filter_d = {}
    if len(sys.argv) == 3:
        for line in open(sys.argv[2]):
            file_filter_d[int(line.strip())] = 1
    else:
        for i in range(1, 251):
            file_filter_d[i] = 1

    for sample_file in os.listdir(sample_dir):
        ctx = {}
        ctx['out_file'] = of

        file_no = int(sample_file.split("_")[0])
        if file_no < start_file_no:
            continue

        if file_no not in file_filter_d:
            continue

        ctx['file_no'] = file_no

        # if file_no in [239,240,241]:
        #     finish(ctx, file_no, 0)
        #     continue

        train_size = get_train_size_from_filename(sample_file)
        ctx['train_size'] = train_size
        print("train size:", ctx['train_size'])

        all_data = []
        for line in open(os.path.join(sample_dir, sample_file)):
            all_data.append(float(line.strip()))
        train = all_data[:train_size].copy()
        test = all_data[train_size:].copy()

        fft_win_size = cal_window_size(train)

        ctx['fft_win_size'] = fft_win_size

        ctx['hs_win_size_l'] = [25, 50, 75, 100, 125, 150, 175, 200, 250, 300]
        if fft_win_size <= 50:
            ctx['hs_win_size_l'] = [25, 50, 75, 100, 125, 150]
        elif fft_win_size <= 150:
            ctx['hs_win_size_l'] = [100, 125, 150, 175, 200]
        elif fft_win_size <= 250:
            ctx['hs_win_size_l'] = [100, 125, 150, 175, 200, 250]
        elif fft_win_size <= 350:
            ctx['hs_win_size_l'] = [100, 125, 150]
        elif fft_win_size <= 450:
            ctx['hs_win_size_l'] = [25, 50, 75]
        elif fft_win_size <= 550:
            ctx['hs_win_size_l'] = [100, 125, 150, 175, 200, 250, 300, 350, 400, 450, 500, 550]
        elif fft_win_size <= 1600:
            ctx['hs_win_size_l'] = [100, 125, 150, 175, 200, 250, 300]
        else:
            ctx['hs_win_size_l'] = [100, 125, 150, 175, 200, 250, 300]


        ctx['win_size_l'] = [25, 50, 75, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
        if fft_win_size <= 50:
            ctx['win_size_l'] = [25, 50, 75, 100, 125, 150, 175, 200, 250]
        elif fft_win_size <= 150:
            ctx['win_size_l'] = [25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400]
        elif fft_win_size <= 250:
            ctx['win_size_l'] = [25, 50, 75, 100, 125, 150, 175, 200, 250, 300, 350, 400]
        elif fft_win_size <= 350:
            ctx['win_size_l'] = [25, 50, 75, 100, 125]
        elif fft_win_size <= 450:
            ctx['win_size_l'] = [200, 250, 300, 350, 400, 450]
        elif fft_win_size <= 550:
            ctx['win_size_l'] = [500, 550, 600, 650, 700, 750, 800, 900, 1000]
        elif fft_win_size <= 1600:
            ctx['win_size_l'] = [1600]
        else:
            ctx['win_size_l'] = [100, 125, 150, 175, 200, 250, 300, 350, 400]      

        ctx['all_data'] = all_data
        ctx['train'] = train
        ctx['test'] = test

        prepare(ctx)

        mp_cluster(ctx)

        adjust_good_lu(ctx)

        if fft_win_size <= 450 and fft_win_size > 350:
            adjust_good_test_1(ctx)

        select_outlier_pos(ctx)

        finish(ctx, file_no, ctx['outlier_pos'])

        #visualize(ctx)
    of.close()