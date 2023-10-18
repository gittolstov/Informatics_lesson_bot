from random import random


class Student:
    hp = 10
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
        print(f"{self.name} из {self.grade}-го класса побил ученика {other.name} из {other.grade}-го класса и нанёс {dmg2} урона по нему.")
        other.last_beaten = self.name
        self.killcheck()
        other.killcheck()

    def killcheck(self):
        if self.hp <= 0:
            print(f"О НЕТ! {self.name} был забит насмерть!")
            self.character = "мёртвый"
            self.hp = 0.0

    def seventeen_moments_of_spring(self):
        print(f"{self.name}. Характер {self.character}. В свои {self.age} лет учится в {self.grade} классе. Любимый предмет - {self.favourite_subject}. У него осталось {self.hp} единиц здоровья. Последний раз был побит учеником {self.last_beaten}. Не женат.")

    def actuated_coal(self, amount):
        if (self.hp == 0.0):
            print(f"Ученика {self.name} уже не спасти активированным углём. Он мёртв")
            return
        self.hp += amount
        print(f"{self.name} бахнул {amount} таблеток активированного угля и излечился на {amount} здоровья")


bully = Student("Быдлослав", 18, "Физ-ра", 11,  power_level = 5)
nerd = Student("Игорь", 15, character = "тихий")
насяльника = Student("Дмитрий Валерьевич Акимов", 35, character = "Нордиченский", power_level = 100)

bully.beat_someone(nerd)
bully.seventeen_moments_of_spring()
nerd.actuated_coal(15)
nerd.seventeen_moments_of_spring()
насяльника.beat_someone(nerd)
насяльника.beat_someone(bully)
насяльника.seventeen_moments_of_spring()
