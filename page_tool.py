# coding: utf-8
import logging

log = logging.getLogger()

def gen_from_table(table_list, page, page_size):
    origin = [item[1] for item in table_list]
    count = sum(origin)
    judge = []
    judge_map = {}
    origin_snd = origin
    for i, v in enumerate(origin_snd):
        value = sum(origin_snd[:i+1])
        judge.append(value)
        if i == 0:
            judge_map[value] = ('', table_list[i][0])
        else:
            judge_map[value] = (table_list[i-1][0], table_list[i][0])
    return count, origin, judge, judge_map


def table_range_map(table_list):
    log.debug('table_range_map input=%s', table_list)
    data = {}
    before = 0
    for table in table_list:
        name, value = table
        log.debug('name=%s|value=%s|before=%s' % (name, value, before))
        data[name] = range(before+1, value+before+1)
        before += value
    # log.debug('table_range_map output=%s', data)
    return data


def gen_total_pages(count, page_size):
    pages, mod = divmod(count, page_size)
    if mod > 0:
        pages += 1
    return pages


def gen_page_range(pages, page_size):
    result = {}
    for i in range(1, pages+1):
        length = i * page_size
        ret = (length - page_size, length)
        result[i] = ret

    return result


def query_from(range_map, page, page_range):
    start_table = ''
    end_table = ''
    start, end = page_range.get(page)
    if start == 0:
        start += 1
    for key, values in range_map.iteritems():
        if start in values:
            start_table = key
        if end in values:
            end_table = key

        if start_table and end_table:
            break

    return start_table, end_table


def gen_one_limit_offset(range_map, table, start, end):
    values = range_map.get(table)
    if start == 0:
        offset = 0
    else:
        offset = values.index(start) + 1

    log.debug('start=%s|end=%s' % (start, end))
    count = end - start
    return count, offset


def gen_two_limit_offset(range_map, start_table, end_table, start, end):
    ret = []
    start_values = range_map.get(start_table)
    end_values = range_map.get(end_table)
    if start == 0:
        start += 1
        offset_start = 0
    else:
        offset_start = start_values.index(start) + 1
    count_start = len(start_values) - offset_start
    if count_start < 0:
        count_start = abs(count_start) + 1

    count_end = end_values.index(end) + 1
    offset_end = 0
    ret.append({start_table: [count_start, offset_start]})
    ret.append({end_table: [count_end, offset_end]})
    return ret