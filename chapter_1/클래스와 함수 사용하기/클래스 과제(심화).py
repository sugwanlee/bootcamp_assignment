class person:
    def __init__(self, age, name, gender):  # 변수 초기설정
        self.age = age
        self.name = name
        self.gender = gender
        while True:
            if self.gender == "male" or self.gender == "female": # 유효한 젠더값일 때 탈출
                break
            else:
                self.gender = input("잘못된 입력입니다. male 또는 female로 입력해주세요\n성별 : ") # 유효한 젠더값을 입력 유도
                
    
    def display(self):
        return f"나이 : {self.age}, 이름 : {self.name}\n성별 : {self.gender}" # 입력값 반환

    def greet(self): # 나이에 따른 미성년, 성년 판단
        if int(self.age) < 20 and int(self.age) > 0:
            return f"안녕하세요, {self.name}! 미성년자시군요!"
        elif int(self.age) >= 20:
            return f"안녕하세요, {self.name}! 성인이시군요!"
        else:
            return f"안녕하세요, {self.name}! ???이시군요!"

person1 = person(input("나이를 입력하세요 : "), input("이름을 입력하세요 : "), input("성별을 입력하세요(male/female로 입력해주세요) : ").lower())
print(person1.display())
print(person1.greet())
