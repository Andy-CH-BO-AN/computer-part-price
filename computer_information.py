import requests
from bs4 import BeautifulSoup
import main


class Coolpc:
    def __init__(self):
        self.url = 'http://www.coolpc.com.tw/evaluate.php'
        self.website = 'coolpc'
        self.cpu_dict = {}
        self.cpu_and_motherboard_dict = {}
        self.title_list = ['品牌小主機、AIO｜VR虛擬',
                           '手機｜平板｜筆電｜穿戴',
                           '酷！PC 套裝產線',
                           '處理器 CPU',
                           '主機板 MB',
                           '記憶體 RAM',
                           '固態硬碟 M.2｜SSD',
                           '傳統內接硬碟HDD',
                           '外接硬碟｜隨身碟｜記憶卡',
                           '散熱器｜散熱墊｜散熱膏',
                           '封閉式｜開放式水冷',
                           '顯示卡VGA',
                           '螢幕｜投影機｜壁掛',
                           'CASE 機殼(+電源)',
                           '電源供應器',
                           '機殼風扇｜機殼配件',
                           '鍵盤,鍵鼠｜搖桿｜椅',
                           '滑鼠｜鼠墊｜數位板',
                           'IP分享器｜網卡｜網通設備',
                           '網路NAS｜網路IPCAM',
                           '音效卡｜電視卡(盒)｜影音',
                           '喇叭｜耳機｜麥克風',
                           '燒錄器 CD/DVD/BD',
                           'USB週邊｜硬碟座｜讀卡機',
                           '行車紀錄器｜USB視訊鏡頭',
                           'UPS不斷電｜印表機｜掃描',
                           '介面擴充卡｜專業Raid卡',
                           '網路、傳輸線、轉頭｜KVM',
                           'WIN10｜APP應用｜禮物卡',
                           '福利品出清']
        self.cpu()

    def cpu(self):
        cpu_and_motherboard_dict = self.cpu_and_motherboard_dict
        title_list = self.title_list
        cpu_dict = self.cpu_dict
        website = self.website
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        computer_hardware = soup.find_all('tr', bgcolor='efefe0')
        # 硬體的標題
        for item in range(len(computer_hardware)):
            title = computer_hardware[item].find('td', class_='t').get_text().split('\n')[0]
            # 是否為cpu的標題
            if title.strip() == title_list[3].strip():

                computer_hardware_label = computer_hardware[item].find_all('optgroup')
                label_list = []
                # cpu的分類
                for category in computer_hardware_label:
                    label = category.get('label').split('(')[0].strip()
                    label_list.append(label)
                    cpu_dict[label] = {}
                    cpu_and_motherboard_dict[label] = {}

                computer_hardware_item = computer_hardware[item].find('option').text
                cpu_list = computer_hardware_item.split('\n')
                cpu_list[0] = ''
                cpu_list.remove(cpu_list[-1])
                cpu_list.remove(cpu_list[-1])
                print(cpu_list)
                label_count = 0
                print(cpu_dict)
                # cpu分出型號與其價格
                for cpu in range(len(cpu_list)):

                    if cpu_list[cpu] == '':
                        cpu_list[cpu] = label_count
                        print(cpu_list[cpu])
                        label_count += 1
                    elif '+' in str(cpu_list[cpu]):
                        cpu_price = \
                            int(cpu_list[cpu].split(',')[1].strip().
                                replace('★', '').replace('◆', '').
                                replace('熱賣', '').replace("", "").
                                split('$')[-1])
                        cpu_name = cpu_list[cpu].split(',')[0].replace('【狂】', '').strip()
                        cpu_and_motherboard_dict[label_list[label_count]] = {'processor name+MB': cpu_name,
                                                                             'price': cpu_price,
                                                                             '備註': 'cpu搭主板',
                                                                             'website': website}
                        processor_info = cpu_and_motherboard_dict[label_list[label_count]]
                        data = main.find_collection_single('CPU+MB', label_list[label_count],
                                                           {'processor name+MB': cpu_name})
                        if data == []:
                            print({'processor name+MB': cpu_name})
                            main.insert_collection('CPU+MB', label_list[label_count],
                                                   processor_info)
                        elif [i for i in data if i['price'] != cpu_price]:
                            main.update_collection('CPU+MB', label_list[label_count],
                                                   {'processor name+MB': cpu_name},
                                                   {'price': cpu_price})
                        print('cpu+主板:', 'name:', cpu_name, '\n', 'price:', cpu_price)
                    elif '↪' in str(cpu_list[cpu]):
                        print('推薦:', str(cpu_list[cpu]))
                    elif '❤' in str(cpu_list[cpu]):
                        print('推薦:', str(cpu_list[cpu]))
                    elif '搭機價' in str(cpu_list[cpu]):
                        cpu_price = \
                            int(cpu_list[cpu].split(',')[1].strip().
                                replace('★', '').replace('◆', '').
                                replace('熱賣', '').replace("", "").
                                split('$')[-1])
                        cpu_name = cpu_list[cpu].split(',')[0].replace('【搭機價】', ''). \
                            split('【')[0].replace('AMD', '').replace('Intel', '').strip()
                        cpu_dict[label_list[label_count]] = {'processor': cpu_name,
                                                             'price': cpu_price,
                                                             '備註': '【搭機價】',
                                                             'website': website}
                        processor_info = cpu_dict[label_list[label_count]]
                        data = main.find_collection_single('CPU', label_list[label_count],
                                                           {'processor': cpu_name, '備註': '【搭機價】'})

                        if data == []:
                            print({'processor': cpu_dict[label_list[label_count]]['processor']})
                            main.insert_collection('CPU', label_list[label_count],
                                                   processor_info)
                        elif [i for i in data if i['price'] != cpu_price and i['備註'] != '【搭機價】']:
                            pass
                        elif [i for i in data if i['price'] != cpu_price and i['備註'] == '【搭機價】']:
                            main.update_collection('CPU', label_list[label_count],
                                                   {'processor': cpu_price}, {'price': cpu_price})
                        print('【搭機價】:', 'name:', cpu_name, '\n', 'price:', cpu_price)
                    else:
                        # print(cpu)

                        cpu_price = \
                            int(cpu_list[cpu].split(',')[1].strip().
                                replace('★', '').replace('◆', '').
                                replace('熱賣', '').split('$')[-1])
                        cpu_name = cpu_list[cpu].split(',')[0].split('【')[0]. \
                            replace('AMD', '').replace('Intel', '').strip()
                        cpu_dict[label_list[label_count]] = {'processor': cpu_name,
                                                             'price': cpu_price,
                                                             '備註': '',
                                                             'website': website}
                        processor_info = cpu_dict[label_list[label_count]]
                        data = main.find_collection_single('CPU', label_list[label_count],
                                                           {'processor': cpu_name, '備註': ''})

                        if data == []:
                            main.insert_collection('CPU', label_list[label_count],
                                                   processor_info)
                        elif [i for i in data if i['price'] != cpu_price and i['備註'] == '']:
                            main.update_collection('CPU', label_list[label_count],
                                                   {'processor': cpu_name},
                                                   {'price': cpu_price})

                        print('name:', cpu_name, '\n', 'price:', cpu_price)


if __name__ == '__main__':
    Coolpc()
