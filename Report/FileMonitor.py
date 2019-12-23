# -*- coding: utf-8  -*-
# -*- author: jokker -*-

import os
import sys
import win32file
import win32con


class FileMonitor(object):

    def __init__(self):
        self.save_dir = None  # 保存文件夹，每一天生成一个文件，防止所有的文件都放在一起

    def monitor_assign_dir(self, path_to_watch, file_save_folder=None):
        """监控指定的文件，将变动信息放到指定文件夹下面"""

        ACTIONS = {
          1: "Created",
          2: "Deleted",
          3: "Updated",
          4: "Renamed from something",
          5: "Renamed to something"
        }

        FILE_LIST_DIRECTORY = 0x0001

        # path_to_watch = r'C:\Users\Administrator\Desktop\kojo'
        path_to_watch = path_to_watch
        print('Watching changes in', path_to_watch)
        hDir = win32file.CreateFile(
          path_to_watch,
          FILE_LIST_DIRECTORY,
          win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
          None,
          win32con.OPEN_EXISTING,
          win32con.FILE_FLAG_BACKUP_SEMANTICS,
          None
        )

        while 1:

            results = win32file.ReadDirectoryChangesW(
                hDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None)

            for action, filename in results:
                full_filename = os.path.join(path_to_watch, filename)

                with open(r'C:\Users\74722\Desktop\log.txt', 'a') as txt_file:
                    txt_file.write(full_filename + ACTIONS.get(action, "Unknown") + '\n')
                    print(full_filename, ACTIONS.get(action, "Unknown"))


if __name__ == '__main__':

    a = FileMonitor()
    a.monitor_assign_dir(r'C:\Users\74722\Desktop\img')
