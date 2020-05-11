import vk


def main():
    text = input("Введите текст для нового поста: ")
    img = input("Введите наименование фото из коллекции: ")

    print(vk.post_vk(text, img))


if __name__ == "__main__":
    main()
