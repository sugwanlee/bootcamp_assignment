import random

print("1과 10 사이의 숫자를 하나 정했습니다.\n이 숫자는 무엇일까요?") # 게임 멘트 출력
random_number = random.randint(1,10) # 1~10까지 난수 지정
while True: # break 이전까지 계속 반복
    user_input = int(input()) # 반복 될때마다 다시 user_input 입력
    print("예상 숫자:",user_input)# 반복 될때마다 '예상 숫자:' 앞에 붙여주기
    if user_input > random_number:
        print("너무 큽니다. 다시 입력하세요")
    elif user_input < random_number:
        print("너무 작습니다. 다시 입력하세요")
    elif user_input == random_number: # 정답을 맞추면 while 문 탈출
        print("정답입니다!\n")
        break
