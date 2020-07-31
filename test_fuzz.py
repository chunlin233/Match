import utils1
import process
import fuzz
from match import name_array_split, email_array_split

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
    result = process.extract(email[0], name_array, scorer=fuzz.partial_token_set_ratio, limit=2)
    print(result)
    result = process.extractOne(email[0], name_array, scorer=fuzz.partial_token_set_ratio)
    print(result)

    # 将字母和数字以外的字符用空格替代，全小写
    print(utils1.full_process(n1))