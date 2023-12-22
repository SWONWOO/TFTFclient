# TFTFclient
네트워크 프로그래밍 

# MyTFTP Client
MyTFTP Client는 Python과 소켓 API를 사용하여 구현된 간단한 TFTP 클라이언트이다.

## 프로그램 설명
이 클라이언트는 TFTP 프로토콜을 이용하여 파일을 다운로드하거나 업로드할 수 있다. 서버와의 통신은 UDP를 사용하며, 포트 69번이 기본으로 설정되어있다.

## 사용법
프로그램을 실행할 때는 다음과 같은 형식을 따르며, 필요한 경우 포트 번호를 지정할 수 있다. (맥북 터미널 기준)

python mytftp_client.py <host_address> [-p <port_number>] [get|put] <filename>
  # 예시
    python mytftp_client.py 203.250.133.88 get tftp.conf
   //호스트 주소 203.250.133.88에 연결하여 tftp.conf 파일을 다운로드 받는다.
    python mytftp_client.py 203.250.133.88 -p 69 put myfile.txt
   //호스트 주소 203.250.133.88에 연결하고 포트 번호를 69로 지정하여 myfile.txt 파일을 업로드한다.
    


