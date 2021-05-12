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
        if winreg.EnumValue(invaxionReg,i)[0].find("Offline_PlayerThemeList")!=-1:
            global index
            index=i
            break
        i+=1
except WindowsError:
    print("No invaxion data founded! Have you played invaxion online before April 7th, 2021?\nYou can download a save file by visiting https://share4nothing.ml/Share/\n未找到音灵的游戏数据！ 是否在停服前进行过在线游戏？\n你可以通过访问https://share4nothing.ml/Share/来获取一份存档！")
    input("Press any key to contiune.../按任意键继续……")
    exit()
winreg.SetValueEx(invaxionReg,winreg.EnumValue(invaxionReg,index)[0],0,winreg.REG_BINARY,b'[{"themeId":1},{"themeId":2},{"themeId":3},{"themeId":4},{"themeId":5},{"themeId":6},{"themeId":7},{"themeId":8},{"themeId":9},{"themeId":10},{"themeId":11},{"themeId":12},{"themeId":13},{"themeId":14}]\x00')
winreg.CloseKey(invaxionReg)
print("Unlocked/解锁成功")
input("Press ENTER to contiune.../按回车键继续……")

