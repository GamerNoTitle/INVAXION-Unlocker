import flet as ft
import os
import json
from typing import List, Dict
import re
import winreg
import locale


def load_language(lang_code: str = None) -> Dict:
    """
    加载语言文件，如果指定语言不存在则回退到英语。
    """
    if lang_code is None:
        lang_code = (
            locale.getdefaultlocale()[0].replace("_", "-")
            if locale.getdefaultlocale()[0]
            else "en"
        )
    en_lang = {
        "app_title": "INVAXION Patch Tool - GamerNoTitle",
        "copyright": "Copyright © 2025 GamerNoTitle. All rights reserved.\nINVAXION 音灵 is a registed trademark of Aquatrax.\nThe developer of this tool is not affiliated with Aquatrax.",
        "github": "Github",
        "select_directory": "Select Directory",
        "patch_all": "Patch All",
        "patch_char": "Patch Character",
        "patch_song": "Patch Song",
        "patch_theme": "Patch Theme",
        "no_directory_selected": "No Directory Selected",
        "read_success_title": "Successfully Read",
        "read_success_content": "Successfully found Song, Character, and theme data",
        "error_title": "Error",
        "error_invaxion_exe": "INVAXION.exe not found. Please ensure you have selected the game directory or that the game is installed correctly.",
        "error_invaxion_data": "INVAXION_DATA folder not found. Please ensure you have selected the game directory or that the game is installed correctly.",
        "error_streaming_assets": "StreamingAssets folder not found. Please ensure you have selected the game directory or that the game is installed correctly.",
        "warning_title": "Warning",
        "warning_empty_data": "Data for {key_name} is empty: {data_str}",
        "warning_empty_bytes": "Encoded data is empty, cannot write to {key_name}",
        "warning_partial_failure": "Partial Patch failed, please check error messages!",
        "steam": "Developer's Steam",
        "success_title": "Completed",
        "success_patch_all": "Successfully Patched Character, Song, and Starship",
        "success_patch_char": "Successfully Patched Character",
        "success_patch_song": "Successfully Patched Song",
        "success_patch_theme": "Successfully Patched Starship",
        "registry_error": "Registry write error ({key_name}): {error_msg}",
    }
    zh_cn_lang = {
        "app_title": "INVAXION 音灵全解锁补丁 - GamerNoTitle",
        "copyright": "Copyright © 2025 GamerNoTitle, 保留所有权利。\nNVAXION 音灵是 Aquatrax 的注册商标。\n本工具的开发者与 Aquatrax 无关。",
        "github": "Github",
        "select_directory": "选择游戏目录",
        "patch_all": "我全都要！",
        "patch_char": "应用补丁到角色",
        "patch_song": "应用补丁到铺面",
        "patch_theme": "应用补丁到星舰",
        "no_directory_selected": "未选择目录",
        "read_success_title": "读取成功",
        "read_success_content": "成功找到铺面、角色和星舰数据",
        "error_title": "错误",
        "error_invaxion_exe": "未找到 INVAXION.exe，请确认你选择的是游戏所在的目录或者游戏安装完整。",
        "error_invaxion_data": "未找到 INVAXION_DATA 文件夹，请确认你选择的是游戏所在的目录或者游戏安装完整。",
        "error_streaming_assets": "未找到 StreamingAssets 文件夹，请确认你选择的是游戏所在的目录或者游戏安装完整。",
        "warning_title": "警告",
        "warning_empty_data": "写入 {key_name} 的数据为空: {data_str}",
        "warning_empty_bytes": "编码后的数据为空，无法写入 {key_name}",
        "warning_partial_failure": "部分数据应用补丁失败，请检查错误信息！",
        "steam": "我的 Steam",
        "success_title": "完成",
        "success_patch_all": "成功应用补丁到角色、铺面和星舰",
        "success_patch_char": "成功应用补丁到角色",
        "success_patch_song": "成功应用补丁到铺面",
        "success_patch_theme": "成功应用补丁到星舰",
        "registry_error": "注册表写入错误 ({key_name}): {error_msg}",
    }
    zh_tw_lang = {
        "app_title": "INVAXION 音靈全解鎖補丁 - GamerNoTitle",
        "copyright": "Copyright © 2025 GamerNoTitle，保留所有權利。\nINVAXION 音靈是 Aquatrax 的註冊商標。\n本工具的開發者與 Aquatrax 無關。",
        "github": "Github",
        "select_directory": "選擇遊戲目錄",
        "patch_all": "我全都要！",
        "patch_char": "應用補丁到角色",
        "patch_song": "應用補丁到譜面",
        "patch_theme": "應用補丁到星艦",
        "no_directory_selected": "未選擇目錄",
        "read_success_title": "讀取成功",
        "read_success_content": "成功找到譜面、角色和星艦資料",
        "error_title": "錯誤",
        "error_invaxion_exe": "未找到 INVAXION.exe，請確認您選擇的是遊戲所在的目錄或遊戲安裝完整。",
        "error_invaxion_data": "未找到 INVAXION_DATA 資料夾，請確認您選擇的是遊戲所在的目錄或遊戲安裝完整。",
        "error_streaming_assets": "未找到 StreamingAssets 資料夾，請確認您選擇的是遊戲所在的目錄或遊戲安裝完整。",
        "warning_title": "警告",
        "warning_empty_data": "寫入 {key_name} 的資料為空: {data_str}",
        "warning_empty_bytes": "編碼後的資料為空，無法寫入 {key_name}",
        "warning_partial_failure": "部分資料應用補丁失敗，請檢查錯誤訊息！",
        "steam": "我的 Steam",
        "success_title": "完成",
        "success_patch_all": "成功應用補丁到角色、譜面和星艦",
        "success_patch_char": "成功應用補丁到角色",
        "success_patch_song": "成功應用補丁到譜面",
        "success_patch_theme": "成功應用補丁到星艦",
        "registry_error": "登錄檔寫入錯誤 ({key_name}): {error_msg}",
    }
    
    if lang_code.startswith("zh-CN"):
        return zh_cn_lang
    elif lang_code.startswith("zh-TW"):
        return zh_tw_lang
    else:
        return en_lang


def main(page: ft.Page):
    # 动态设置窗口大小
    page.window.width = 600  # 设置窗口宽度
    page.window.height = 400  # 设置窗口高度
    page.window.resizable = False  # 允许用户调整窗口大小

    # 加载语言文件
    lang = load_language()

    page.title = lang.get("app_title", "INVAXION Patch Tool - GamerNoTitle")
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI 组件
    selected_path = ft.Text(
        value=lang.get("no_directory_selected", "No Directory Selected"), size=16
    )
    select_button = ft.ElevatedButton(
        lang.get("select_directory", "Select Directory"),
        on_click=lambda e: pick_directory(),
    )
    patch_all_button = ft.ElevatedButton(
        lang.get("patch_all", "Patch All"),
        on_click=lambda e: patch_all(),
        disabled=True,
    )
    patch_char_button = ft.ElevatedButton(
        lang.get("patch_char", "Patch Character"),
        on_click=lambda e: patch_single("char"),
        disabled=True,
    )
    patch_song_button = ft.ElevatedButton(
        lang.get("patch_song", "Patch Song"),
        on_click=lambda e: patch_single("song"),
        disabled=True,
    )
    patch_theme_button = ft.ElevatedButton(
        lang.get("patch_theme", "Patch Starship"),
        on_click=lambda e: patch_single("theme"),
        disabled=True,
    )

    github_button = ft.ElevatedButton(
        lang.get("github", "GitHub"),
        on_click=lambda e: page.launch_url(
            "https://github.com/GamerNoTitle/INVAXION-Unlocker"
        ),
    )
    steam_button = ft.ElevatedButton(
        lang.get("steam", "Developer's Steam"),
        on_click=lambda e: page.launch_url("https://steamcommunity.com/id/bili33"),
    )
    sponsor_button = ft.ElevatedButton(
        lang.get("sponsor", "Sponsor"),
        on_click=lambda e: page.launch_url("https://bili33.top/sponsors"),
    )

    # 全局变量存储数据
    global char_data, song_data, theme_data
    char_data = []
    song_data = []
    theme_data = []

    # 弹窗队列及其状态标志位
    dialog_queue = []
    dialog_in_use = [False] * 5  # 5个弹窗的使用状态，False 表示未使用
    for i in range(5):
        dialog = ft.AlertDialog(
            title=ft.Text(""),
            content=ft.Text("", size=14),
            actions=[ft.TextButton("确认", on_click=lambda e, d=i: close_dialog(d))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        dialog_queue.append(dialog)
        page.overlay.append(dialog)

    def show_alert(title: str, content: str):
        # 查找可用的弹窗
        available_dialog_index = -1
        for i in range(len(dialog_in_use)):
            if not dialog_in_use[i]:
                available_dialog_index = i
                break

        if available_dialog_index == -1:
            # 如果没有可用的弹窗，清空所有弹窗状态并重用第一个
            for i in range(len(dialog_in_use)):
                dialog_in_use[i] = False
                dialog_queue[i].open = False
            available_dialog_index = 0
            page.update()

        # 设置弹窗内容
        dialog = dialog_queue[available_dialog_index]
        dialog.title = ft.Text(title)
        dialog.content = ft.Text(content, size=14)
        dialog_in_use[available_dialog_index] = True
        dialog.open = True
        page.update()

    def close_dialog(dialog_index: int):
        dialog_in_use[dialog_index] = False
        dialog_queue[dialog_index].open = False
        page.update()

    def pick_directory():
        dialog = ft.FilePicker(on_result=lambda e: handle_directory_selection(e))
        page.overlay.append(dialog)
        page.update()
        dialog.get_directory_path()  # 使用 get_directory_path 选择目录

    def handle_directory_selection(e: ft.FilePickerResultEvent):
        if e.path:
            selected_path.value = (
                f"{lang.get('select_directory', 'Selected Directory')}: {e.path}"
            )
            if check_directory(e.path):
                # 启用 Patch 按钮
                patch_all_button.disabled = False
                patch_char_button.disabled = False
                patch_song_button.disabled = False
                patch_theme_button.disabled = False
            else:
                patch_all_button.disabled = True
                patch_char_button.disabled = True
                patch_song_button.disabled = True
                patch_theme_button.disabled = True
        page.update()

    def check_directory(path: str):
        global char_data, song_data, theme_data
        # 检查必要文件和目录
        invaxion_exe = os.path.join(path, "INVAXION.exe")
        invaxion_data = os.path.join(path, "INVAXION_DATA")

        if not os.path.exists(invaxion_exe):
            show_alert(
                lang.get("error_title", "Error"),
                lang.get("error_invaxion_exe", "INVAXION.exe not found"),
            )
            return False

        if not os.path.exists(invaxion_data):
            show_alert(
                lang.get("error_title", "Error"),
                lang.get("error_invaxion_data", "INVAXION_DATA folder not found"),
            )
            return False

        streaming_assets = os.path.join(invaxion_data, "StreamingAssets")
        if not os.path.exists(streaming_assets):
            show_alert(
                lang.get("error_title", "Error"),
                lang.get("error_streaming_assets", "StreamingAssets folder not found"),
            )
            return False

        # 处理文件列表
        themes = set()
        characters = set()
        songs = set()

        # 铺面匹配的正则表达式
        song_pattern = re.compile(r"^(\d+)_(4k|6k|8k)_(standard|trinity|hard)_pc$")

        for root, _, files in os.walk(streaming_assets):
            for file in files:
                filename = os.path.splitext(file)[0]

                if filename.startswith("theme_"):
                    try:
                        theme_id = int(filename.split("_")[1])
                        themes.add(theme_id)
                    except (IndexError, ValueError):
                        pass

                elif filename.startswith("character_"):
                    try:
                        char_id = int(filename.split("_")[1])
                        characters.add(char_id)
                    except (IndexError, ValueError):
                        pass

                else:
                    match = song_pattern.match(filename)
                    if match:
                        song_id = int(match.group(1))
                        songs.add(song_id)

        # 构建结果列表
        char_data = [
            {"charId": char_id, "level": 30, "exp": 0, "playCount": 0}
            for char_id in sorted(characters)
        ]
        theme_data = [{"themeId": theme_id} for theme_id in sorted(themes)]
        song_data = [{"songId": song_id} for song_id in sorted(songs)]

        # 显示结果在弹窗中，标题为"读取成功"，内容为成功信息
        show_alert(
            lang.get("read_success_title", "Read Successful"),
            lang.get(
                "read_success_content",
                "Successfully found Song, Character, and Starship data",
            ),
        )
        return True

    def write_to_registry(key_name: str, data: List[Dict]):
        try:
            # 调试：确认数据内容
            data_str = json.dumps(data, separators=(",", ":"))
            if not data:  # 如果数据为空
                show_alert(
                    lang.get("warning_title", "Warning"),
                    lang.get(
                        "warning_empty_data", "Data for {key_name} is empty: {data_str}"
                    ).format(key_name=key_name, data_str=data_str),
                )
                return False

            # 转换为字节数据（二进制）
            data_bytes = data_str.encode("utf-8")
            if not data_bytes:  # 如果编码后为空
                show_alert(
                    lang.get("warning_title", "Warning"),
                    lang.get(
                        "warning_empty_bytes",
                        "Encoded data is empty, cannot write to {key_name}",
                    ).format(key_name=key_name),
                )
                return False

            # 打开或创建注册表路径
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Aquatrax\INVAXION"
            )
            # 写入注册表，类型为 REG_BINARY
            winreg.SetValueEx(key, key_name, 0, winreg.REG_BINARY, data_bytes)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            show_alert(
                lang.get("error_title", "Error"),
                lang.get(
                    "registry_error", "Registry write error ({key_name}): {error_msg}"
                ).format(key_name=key_name, error_msg=str(e)),
            )
            return False

    def patch_single(data_type: str):
        success = False
        if data_type == "char":
            success = write_to_registry("Offline_PlayerCharList_h2836715314", char_data)
            if success:
                show_alert(
                    lang.get("success_title", "Completed"),
                    lang.get("success_patch_char", "Successfully Patched Character"),
                )
        elif data_type == "song":
            success = write_to_registry("Offline_PlayerSongList_h655833887", song_data)
            if success:
                show_alert(
                    lang.get("success_title", "Completed"),
                    lang.get("success_patch_song", "Successfully Patched Song"),
                )
        elif data_type == "theme":
            success = write_to_registry(
                "Offline_PlayerThemeList_h553588539", theme_data
            )
            if success:
                show_alert(
                    lang.get("success_title", "Completed"),
                    lang.get("success_patch_theme", "Successfully Patched Starship"),
                )

    def patch_all():
        char_success = write_to_registry(
            "Offline_PlayerCharList_h2836715314", char_data
        )
        song_success = write_to_registry("Offline_PlayerSongList_h655833887", song_data)
        theme_success = write_to_registry(
            "Offline_PlayerThemeList_h553588539", theme_data
        )

        if char_success and song_success and theme_success:
            show_alert(
                lang.get("success_title", "Completed"),
                lang.get(
                    "success_patch_all",
                    "Successfully Patched Character, Song, and Starship",
                ),
            )
        else:
            show_alert(
                lang.get("warning_title", "Warning"),
                lang.get(
                    "warning_partial_failure",
                    "Partial Patch failed, please check error messages!",
                ),
            )

    # 布局
    page.add(
        ft.Column(
            [
                selected_path,
                select_button,
                ft.Row(
                    [
                        patch_all_button,
                        patch_char_button,
                        patch_song_button,
                        patch_theme_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Row(
                    [
                        github_button,
                        steam_button,
                        sponsor_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Divider(),
                ft.Text(
                    lang.get(
                        "copyright",
                        "Copyright © 2025 GamerNoTitle. All rights reserved.\nINVAXION 音灵 is a registed trademark of Aquatrax.\nThe developer of this tool is not affiliated with Aquatrax.",
                    ),
                    size=14,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,  # 减少组件间距以适应小窗口
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
