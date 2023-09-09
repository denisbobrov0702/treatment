import sys
import pathlib
import shutil


def normalize(name):
    new_string = ""

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )
    if not name.is_dir():
        extension = name.suffix.lower()
        name.removesuffix(extension)

    for i in name:
        if not i.isdigit() and "a" <= i.lower() <= "z":
            new_string += i
        elif i.lower() in CYRILLIC_SYMBOLS:
            for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
                if c == i:
                    new_string += l
                elif c.upper() == i:
                    new_string += l.upper()

        else:
            new_string += "_"
    if name.is_dir():
        return new_string
    else:
        return new_string + extension


archives = []
video = []
audio = []
documents = []
images = []
unkwown = []
set_extensions = set()
unkwown_set_extensions = set()


def recursive_dir(path):
    if path.is_dir():
        for item in path.iterdir():
            if item.name in ("archives", "video", "audio", "documents", "images"):
                continue
            new_name = normalize(item.name)
            new_path = item.with_name(
                new_name
            )  # Повертає новий об'єкт Path з новим ім'ям
            item.rename(new_path)  # Перейменовуємо папку
            recursive_dir(new_path)
    else:
        new_name = normalize(path.name)  #
        new_path = path.with_name(new_name)  # Повертає новий об'єкт Path з новим ім'ям
        path.rename(new_path)  # Перейменовуємо файл
        extension = new_path.suffix.lower()  # Знаходимо розширення файлу
        if extension in (".jpeg", ".png", ".jpg", ".svg"):
            set_extensions.add(extension)

            images.append(new_path)
        elif extension in (".avi", ".mp4", ".mov", ".mkv"):
            set_extensions.add(extension)
            video.append(new_path)
        elif extension in (".doc", ".docx", ".txt", ".pdf"):
            set_extensions.add(extension)
            documents.append(new_path)
        elif extension in (".mp3", ".ogg", ".wav", ".amr"):
            set_extensions.add(extension)
            audio.append(new_path)
        elif extension in (".zip", ".gz", ".tar"):
            set_extensions.add(extension)
            archives.append(new_path)
        else:
            unkwown_set_extensions.add(extension)
            unkwown.append(new_path)


def treatment(path):
    for i in path.iterdir():
        if i.name == "images":
            for item in images:
                shutil.move(str(item), str(i))
        elif i.name == "video":
            for item in video:
                shutil.move(str(item), str(i))
        elif i.name == "documents":
            for item in documents:
                shutil.move(str(item), str(i))
        elif i.name == "audio":
            for item in audio:
                shutil.move(str(item), str(i))
        elif i.name == "archives":
            for item in archives:
                shutil.unpack_archive(str(item), str(i))

    for i in path.iterdir():
        if i.is_dir() and not list(i.iterdir()):
            i.rmdir()


def main():
    if len(sys.argv) != 2:
        print("Must be 2 arguments")
        sys.exit()
    path = pathlib.Path(sys.argv[1])
    recursive_dir(path)
    treatment(path)


if __name__ == "__main__":
    main()
