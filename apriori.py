# coding=utf-8
from itertools import chain, combinations
from collections import defaultdict


def subsets(arr):
    """ 返回非空子集"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def return_item_with_min_support(item_set, transaction_list, min_support, freq_set):
    """
    计算在项集合中的项的支持度
    返回符合最小支持度的子集
   """
    _item_set = set()
    local_set = defaultdict(int)

    for item in item_set:
        for transaction in transaction_list:
            if item.issubset(transaction):
                freq_set[item] += 1
                local_set[item] += 1

    for item, count in local_set.items():
        support = float(count) / len(transaction_list)

        if support >= min_support:
            _item_set.add(item)

    return _item_set


def join_set(item_set, length):
    """
    得到下一阶的候选集
    """
    return set([
        i.union(j)  # 返回一个新的 set 包含 i 和 j 中的每一个元素
        for i in item_set
        for j in item_set if len(i.union(j)) == length
    ])


def getitem_set_transaction_list(data_iterator):
    """
    从数据集中将数据分离
    :param data_iterator:
    :return:
    item_set: 数据集中的所有项
    transaction_list: 所有行(交易)
    """
    transaction_list = list()
    item_set = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transaction_list.append(transaction)
        for item in transaction:
            item_set.add(frozenset([item]))  # Generate 1-item_sets
    return item_set, transaction_list


def run_apriori(data_iter, min_support, min_confidence):
    """
    apriori算法。
    Return
     - 项 (tuple, support)
     - 关联规则 ((pre_tuple, post_tuple), confidence)
    """
    item_set, transaction_list = getitem_set_transaction_list(data_iter)

    freq_set = defaultdict(int)  # 频繁集
    large_set = dict()

    # assoc_rules = dict()
    # Dictionary which stores Association Rules

    one_c_set = return_item_with_min_support(
        item_set,
        transaction_list,
        min_support,
        freq_set
    )

    current_l_set = one_c_set
    k = 2  # K阶频繁集
    while current_l_set != set([]):
        large_set[k - 1] = current_l_set
        current_l_set = join_set(current_l_set, k)
        current_c_set = return_item_with_min_support(
            current_l_set,
            transaction_list,
            min_support,
            freq_set
        )
        current_l_set = current_c_set
        k = k + 1

    def get_support(item):
        """
        得到每项的支持度
        """
        return float(freq_set[item]) / len(transaction_list)

    # 返回符合最小支持度和可信度的项
    to_ret_items = []
    for key, value in large_set.items():
        to_ret_items.extend(
            [(tuple(item), get_support(item)) for item in value]
        )

    # 返回关联规则
    to_ret_rules = []
    for key, value in large_set.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item) / get_support(element)
                    if confidence >= min_confidence:
                        to_ret_rules.append(
                            ((tuple(element), tuple(remain)), confidence)
                        )
    return to_ret_items, to_ret_rules


def print_results(items, rules):
    """
    打印出按照支持度排列的集合以及按照可信度排列规则
    """
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
    print "\n------------------------ RULES:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


def data_from_file(fname):
    """
    从文件中读取数据并生成一个生成器
    """
    file_iter = open(fname, 'r')
    for line in file_iter:
        line = line.strip('\n')
        record = frozenset(line.split(' '))
        yield record


if __name__ == "__main__":

    filename = 'test.csv'
    in_file = data_from_file(filename)
    minSupport = 0.1
    minConfidence = 0.7

    re_items, re_rules = run_apriori(in_file, minSupport, minConfidence)
    print_results(re_items, re_rules)
