import utils1
import process
import fuzz
from match import name_array_split, email_array_split, match_full_short_name
import re

if __name__ == "__main__":

    # 全匹配，对顺序不敏感
    print(fuzz.ratio('zhang, ZY', 'zhangzy'))
    # 搜索匹配，对顺序不敏感
    print(fuzz.partial_ratio('zhang, ZY', 'zhangzy'))

    # 对字符串进行排序
    print(fuzz._process_and_sort('zhang, CY', False, True))
    # 先执行_process_and_sort， 再全匹配
    print(fuzz.token_sort_ratio('zhangzynpc', 'ZY, zhang'))
    # 先执行_process_and_sort， 再搜索匹配
    print(fuzz.partial_token_sort_ratio('zhangzynpc', 'ZY, zhang'))

    # 先执行_process_and_sort, 过滤重复词， 再全匹配
    print(fuzz.token_set_ratio('zhangzynpc', 'ZY, zhang, zhang'))
    # 先执行_process_and_sort, 过滤重复词， 再搜索匹配
    print(fuzz.partial_token_set_ratio('zhangzynpc', 'ZY, zhang, zhang'))


    n1 = 'Zhang, CS; Chen, J; Sun, LW; Zhang, P; Liu, Y; Chen, L; Yang, ZL; Pang, BB; Huang, YL; Sun, GG; Huang, CQ'
    n2 = 'Nair, AK; Kumari, P; Kamalakar, MV; Ray, SJ'
    n3 = 'Cui, P; Zeng, J; Peng, HW; Choui, JH; Li, ZY; Zeng, CG; Shih, CK; Perdew, JP; Zhang, ZY'
    n4 = 'Arif, S; Faraz, A'
    name_array = name_array_split(n2)

    e1 = 'inpc_zhang@163.com'
    e2 = 'ray@qq.com'
    e3 = 'zhangzy@ustc.edu.cn'
    e4 = 'suneela.hu@gmail.com; ahmad.faraz@tyndall.ie'

    email = email_array_split(e2)
    result = process.extract(email[0], name_array, scorer=fuzz.partial_token_set_ratio)
    print(result)
    result = process.extractOne(email[0], name_array, scorer=fuzz.partial_token_set_ratio)
    print(result)

    # 将字母和数字以外的字符用空格替代，全小写
    print(utils1.full_process(n1))

    print(type([1]) == list)

    email_array = ['suneela.hu@gmail.com; suneela.hu@gmail.com;', None,
                   'ahmad.faraz@tyndall.ie; suneela.hu@gmail.com; lalala', None]
    full_names = ['Zhang, CS; Chen, J', 'Cui, P; Zeng, J',
                  'Arif, S; Faraz, A', 'Peng, HW']
    all_author = []

    for i in range(len(email_array)):
        if email_array[i] is None:
            continue
        emails_one = email_array_split(email_array[i])
        for _ in range(len(emails_one)):
            all_author.append(full_names[i])

    print(all_author)

    count9 = 0
    full = []
    all_author = []
    for r in range(len(email_array)):
        if email_array[r] is None:
            count9 = count9 + 1
            continue
        each_full_author = full_names[r]
        full.append(each_full_author)
        emails_one = email_array_split(email_array[r])
        for b in range(len(emails_one)):
            all_author.append(full[r-count9])

    print(all_author)

    short_names = "Zhang, CS; Chen, J; Sun, LW; Zhang, P; Liu, Y; Chen, L; Yang, ZL; Pang, BB; Huang, YL; Sun, GG; Huang, CQ"
    short_names = name_array_split(short_names)
    full_names = "Zhang, Changsheng; Chen, Jie; Sun, Liangwei; Zhang, Pei; Liu, Yi; Chen, Liang; Yang, Zhaolong; Pang, Beibei; Huang, Yalin; Sun, Guangai; Huang, Chaoqiang"
    full_names = name_array_split(full_names)
    rp_names = "Zhang, CS (reprint author), Inst Nucl Phys & Chem, Key Lab Neutron Phys CAEP, Mianyang 621999, Sichuan, Peoples R China."
    rp_names = rp_names = re.findall(r'[; ]?(.*?)\s\(reprint author\).*?\.', rp_names)
    print(rp_names)
    print(match_full_short_name(short_names, full_names, rp_names))

    splited_rp_names = []
    for rp_name in rp_names:
        rp_name = rp_name.split(';')
        [splited_rp_names.append(r.strip()) for r in rp_name]

    print(splited_rp_names)

    name = 'chunlin'
    name2 = 'chunlin; daiqiang'
    print(name.split(';'))
    print(name2.split(';'))