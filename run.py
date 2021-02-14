#!/usr/bin/python3
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import config
from PIL import Image
import os
import random
import string
import ctypes
from ctypes import *
import sys
dll=0

def wait_for_element_txt(driver,element_txt):
    t=int(time.time())
    print('Waiting for loading.', end='', flush=True)
    while driver.find_elements_by_link_text(element_txt) == []:
        if(int(time.time())-t>60):
            raise Exception("time limit!", level)
        print('.', end='', flush=True)
        time.sleep(0.2)
    print()

def wait_for_element_class(driver,element_class_name):
    t=int(time.time())
    print('Waiting for loading.', end='', flush=True)
    while driver.find_elements_by_class_name(element_class_name) == []:
        if(int(time.time())-t>60):
            raise Exception("time limit!", level)
        print('.', end='', flush=True)
        time.sleep(0.2)
    print()

def getcode(path):
        Str = create_string_buffer(20)
        if(dll.GetImageFromFile(path, Str)):
            print('GetVcode Success:', Str.raw.decode("gbk"))
            return str(Str.raw.decode("gbk")).replace("\x00","")
        else:
            print('GetVcode Fail!')
            return("0000")

def getimg(driver,n=0):  
    driver.save_screenshot('.\photo.png')  # 一次截图：形成全图
    baidu = driver.find_element_by_id('codeImage')
    left = baidu.location['x']  # 区块截图左上角在网页中的x坐标
    top = baidu.location['y']  # 区块截图左上角在网页中的y坐标
    right = left + baidu.size['width']  # 区块截图右下角在网页中的x坐标
    bottom = top + baidu.size['height']  # 区块截图右下角在网页中的y坐标
    picture = Image.open('.\photo.png')
    print((left, top, right, bottom))
    picture = picture.crop((left, top, right, bottom))  # 二次截图：形成区块截图
    if len(picture.split()) == 4:
        # prevent IOError: cannot write mode RGBA as BMP
        r, g, b, a = picture.split()
        picture = Image.merge("RGB", (r, g, b))
        picture.convert('RGB').save(sys.path[0]+"\\"+"photo"+str(n)+".jpg", quality=70)
        res= getcode(sys.path[0]+"\\"+"photo"+str(n)+".jpg")
        print(sys.path[0]+"\\"+"photo"+str(n)+".jpg")
        # picture.convert('RGB').save(".\\"+res+".jpg", quality=70)
        os.remove(sys.path[0]+"\\"+"photo"+str(n)+".jpg")
        return res
    else:
        picture.convert('RGB').save(sys.path[0]+"\\"+"photo"+str(n)+".jpg", quality=70)

def inrow(a,b):
    u=0
    for i in a:
        while(not(i==str((b//(10**(4-1-u)))%(10)))):
            # print(i,(b//(10**(4-1-u)))%(10))
            u=u+1
            if(u>4):
                break
        # print(i,b,u)
        u=u+1
        if(u>4):
            break
    else:
        return True
    return False

def addzero(a):
    if a<10:
        return "000"+str(a)
    elif a<100:
        return "00"+str(a)
    elif a<1000:
        return "0"+str(a)
    elif a<10000:
        return str(a)
    return "0000"

def getrendomtem():
    return(str(random.randint(357,365)/10))

def submit(username,password):
    day=time.strftime("%Y-%m-%d", time.localtime()) 
    if(not(os.path.exists(sys.path[0]+'\\'+username+'\\'+day))):
        os.makedirs(sys.path[0]+'\\'+username+'\\'+day)
    options = Options()
    options.add_argument("--headless")
    # options.add_argument("disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get("https://yqtb.hust.edu.cn/infoplus/form/BKS/start")
    assert "统一身份认证系统" in driver.title

    elem = driver.find_element_by_id('un')
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element_by_id('pd')
    elem.clear()
    elem.send_keys(password)

    # time.sleep(5)
    # codeImage
    codevi=True
    while(codevi):
        codes=[]
        for p in range(10):
            codes.append(getimg(driver,p))
            time.sleep(0.3)
        print(codes)
        for i in range(0,10001):
            for b in codes:
                u=0
                if(not(inrow(b,i))):
                    break
            else:
                # print(i)
                break
        if(i<10000):
            codevi=False
            vcode=addzero(i)
        else:
            driver.find_element_by_id('codeImage').click()
    print(vcode)
    print(sys.path[0]+'\\'+username+'\\'+day+'\\2.png')
    elem = driver.find_element_by_id('code')
    elem.clear()
    elem.send_keys(vcode)
    time.sleep(1)
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\1.png')
    driver.find_element_by_id('index_login_btn').click()
    time.sleep(5)
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\2.png')
    if(driver.find_elements_by_id("errormsg")!=[] and driver.find_element_by_id("errormsg").text!=""):
        print("发生错误：密码错误或验证码错误")
        return(1)
    wait_for_element_txt(driver,'下一步')
    print('Login succeeded.')
    driver.find_element_by_id('V1_CTRL264').click()
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\3.png')
    assert driver.find_element_by_id('V1_CTRL264').is_selected() # Submit for myself
    driver.find_element_by_link_text('下一步').click()

    time.sleep(1)
    wait_for_element_txt(driver,'下一步 Next step')
    print('join succeeded.')
    assert driver.find_element_by_id('V1_CTRL154').is_selected() # Submit for myself
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\4.png')
    driver.find_element_by_link_text('下一步 Next step').click()

    wait_for_element_txt(driver,'提交 Submit')
    # I will leave all info as-is.
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\5.png')
    driver.find_element_by_id('V1_CTRL164').send_keys(getrendomtem())
    driver.find_element_by_id('V1_CTRL104').click()
    driver.find_element_by_id('V1_CTRL74').click()

    try:
        # driver.find_element_by_id('V1_CTRL172_0').clear()
        driver.find_element_by_id('V1_CTRL174_0').send_keys(getrendomtem())
        driver.find_element_by_id('V1_CTRL184_0').click()
        driver.find_element_by_id('V1_CTRL186_0').click()
        # driver.find_element_by_id('V1_CTRL172_1').clear()
        driver.find_element_by_id('V1_CTRL174_1').send_keys(getrendomtem())
        driver.find_element_by_id('V1_CTRL184_1').click()
        driver.find_element_by_id('V1_CTRL186_1').click()
        driver.find_element_by_id('V1_CTRL174_2').send_keys(getrendomtem())
        driver.find_element_by_id('V1_CTRL184_2').click()
        driver.find_element_by_id('V1_CTRL186_2').click()
        driver.find_element_by_id('V1_CTRL174_3').send_keys(getrendomtem())
        driver.find_element_by_id('V1_CTRL184_3').click()
        driver.find_element_by_id('V1_CTRL186_3').click()
    except:
        pass
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\6.png')
    driver.find_element_by_link_text('提交 Submit').click() # Fucking dynamic id
    time.sleep(0.5)
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\7.png')
    wait_for_element_class(driver,'dialog_button')
    driver.find_element_by_class_name('dialog_button').click() # first one is 'Ok', second one is 'Cancel'.
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\8.png')
    wait_for_element_class(driver,'dialog_content')

    #while 'If you have anything to comment' in driver.find_element_by_class_name('dialog_content').text:
    #    wait_for_element_class(driver,'dialog_content')
    #while '' == driver.find_element_by_class_name('dialog_content').text:
    #    wait_for_element_class(driver,'dialog_content')
    time.sleep(5) # magic bug, I give it up, and simply sleeps 2 second. Fix the4 code lines above if you could.
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\9.png')
    result = driver.find_element_by_class_name('dialog_content').text
    print(result)
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\10.png')
    driver.find_element_by_class_name('dialog_button').click() # Unnecessary.
    time.sleep(5)
    driver.save_screenshot(sys.path[0]+'\\'+username+'\\'+day+'\\11.png')
    driver.close()
    return(0 if result == '办理成功!' else 2)

dll = ctypes.windll.LoadLibrary('.\WmCode.dll')
if(dll.UseUnicodeString(1, 1)):
    print('SetInUnicode Success:')
else:
    print('etInUnicode Fail!')
print(sys.path[0]+"\\"+'hust.dat')
if(dll.LoadWmFromFile(sys.path[0]+"\\"+'hust.dat', '123')): 
    print('Loaddat Success:')
    dll.SetWmOption(6,95)
else:
    print("loaddat error")

for i in config.users:
    try:
        res=submit(i[0],i[1])
        file_handle=open(sys.path[0]+"\\"+'res.txt',mode='a+', encoding = 'utf-8')
        resmap=["成功","密码错误或验证码错误","打卡失败"]
        print(i[0]+"  "+resmap[res])
        print(i[0]+"  "+resmap[res],file=file_handle)
        file_handle.close()
    except BaseException:
        file_handle=open(sys.path[0]+"\\"+'res.txt',mode='a+', encoding = 'utf-8')
        print(i[0]+"  未知错误")
        print(i[0]+"  未知错误",file=file_handle)
        file_handle.close()
