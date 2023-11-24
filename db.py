def write_to_bd(list):
    file = open("database.txt", "a", encoding="UTF-8")
    for i in list:
        file.write(i + "\t")
    file.write("\n")