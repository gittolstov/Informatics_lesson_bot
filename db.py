def write_to_bd(list):
    with appender() as file:
        file.write("\t".join(list))
        file.write("\n")


def find_by_id(id):
    with reader() as file:
        for line in file:
            a = line.split("\t")
            if int(a[0]) == id:
                return a


def redact_by_id(id, list):
    with redacter() as file:
        text = []
        for line in file:
            a = line.split("\t")
            if int(a[0]) == id:
                text.append("\t".join(list)+"\n")
            else:
                text.append(line)
        file.write("".join(text))


def isInDbById(id):
    with reader() as file:
        for line in file:
            a = line.split("\t")
            if int(a[0]) == id:
                return True
    return False

def appender():
    return open("database.txt", "a", encoding="UTF-8")

def reader():
    return open("database.txt", "r", encoding="UTF-8")

def redacter():
    return open("database.txt", "r", encoding="UTF-8")