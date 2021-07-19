# python-OCR_Translator
This Program catches text from screen and translate them(for windows only)

# 사용 방법



프로그램을 실행하면 조금있다가 창이 2개 화면에 나타납니다. 



그 중에 투명한 창을 크기를 조절해서 원하는데에 가져다 놓으면 다른 창에서 번역을 해주는 구조로 구성되있습니다.



번역해주는 부분에서 언어를 지정해줄수 있습니다.(한 , 영, 일본어, 중국어(간체) )



3가지를 지정할 수 있는데 그 종류는 읽어올 이미지 언어, 원문, 번역할 언어 입니다.

(사실 읽어올 이미지 언어하고 원문은 같은데 코드가 달라서 그냥 따로 지정했습니다. ㅎㅎ)



# 사용 예시



<번역할 부분 지정>
![1](https://user-images.githubusercontent.com/35189020/126132224-e7935c98-224c-4bc6-874c-25d3220184f5.png)

<번역 수행>
![2](https://user-images.githubusercontent.com/35189020/126132220-eb8b4f47-4359-4abb-90d7-7b815a5cddac.png)

<전체 구성>
![3](https://user-images.githubusercontent.com/35189020/126132226-9f6d9665-1f25-487d-8585-cab9eefbfd96.png)


<제작중 참고한 링크>

1) Img To Text

https://stackoverflow.com/questions/19964345/how-to-do-a-screenshot-of-a-tkinter-application


2) Thread

https://niceman.tistory.com/140?category=940952


3) Tkinter Configure

https://m.blog.naver.com/PostView.nhn?blogId=audiendo&logNo=220794534654&proxyReferer=https%3A%2F%2Fwww.google.com%2F


4) exe 파일 만들기

https://winterj.me/pyinstaller/


버그) https://stackoverflow.com/questions/32672596/pyinstaller-loads-script-multiple-times

-> PC에 OCR 프로그램이 별도로 설치되어야한다. - 독립적이지 않음
