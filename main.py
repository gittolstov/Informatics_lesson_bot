from random import random


class Student:
    hp = 10
    title = "ученика"
    """описание объекта ученика в БД"""
    def __init__(self, name, age = 7, fav_sub = "информатика", age_by_grade1 = 6, character = "нордический", power_level = 1):
        self.name = name
        self.age = age
        self.favourite_subject = fav_sub
        self.grade = age - age_by_grade1
        self.character = character
        self.last_beaten = "никто"
        self.strength = power_level

    def beat_someone(self, other):
        dmg1 = (other.age - 7 / 11) * (other.strength / 2) * ((random() / 2) + 0.75) * 100 // 20 / 100
        dmg2 = (self.age - 7 / 11) * (self.strength / 2) * ((random() / 2) + 0.75) * 100 // 20 / 100
        self.hp -= dmg1
        other.hp -= dmg2
        print(f"{self.name} из {self.grade}-го класса побил {other.title} {other.name} из {other.grade}-го класса"
              f" и нанёс {dmg2} урона по нему.")
        other.last_beaten = self.name
        self.killcheck()
        other.killcheck()

    def killcheck(self):
        if self.hp <= 0:
            print(f"О НЕТ! {self.name} был забит насмерть!")
            self.character = "мёртвый"
            self.hp = 0.0

    def seventeen_moments_of_spring(self):
        print(f"{self.name}. Характер {self.character}. В свои {self.age} лет учится в {self.grade} классе."
              f" Любимый предмет - {self.favourite_subject}. У него осталось {self.hp} единиц здоровья."
              f" Последний раз был побит учеником {self.last_beaten}. Не женат.")

    def actuated_coal(self, amount):
        if (self.hp == 0.0):
            print(f"Ученика {self.name} уже не спасти активированным углём. Он мёртв")
            return
        self.hp += amount
        print(f"{self.name} бахнул {amount} таблеток активированного угля и излечился на {amount} здоровья")


class Teacher(Student):
    title = "учителя"


    def __init__(self, teacher_name, age, subject = "информатика", grade_they_teach = 11, character = "строгий"):
        super().__init__(teacher_name, age, subject, age - grade_they_teach, character, 100)

    def seventeen_moments_of_spring(self):
        print(f"{self.name}. Характер {self.character}. В свои {self.age} лет преподаёт в {self.grade} классе предмет "
              f"{self.favourite_subject}. У него осталось {self.hp} единиц здоровья. Не женат.")

    def psycholgical_attack(self, target):
        print(f"У ТЕБЯ ДВОЙКА, {target.name}!!!   [сила ученика {target.name} снизилась]")
        target.strength = 0.0

class Failure(Student):
    def __init__(self, name, age = 7, age_by_grade1 = 10):
        super().__init__(name, age, None, age - age_by_grade1, "вялый", 0.0)
        self.hp = 0.5

    def seventeen_moments_of_spring(self):
        print(f"{self.name}. Характер {self.character}. В свои {self.age} лет учится в {self.grade} классе. Любимого"
              f" предмета нет. У него осталось {self.hp} единиц здоровья. Не женат.")

class Eleventh_grader(Student):
    def __init__(self, name, fav_sub, power_level):
        super().__init__(name, 18, fav_sub, 7, "Уверенный", power_level)
        self.hp = 15

bully = Eleventh_grader("Быдлослав", "Физ-ра",  power_level = 5)
nerd = Failure("Игорь", 15)
насяльника = Teacher("Дмитрий Валерьевич Акимов", 35, "информатика", character = "Нордический")

bully.beat_someone(nerd)
bully.seventeen_moments_of_spring()
nerd.actuated_coal(15)
nerd.seventeen_moments_of_spring()
насяльника.psycholgical_attack(bully)
насяльника.seventeen_moments_of_spring()
bully.beat_someone(насяльника)
