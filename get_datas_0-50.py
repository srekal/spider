# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import xlwt
import os,base64
import requests as req
from PIL import Image
from io import BytesIO
import time 
print 'Hello World!'







url = 'https://www.grainger.cn/b-733.html'
print url
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

soups = soup.find_all('a',class_='cur')
for soup in soups:

    urls = 'https://www.grainger.cn'+soup.get('href')
    page = requests.get(urls)
    soup = BeautifulSoup(page.content, 'html.parser')
    pages = int(soup.find_all('label')[-1].get_text())
    for page_detail in range(int(pages)):
        url = urls+ '&sort=score&page='+ str(page_detail+1)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_details = soup.find('div',class_='proUL').find('ul',class_='clearfix').find_all('li')

        for soup_detail in soup_details:
            #这个是某个产品的
            img_url = soup_detail.find('div',class_='pic').find('img').get('src')
            product_url = soup_detail.find('a').get('href')
            url = 'https://www.grainger.cn'+product_url
            print url
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                name = (soup.find('h3').find_all('a')[-1].get_text())
            except:
                continue


            xls_name = name + '.xls'

            if os.path.exists(xls_name):
                print '已存在'
                print xls_name
                continue

                # try:
            workbook = xlwt.Workbook(encoding = 'ascii')
            worksheet = workbook.add_sheet('My Worksheet')
            worksheet.write(0, 0, label = u'名称')
            worksheet.write(0, 1, label = u'川拓型号')
            worksheet.write(0, 2, label = u'内部参考')
            worksheet.write(0, 3, label = u'技术参数/参数名称')
            worksheet.write(0, 4, label = u'技术参数/参数值')
            worksheet.write(0, 5, label = u'技术参数/单位')
            worksheet.write(0, 6, label = u'川拓品牌')
            worksheet.write(0, 7, label = u'供应商/价格')
            worksheet.write(0, 8, label = u'成本')
            worksheet.write(0, 9, label = u'销售价格')
            worksheet.write(0, 10, label = u'计量单位')
            worksheet.write(0, 11, label = u'产品种类')
            worksheet.write(0, 12, label = u'供应商/供应商产品代码')
            worksheet.write(0, 13, label = u'供应商/供应商产品名称')
            worksheet.write(0, 14, label = u'供应商/供应商型号')
            worksheet.write(0, 15, label = u'供应商/供应商品牌')
            worksheet.write(0, 16, label = u'供应商/最少数量')
            worksheet.write(0, 17, label = u'供应商/交货提前时间')
            worksheet.write(0, 18, label = u'Skippercode Custom/客户')
            worksheet.write(0, 19, label = u'Skippercode Custom/客户SKU')
            worksheet.write(0, 20, label = u'Skippercode Custom/客户产品名称')
            worksheet.write(0, 21, label = u'Skippercode Custom/客户型号')
            worksheet.write(0, 22, label = u'Skippercode Custom/客户品牌')
            worksheet.write(0, 23, label = u'体积')
            worksheet.write(0, 24, label = u'重量')
            worksheet.write(0, 25, label = u'重量计量单位')
            worksheet.write(0, 26, label = u'标签')
            worksheet.write(0, 27, label = u'包装方式')
            worksheet.write(0, 28, label = u'产地')
            worksheet.write(0, 29, label = u'面价')
            worksheet.write(0, 30, label = u'vip价')
            worksheet.write(0, 31, label = u'说明')
            worksheet.write(0, 32, label = u'供应商/供应商')
            worksheet.write(0, 33, label = u'小尺寸图像')
            end_data = []
            real_n = 0
            #  订货号
            num_data = []
            #  制造商型号
            type_data = []
            nums= soup.find('div',class_='leftTable2').find_all('tr',class_='trsku2 lefttr')
            for num in nums:
                num_details = num.find_all('td')

                end_data.append([])
                end_data[nums.index(num)].append(num_details[0].find('a').get_text())
                end_data[nums.index(num)].append(num_details[1].find('a').get_text())
                real_n +=1
            #技术参数
            paramas_data = []
            alls = soup.find('div',class_='rightTable1').find('tr',class_='pxTR').find_all('td')
            for all in alls:
                paramas_data.append(all.get_text())

            products= soup.find('div',class_='rightTable2').find_all('tr')
            paramas = []
            real_n = 0
            #所有参数
            for product in products:
                # print product
                paramas.append([])
                for product_detail in product.find_all('td'):
                    index = product.find_all('td').index(product_detail)
                    paramas[real_n].append({paramas_data[index]:product_detail.get_text()})
                end_data[real_n].append(paramas[real_n])
                real_n +=1
            #销售价格

            prices =  soup.find('div',class_='fixRightTable2').find_all('tr')
            real_n = 0
            for price in prices:
                for detail in price.find_all('td'):
                    try:
                        end_data[real_n].append(detail.find('span',class_='sales_price').get_text()[1:])
                        real_n+=1
                    except:pass

            try:
                response = req.get('http://'+img_url[2:]) # 将这个图片保存在内存
                file='/Users/apple/Desktop/gaj/%s.jpeg' % (name)
                with open(file, 'wb') as f:
                    f.write(response.content)

                # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
     
                    
                f = open(file)
                
                im = Image.open(file)
                w, h = im.size
                dImg = im.resize((100,100), Image.ANTIALIAS)
                # dImg.save(file)
                base64_data = base64.b64encode(f.read())
                image_data = base64_data.decode()

                if len(image_data) > 32767:
                    w, h = im.size
                    dImg = im.resize((int(w/3),int(h/3)), Image.ANTIALIAS)
                    # dImg.save(file)
                    base64_data = base64.b64encode(f.read())
                    image_data = base64_data.decode()
                    if len(image_data) > 32767:
                        w, h = im.size
                        dImg = im.resize((int(w/5),int(h/5)),Image.ANTIALIAS)
                        # dImg.save(file)
                        base64_data = base64.b64encode(f.read())
                        image_data = base64_data.decode()

            except:
                image_data='http://'+img_url[2:]



            n = 0
            for go in end_data:
                

                worksheet.write(n+1, 33, label = image_data)


                try:
                    product_detail = soup.find('div',class_='proDetailTit').find('div',class_='box').get_text();
                    
                except:product_detail=''
                product_categ = ''
                try:
                   
                    for categ in soup.find('div',class_='wrapper').find_all('a'):
                        product_categ +='/'+categ.get_text()
                
                except:
                    pass
                try:
                    worksheet.write(n+1, 0, label = name)
                    worksheet.write(n+1, 7, label = go[-1])
                    worksheet.write(n+1, 12, label = go[0])
                    worksheet.write(n+1, 2, label = go[1])
                    worksheet.write(n+1, 14, label = go[1])
                    worksheet.write(n+1, 31, label = product_detail)
                    worksheet.write(n+1, 11, label = product_categ)
                    print name
                    worksheet.write(n+1, 15, label = u'施耐德')
                    worksheet.write(n+1, 32, label = u'固安捷工业品(中国)销售有限公司')
                except:pass
                if go[2]:
                    pn_index = 0
                    for paramas in go[2]:
                        
                        pn_index +=1
                        worksheet.write(n+pn_index, 3, label = paramas.keys()[0])
                        worksheet.write(n+pn_index, 4, label = paramas.values()[0])

                    n = n + pn_index

            print('write excel')

            try:
                workbook.save(xls_name)
            except:pass
            # except:pass





    # url = 'https://www.grainger.cn/g-287896.html'
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    #
    #
    #
    #
    # xls_name = 'test.xls'
    # workbook = xlwt.Workbook(encoding = 'ascii')
    # worksheet = workbook.add_sheet('My Worksheet')
    # worksheet.write(0, 0, label = u'名称')
    # worksheet.write(0, 1, label = u'川拓型号')
    # worksheet.write(0, 2, label = u'内部参考')
    # worksheet.write(0, 3, label = u'技术参数/参数名称')
    # worksheet.write(0, 4, label = u'技术参数/参数值')
    # worksheet.write(0, 5, label = u'技术参数/单位')
    # worksheet.write(0, 6, label = u'川拓品牌')
    # worksheet.write(0, 7, label = u'供应商/价格')
    # worksheet.write(0, 8, label = u'成本')
    # worksheet.write(0, 9, label = u'销售价格')
    # worksheet.write(0, 10, label = u'计量单位')
    # worksheet.write(0, 11, label = u'产品种类')
    # worksheet.write(0, 12, label = u'供应商/供应商产品代码')
    # worksheet.write(0, 13, label = u'供应商/供应商产品名称')
    # worksheet.write(0, 14, label = u'供应商/供应商型号')
    # worksheet.write(0, 15, label = u'供应商/供应商品牌')
    # worksheet.write(0, 16, label = u'供应商/最少数量')
    # worksheet.write(0, 17, label = u'供应商/交货提前时间')
    # worksheet.write(0, 18, label = u'Skippercode Custom/客户')
    # worksheet.write(0, 19, label = u'Skippercode Custom/客户SKU')
    # worksheet.write(0, 20, label = u'Skippercode Custom/客户产品名称')
    # worksheet.write(0, 21, label = u'Skippercode Custom/客户型号')
    # worksheet.write(0, 22, label = u'Skippercode Custom/客户品牌')
    # worksheet.write(0, 23, label = u'体积')
    # worksheet.write(0, 24, label = u'重量')
    # worksheet.write(0, 25, label = u'重量计量单位')
    # worksheet.write(0, 26, label = u'标签')
    # worksheet.write(0, 27, label = u'包装方式')
    # worksheet.write(0, 28, label = u'产地')
    # worksheet.write(0, 29, label = u'面价')
    # worksheet.write(0, 30, label = u'vip价')
    # worksheet.write(0, 31, label = u'说明')
    # worksheet.write(0, 32, label = u'小尺寸图像')
    # end_data = []
    # real_n = 0
    # #  订货号
    # num_data = []
    # #  制造商型号
    # type_data = []
    # nums= soup.find('div',class_='leftTable2').find_all('tr',class_='trsku2 lefttr')
    # for num in nums:
    #     num_details = num.find_all('td')
    #
    #     end_data.append([])
    #     end_data[nums.index(num)].append(num_details[0].find('a').get_text())
    #     end_data[nums.index(num)].append(num_details[1].find('a').get_text())
    #     real_n +=1
    # print num_data
    # print type_data
    #
    # #技术参数
    # paramas_data = []
    # alls = soup.find('div',class_='rightTable1').find('tr',class_='pxTR').find_all('td')
    # for all in alls:
    #     paramas_data.append(all.get_text())
    #     print(all.get_text())
    #
    # products= soup.find('div',class_='rightTable2').find_all('tr')
    #
    # paramas = []
    # real_n = 0
    # #所有参数
    # for product in products:
    #     # print product
    #     paramas.append([])
    #     for product_detail in product.find_all('td'):
    #         index = product.find_all('td').index(product_detail)
    #         paramas[real_n].append({paramas_data[index]:product_detail.get_text()})
    #     end_data[real_n].append(paramas[real_n])
    #     real_n +=1
    #
    #
    # #销售价格
    #
    # prices =  soup.find('div',class_='fixRightTable2').find_all('tr')
    # real_n = 0
    # for price in prices:
    #     for detail in price.find_all('td'):
    #         try:
    #             end_data[real_n].append(detail.find('span',class_='sales_price').get_text()[1:])
    #             real_n+=1
    #         except:pass
    # print end_data