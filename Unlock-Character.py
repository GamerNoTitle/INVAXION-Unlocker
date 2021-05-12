import winreg
try:
    invaxionReg=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"SOFTWARE\Aquatrax\INVAXION",0,winreg.KEY_ALL_ACCESS)
except FileNotFoundError:
    print("No invaxion data founded! Does invaxion be installed on this computer?\n未找到音灵的游戏数据！ 此电脑上安装了音灵吗？")
    input("Press any key to contiune.../按任意键继续……")
    exit()
try:
    i=0
    while True:
        if winreg.EnumValue(invaxionReg,i)[0].find("Offline_PlayerCharList")!=-1:
            global index
            index=i
            break
        i+=1
except WindowsError:
    print("No invaxion data founded! Have you played invaxion online before April 7th, 2021?\nYou can download a save file by visiting https://share4nothing.ml/Share/\n未找到音灵的游戏数据！ 是否在停服前进行过在线游戏？\n你可以通过访问https://share4nothing.ml/Share/来获取一份存档！")
    input("Press any key to contiune.../按任意键继续……")
    exit()
winreg.SetValueEx(invaxionReg,winreg.EnumValue(invaxionReg,index)[0],0,winreg.REG_BINARY,b'[{"charId":10010,"level":1,"exp":0,"playCount":0},{"charId":10020,"level":1,"exp":0,"playCount":0},{"charId":10030,"level":1,"exp":0,"playCount":0},{"charId":10040,"level":1,"exp":0,"playCount":0},{"charId":10050,"level":1,"exp":0,"playCount":0},{"charId":10060,"level":1,"exp":0,"playCount":0},{"charId":20010,"level":1,"exp":0,"playCount":0},{"charId":20020,"level":1,"exp":0,"playCount":0},{"charId":20030,"level":1,"exp":0,"playCount":0},{"charId":20040,"level":1,"exp":0,"playCount":0},{"charId":20050,"level":1,"exp":0,"playCount":0},{"charId":20060,"level":1,"exp":0,"playCount":0},{"charId":20070,"level":1,"exp":0,"playCount":0},{"charId":20080,"level":1,"exp":0,"playCount":0},{"charId":20090,"level":1,"exp":0,"playCount":0},{"charId":20100,"level":1,"exp":0,"playCount":0},{"charId":20110,"level":1,"exp":0,"playCount":0},{"charId":20120,"level":1,"exp":0,"playCount":0},{"charId":20130,"level":1,"exp":0,"playCount":0},{"charId":20140,"level":1,"exp":0,"playCount":0},{"charId":20150,"level":1,"exp":0,"playCount":0},{"charId":20160,"level":1,"exp":0,"playCount":0},{"charId":20170,"level":1,"exp":0,"playCount":0},{"charId":30010,"level":1,"exp":0,"playCount":0},{"charId":30020,"level":1,"exp":0,"playCount":0},{"charId":30030,"level":1,"exp":0,"playCount":0},{"charId":30040,"level":1,"exp":0,"playCount":0},{"charId":30050,"level":1,"exp":0,"playCount":0},{"charId":30060,"level":1,"exp":0,"playCount":0},{"charId":30070,"level":1,"exp":0,"playCount":0},{"charId":30080,"level":1,"exp":0,"playCount":0},{"charId":30090,"level":1,"exp":0,"playCount":0},{"charId":30100,"level":1,"exp":0,"playCount":0},{"charId":30110,"level":1,"exp":0,"playCount":0},{"charId":40010,"level":1,"exp":0,"playCount":0},{"charId":40020,"level":1,"exp":0,"playCount":0},{"charId":40030,"level":1,"exp":0,"playCount":0},{"charId":40040,"level":1,"exp":0,"playCount":0},{"charId":40050,"level":1,"exp":0,"playCount":0},{"charId":40060,"level":1,"exp":0,"playCount":0},{"charId":40070,"level":1,"exp":0,"playCount":0},{"charId":40080,"level":1,"exp":0,"playCount":0},{"charId":40090,"level":1,"exp":0,"playCount":0},{"charId":40100,"level":1,"exp":0,"playCount":0},{"charId":40110,"level":1,"exp":0,"playCount":0},{"charId":40120,"level":1,"exp":0,"playCount":0},{"charId":40130,"level":1,"exp":0,"playCount":0},{"charId":40140,"level":1,"exp":0,"playCount":0},{"charId":40150,"level":1,"exp":0,"playCount":0},{"charId":40160,"level":1,"exp":0,"playCount":0},{"charId":40170,"level":1,"exp":0,"playCount":0},{"charId":40180,"level":1,"exp":0,"playCount":0},{"charId":40190,"level":1,"exp":0,"playCount":0},{"charId":40200,"level":1,"exp":0,"playCount":0},{"charId":40210,"level":1,"exp":0,"playCount":0},{"charId":40220,"level":1,"exp":0,"playCount":0},{"charId":40230,"level":1,"exp":0,"playCount":0},{"charId":40240,"level":1,"exp":0,"playCount":0},{"charId":40250,"level":1,"exp":0,"playCount":0},{"charId":40260,"level":1,"exp":0,"playCount":0},{"charId":40270,"level":1,"exp":0,"playCount":0},{"charId":40280,"level":1,"exp":0,"playCount":0},{"charId":40290,"level":1,"exp":0,"playCount":0},{"charId":40300,"level":1,"exp":0,"playCount":0},{"charId":40310,"level":1,"exp":0,"playCount":0},{"charId":40320,"level":1,"exp":0,"playCount":0},{"charId":40330,"level":1,"exp":0,"playCount":0},{"charId":50010,"level":1,"exp":0,"playCount":0}]\x00')
winreg.CloseKey(invaxionReg)
print("Unlocked/解锁成功")
input("Press ENTER to contiune.../按回车键继续……")
