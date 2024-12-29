class person:
    def __init__(self, name, gender, age): # 변수 초기화
        self.name = name
        self.gender = gender
        self.age = age
    
    def display(self):
        return f"이름 : {self.name}\n성별 : {self.gender}\n나이 : {self.age}" # 스트링 출력

person1 = person(input("이름을 입력하세요 : "),input("성별을 입력하세요(male/female로 입력해주세요) : "), input("나이를 입력하세요 : "))
print(person1.display())