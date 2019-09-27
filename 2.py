import re
import json

ret = []
direct_city={"北京","天津","上海","重庆"}
region_dict={"内蒙古":"内蒙古自治区","广西":"广西壮族自治区","宁夏":"宁夏回族自治区","新疆":"新疆维吾尔自治区","西藏":"西藏自治区"}
help_Lv3 = {"市","区","县"}
help_Lv4 = {"街道","镇","乡"}

def getNums(info):
    res = re.search("[0-9]{11}", info)
    if res:
        return res.group(0)
    return "Can‘t find a phone num"

def delNums(info):
    return re.sub("[0-9]{11}", "", info)

def getLv6(cur_addr):
    res = re.match(r"[0-9]+号?", cur_addr)
    if res:
        ret[5] = res.group(0)
        cur_addr = re.sub(r"[0-9]+号", "", cur_addr)
    ret[6] = cur_addr
    return

def getLv5(cur_addr):
    #print('Lv5' + cur_addr)
    if lv == 1:
        ret[4] = cur_addr
        return
    res = re.match(r".*(路|街|巷|弄)", cur_addr)
    if res:
        ret[4] = res.group(0)
        cur_addr = re.sub(r".*(路|街|巷|弄)", '', cur_addr)
        getLv6(cur_addr)
        return


def getLv4(cur_addr, cur_path):
    if ret[2] == '':
        for tem in help_Lv4:
            p = cur_addr.find(tem)
            if p >= 0:
                ret[3] = cur_addr[:p + len(tem)]
                cur_addr = cur_addr[p + len(tem):]
                break
        getLv5(cur_addr)
        return
    for key in cur_path:
        street = cur_path[key]['n']
        pos = cur_addr.find(street)
        if pos >= 0:
            if cur_addr[pos + len(street)] in help_Lv4:
                street = street + cur_addr[pos + len(street)]
            elif cur_addr[pos + len(street):pos + len(street) + 2] in help_Lv4:
                street = street + cur_addr[pos + len(street):pos + len(street) + 2]
            ret[3] = street
            getLv5(cur_addr[pos + len(street):])
            return
    getLv5(cur_addr)
    return

def getLv3(cur_addr, cur_path):
    for key in cur_path:
        city = cur_path[key]['n']
        pos = cur_addr.find(city)
        if pos >= 0:
            if cur_addr[pos + len(city)] in help_Lv3:
                city = city + cur_addr[pos + len(city)]
            ret[2] = city
            getLv4(cur_addr[pos + len(city):], cur_path[key]['c'])
            return
    getLv4(cur_addr, cur_path[key]['c'])
    return
def getLv2(cur_addr, cur_path):
    for key in cur_path:
        country = cur_path[key]['n']
        pos = cur_addr.find(country)
        if pos >= 0:
            ret[1] = country + "市"
            getLv3(cur_addr[pos + len(country):], cur_path[key]['c'])
            return
    for key in cur_path:
        getLv3(cur_addr, cur_path[key]['c'])
        return

def getLv1(cur_addr, cur_path):
    try:
        for key in cur_path:
            prov = cur_path[key]['n']
            pos = cur_addr.find(prov)
            if pos >= 0:
                if prov in direct_city:
                    ret[0] = prov
                    ret[1] = prov + "市"
                    getLv2(cur_addr[pos + len(prov):], cur_path[key]['c'])
                    break
                else:
                    ok = True
                    for fi, se in region_dict.items():
                        if fi == prov:
                            ok = False
                            ret[0] = fi
                            ret[1] = se
                    if ok:
                        ret[0] = prov + "省"
                getLv2(cur_addr[pos + len(prov):], cur_path[key]['c'])
    except:
        return

input_json = open(r'E:/031702126/031702126.json', 'rb')

data = json.load(input_json)
out_list = []
# in_info = open(r'C:/031702126/in.txt', 'r', encoding='utf-8').read()
in_info = input()
in_list = in_info.split()

for info in in_list:
    try:
        ret.clear()
        for i in range(10):
            ret.append('')
        lv = int(info[0])
        phoneNum = getNums(info)
        addr = delNums(info)
        addr = addr.replace('.', '')
        tem = addr[2:]
        name = tem.split(',')[0]
        cur_addr = tem.split(',')[1]
        getLv1(cur_addr, data)
        tem_addr_list = []
        tem_addr_list.clear()
        if lv == 1:
            for i in range(5):
                tem_addr_list.append(ret[i])
        else:
            for i in range(7):
                tem_addr_list.append(ret[i])
        tem_out = {}
        tem_out.clear()
        tem_out["姓名"] = name
        tem_out["手机"] = phoneNum
        tem_out["地址"] = tem_addr_list
        out_list.append(tem_out)
        out_json = json.dumps(tem_out, ensure_ascii=False)
        print(out_json)
    except:
        continue
# print(out_list)
# out_file = open(r'C:/031702126/Address/out.txt', 'w', encoding='utf-8')
# out_file.write(json.dumps(out_list, indent=4).encode('utf-8').decode('unicode_escape'))