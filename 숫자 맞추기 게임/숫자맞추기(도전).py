import random

print("1과 10 사이의 숫자를 하나 정했습니다.\n이 숫자는 무엇일까요?")    # 초기 게임문제 출력
random_number = random.randint(1,10) # 초기 난수 random_number객체에 저장
while True:    # break로 탈출하기 전에는 계속 반복
    user_input = int(input())   # 입력값을 while문이 돌아갈 때마다 user_input객체에 저장하는 용도
    print("예상 숫자:",user_input)    # 위 용도와 같이 항상 출력되는 메시지
    if user_input > 10 or user_input <= 0:    # user_input값이 난수 범위 외에 값이 입력됐을 때 if문 실행 
        print("1과 10 사이에 숫자를 입력해주세요\n")    
    elif user_input > random_number:    # user_input값이 난수보다 클 때 elif문 실행(힌트) 
        print("너무 큽니다. 다시 입력하세요\n")
    elif user_input < random_number:    # user_input값이 난수보다 작을 때 elif문 실행(힌트) 
        print("너무 작습니다. 다시 입력하세요\n")
    elif user_input == random_number:   #정답을 맞췄을 때 elif문 실행
        print("정답입니다!\n")
        print("한 번 더 하시려면 아무 키를 눌러주시고")
        if "n" == input("그만하시려면 n을 눌러주세요\n").lower():   # input 값이 n이면 반복문에서 탈출
            break
        else:
            random_number = random.randint(1,11)  # 그 외의 키를 입력하면 반복문 다시시작
            print("1과 10 사이의 숫자를 하나 정했습니다.\n이 숫자는 무엇일까요?")