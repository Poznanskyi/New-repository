from pathlib import Path
import shutil
import sys
import collections
import random
import string


papki = {
    "documents": [".doc", ".docx", ".xls", ".xlsx", ".txt", ".pdf"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"],
}


SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_")
TRANSLATE = {}
for x, y in zip(SYMBOLS, TRANSLATION):
    TRANSLATE[ord(x)] = y
    TRANSLATE[ord(x.upper())] = y.upper()


def normalize(name):
    global TRANSLATE
    return name.translate(TRANSLATE)


def unpack(archive_path, path_to_unpack):
    return shutil.unpack_archive(archive_path, path_to_unpack)


def is_file_exists(i, dr):
    if i in dr.iterdir():
        add_name = ""
        for _ in range(1):
            ch = random.choice(string.ascii_letters + string.digits)
            add_name += str(ch)

        name = i.resolve().stem + f"({add_name})" + i.suffix
        file_path = Path(dr, name)
        return file_path
    return i


def is_fold_exists(i, dr):
    if dr.exists():
        folder_sort(i, dr)
    else:
        Path(dr).mkdir()
        folder_sort(i, dr)


def folder_sort(i, dr):
    latin_name = normalize(i.name)
    new_file = Path(dr, latin_name)
    file_path = is_file_exists(new_file, dr)
    i.replace(file_path)


def sort_file(path):
    global fold
    p = Path(path)
    for _ in range(2):
        for i in p.iterdir():
            if i.name in ("documents", "audio", "video", "images", "archives", "other"):
                continue
            if i.is_file():
                flag = False
                for f, suf in papki.items():
                    if i.suffix.lower() in suf:
                        dr = Path(fold, f)
                        is_fold_exists(i, dr)
                        flag = True
                    else:
                        continue
                if not flag:
                    dr = Path(fold, "other")
                    is_fold_exists(i, dr)
            elif i.is_dir():
                if len(list(i.iterdir())) != 0:
                    sort_file(i)
                else:
                    shutil.rmtree(i)

        for j in p.iterdir():
                if j.name == "archives" and len(list(j.iterdir())) != 0:
                    for arch in j.iterdir():
                        if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                                arch_dir_name = arch.resolve().stem
                                path_to_unpack = Path(fold, "archives", arch_dir_name)
                                shutil.unpack_archive(arch, path_to_unpack)
                            else:
                                continue


def main(path):
    sort_file(path)
    p = Path(path)

    total_dict = collections.defaultdict(list)
    for item in p.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    total_dict[item.name].append(file.suffix)


    print("| {:^15} | {:^17} | {:^43} |".format("Назва папки ", "кількість файлів", "розширення файлів")

    for key, value in total_dict.items():
        k, a, b = key, len(value), ", ".join(set(value))
        print("| {:<15} | {:^17} | {:<43} |".format(k, a, b))


if __name__ == "__main__":
    path = sys.argv[1]
    fold = Path(path)
    main(path)