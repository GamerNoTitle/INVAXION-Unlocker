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

    lang_folder = "assets/lang"
    lang_file = os.path.join(lang_folder, f"{lang_code}.json")
    fallback_file = os.path.join(lang_folder, "en.json")

    # 确保 lang 文件夹存在
    if not os.path.exists(lang_folder):
        os.makedirs(lang_folder)

    # 尝试加载指定语言文件
    if os.path.exists(lang_file):
        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 如果不存在，尝试加载英语文件
        if os.path.exists(fallback_file):
            with open(fallback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # 如果英语文件也不存在，返回空字典（或硬编码默认值，这里省略）
            return {}

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
        on_click=lambda e: page.launch_url("https://github.com/GamerNoTitle/INVAXION-Unlocker")
    )
    steam_button = ft.ElevatedButton(
        lang.get("steam", "Developer's Steam"),
        on_click=lambda e: page.launch_url("https://steamcommunity.com/id/bili33")
    )
    sponsor_button = ft.ElevatedButton(
        lang.get("sponsor", "Sponsor"),
        on_click=lambda e: page.launch_url("https://bili33.top/sponsors")
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
                    lang.get("copyright", "Copyright © 2025 GamerNoTitle. All rights reserved.\nINVAXION 音灵 is a registed trademark of Aquatrax.\nThe developer of this tool is not affiliated with Aquatrax."),
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