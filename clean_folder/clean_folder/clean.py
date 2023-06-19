import os
import sys
import shutil
from pathlib import Path
# import uuid
# from normalize import normalize

extensions = {
    'video': ['.mp4', '.mov', '.avi', '.mkv'],
    'audio': ['.mp3', '.wav', '.ogg', '.amr'],
    'images': ['.jpg', '.png', '.jpeg', '.svg'],
    'archives': ['.zip', '.gz', '.tar'],
    'documents': ['.pdf', '.txt', '.doc', '.docx',
                  '.rtf', '.pptx', '.ppt', '.xlsx', '.xls']
}

map_translate_ord = {
    1072: 'a', 1073: 'b', 1074: 'v', 1075: 'h', 1076: 'd', 1077: 'e', 1105: 'e',
    1078: 'zh', 1079: 'z', 1080: 'y', 1081: 'i', 1082: 'k', 1083: 'l', 1084: 'm',
    1085: 'n', 1086: 'o', 1087: 'p', 1088: 'r', 1089: 's', 1090: 't', 1091: 'u',
    1092: 'f', 1093: 'kh', 1094: 'ts', 1095: 'ch', 1096: 'sh', 1097: 'shch', 1098: '',
    1099: 'y', 1100: '', 1101: 'e', 1102: 'iu', 1103: 'ia', 1108: 'ie', 1110: 'i',
    1111: 'i', 1169: 'g', 1040: 'A', 1041: 'B', 1042: 'V', 1043: 'H', 1044: 'D',
    1045: 'E', 1025: 'E', 1046: 'ZH', 1047: 'Z', 1048: 'Y', 1049: 'I', 1050: 'K',
    1051: 'L', 1052: 'M', 1053: 'N', 1054: 'O', 1055: 'P',  1056: 'R', 1057: 'S',
    1058: 'T', 1059: 'U', 1060: 'F', 1061: 'KH', 1062: 'TS', 1063: 'CH', 1064: 'SH',
    1065: 'SHCH', 1066: '', 1067: 'Y', 1068: '', 1069: 'E', 1070: 'IU', 1071: 'IA',
    1028: 'IE', 1030: 'I',  1031: 'I', 1168: 'G'
}
BAD_SYMBOLS = ("%", "*", " ", "-")
for i in BAD_SYMBOLS:
    map_translate_ord[ord(i)] = "_"
    # print(map_translate_ord)


def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)

                print(a, 'видалена')


def extract_file(folder_path) -> None:
    extract_dir = folder_path.joinpath('archives')
    for elem in extract_dir.glob("*.*"):
        target_dir = extract_dir.joinpath(f"{extract_dir}\{elem.stem}")
        if not target_dir.exists():
            target_dir.mkdir()
        shutil.unpack_archive(elem, target_dir)
        os.remove(elem)
        continue
    return


def get_extension(file: Path) -> str:
    ext = file.suffix.lower()
    for key, values in extensions.items():
        if ext in values:
            return key
    return "unknown"


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} dosn't exists."
    sort_folder(path)
    return "All ok"


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        target_dir.mkdir()
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    file.replace(new_name)


def normalize(file_for_translate: str) -> str:
    new_name = file_for_translate.translate(map_translate_ord)
    return new_name


def sort_folder(path: Path) -> None:
    for elem in path.glob("**/*"):
        if elem.is_dir():
            if elem.stem in extensions.keys():
                continue
        if elem.is_file():
            extension = get_extension(elem)
            move_file(elem, path, extension)
    del_empty_dirs(path)
    extract_file(path)


if __name__ == "__main__":
    main()
