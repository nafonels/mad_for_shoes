#1.어느 sns에서 각 제품들이 많이 노출 되었나(각 sns별 글 등록수 통계)
#1-1.각 sns별 데이터 모으기
install.packages('jsonlite')
install.packages('rjson')

library(jsonlite)
#library(rjson)

setwd('C:/Rwork/data/airmax97/')

#트위터의 에어맥스:airmax97_twit_post_final_1.json 파일 가져오기 
twi_airmax_data<-fromJSON('airmax97_twit_post_final_1.json')
twi_airmax_data<-twi_airmax_data[,c(1,2,4,5,6)] #필요한컬럼만뽑아오기
View(twi_airmax_data)

exportJson<-toJSON(twi_airmax_data) #데이터셋 dataset/.json파일로저장
write(exportJson, file='C:\\Rwork\\data\\dataset\\twi_airmax_data.json')

#인스타의 에어맥스:airmax97_insta_post.json 파일 가져오기
ins_airmax_data<-data.frame() #누적할 데이터프레임 설정
#여러개의 inst_post.json 붙히기. 필요한 .json 파일 갯수 확인
start<-1
end<-19 
a<-'airmax97_insta_post'
b<-'.json'
for (i in start:end) {
  i<-as.character(i)
  file_name<-paste(a,b, sep=i)
  ins_air_data<-fromJSON(file_name)
  d<-as.character(dim(ins_air_data))
  cat(i,'번째 ',d,'\n')
  ins_air_data<-ins_air_data[,c(1,3,4,5)] #필요한 컬럼만 뽑기
  
  #ins_airmax_data 누적변수에 누적하기 위해, rbind()
  ins_airmax_data<-rbind(ins_airmax_data, ins_air_data)
}
dim(ins_airmax_data)
View(ins_airmax_data)

exportJson<-toJSON(ins_airmax_data) #데이터셋 dataset/.json파일로저장
write(exportJson, file='C:\\Rwork\\data\\dataset\\ins_airmax_data.json')

#인스타의 경우, json파일이 많기 때문에 변수를 계속 만들고 
#그 변수들을하나로 모으는데 하나씩 하드 코딩이 힘들어 
#[for(){},paste(,sep=)]등 함수등을 활용하여 한 변수에 모으기
#rbind()를 활용하여 필요한 컬럼만 리코딩.

setwd('C:/Rwork/data/dis2/')

#트위터의 디스럽터2:dis2__twit_post_final_1.json 파일 가져오기 
twi_dis2_data<-fromJSON('dis2__twit_post_final_1.json')
twi_dis2_data<-twi_dis2_data[,c(1,2,4,5,6)] #필요한컬럼만뽑아오기
View(twi_dis2_data) 

exportJson<-toJSON(twi_dis2_data) #데이터셋 dataset/.json파일로 저장
write(exportJson, file='C:\\Rwork\\data\\dataset\\twi_dis2_data.json')

#인스타의 디스럽터2:dis2_insta_post1.json 파일들 가져오기
ins_dis2_data<-data.frame()
#여러개의 inst_post.json 붙히기. 필요한 .json 파일 갯수 확인
start<-1
end<-6 
a<-'dis2_insta_post'
b<-'.json'
for (i in start:end) {
  i<-as.character(i)
  file_name<-paste(a,b, sep=i)
  ins_d_data<-fromJSON(file_name)
  d<-as.character(dim(ins_d_data))
  cat(i,'번째 ',d,'\n')
  ins_d_data<-ins_d_data[,c(1,3,4,5)] #필요한 컬럼만 뽑게, 리코딩
  
  #ins_dis2_data 변수에 누적하기 위해, rbind
  ins_dis2_data<-rbind(ins_dis2_data, ins_d_data)
}
dim(ins_dis2_data)
View(ins_dis2_data)

exportJson<-toJSON(ins_dis2_data) #데이터셋 dataset/.json파일로저장
write(exportJson, file='C:\\Rwork\\data\\dataset\\ins_dis2_data.json')

#1-2.각 sns별 post 갯수 - 파이 그래프 그리기
par(mfrow=c(1,2)) #두개의 파이그래프 보이게 
t_header<-c('airmax97','disrupter2')
t_somedata<-c(length(twi_airmax_data$post_id),length(twi_dis2_data$post_id))
t_testdata<-xtabs(t_somedata ~ t_header) #xtbas()교차표만들기
t_testdata<-sort(t_testdata, decreasing=T)
t_colors<-c('purple','skyblue')
t_label<-paste(names(t_testdata),'\n',t_testdata,'개')
pie(t_testdata, labels=t_label, col=t_colors,
    main='Twitter(2018.5.14~22)', 
    cex=0.8, radius=1)

i_header<-c('airmax97','disrupter2')
i_somedata<-c(length(ins_airmax_data$post_id),length(ins_dis2_data$post_id))
i_testdata<-xtabs(i_somedata ~ i_header)
i_testdata<-sort(i_testdata, decreasing=T)
i_colors<-c('purple','skyblue')
i_label<-paste(names(i_testdata),'\n',i_testdata,'개')
pie(i_testdata, labels=i_label, col=i_colors,
    main='Instagram', 
    cex=0.8, radius=1)

#각 단계별로 전 코드를 다시 RUN을 해야하는 수고로움이 발생.
#필요한 컬럼들만 리코딩한 데이터셋을 .json파일로 저장하기.

#2.제품간 비교-인기도
#비율의 차이를 막대 그래프
#total : airmax97:1257 / distrupter2:357
#total : 1614
#각데이터들의 length()값을 변수에 넣어주기


setwd('C:\\Rwork\\data\\airmax97')
#twi_airmax_data<-fromJSON('twi_airmax_data.json') #post컬럼의 내용이 UTF-8 에러가 남.
twi_airmax_data<-fromJSON('airmax97_twit_post_final_1.json')
twi_airmax_data<-twi_airmax_data[,c(1,2,4,5,6)] #인코딩 에러로 인해, 원시데이터에서 정제시켜 다시 가져오기.

#데이터셋 모아 놓은 워킹디렉토리 재 설정
setwd('C:\\Rwork\\data\\dataset')

#변수에 정제된 데이터셋 json파일 불러오기
ins_airmax_data<-fromJSON('ins_airmax_data.json')

#airmax97
twi_a<- length(twi_airmax_data$post_id) 
ins_a<- length(ins_airmax_data$post_id)
sns_air<- twi_a+ins_a

#twi_dis2_data<-fromJSON('twi_dis2_data.json')
setwd('C:\\Rwork\\data\\dis2')

#twi_airmax_data<-fromJSON('twi_dis2_data.json') #post컬럼의 내용이 UTF-8 에러가 남.
twi_dis2_data<-fromJSON('dis2__twit_post_final_1.json')
twi_dis2_data<-twi_dis2_data[,c(1,2,4,5,6)] #인코딩 에러로 인해, 원시데이터에서 정제시켜 다시 가져오기.

#데이터셋 모아 놓은 워킹디렉토리 재 설정
#변수에 정제된 데이터셋 json파일 불러오기
setwd('C:\\Rwork\\data\\dataset')
ins_dis2_data<-fromJSON('ins_dis2_data.json')

#distrupter2
twi_d<- length(twi_dis2_data$post_id)
ins_d<- length(ins_dis2_data$post_id)
sns_dis<- twi_d+ins_d

#total=1614
sum_all<-twi_a+twi_d+ins_a+ins_d
#total

#(제품별 sns의 수/모든 sns의 모든 제품의 합)*100
result_a<-(sns_air/sum_all)*100
result_d<-(sns_dis/sum_all)*100
chart_data<-c(result_a, result_d)
names(chart_data)<-c('Airmax97','Disrupter2') 
str(chart_data)
chart_data #비율 벡터화 

#(이산변수-정수 단위로 나누어 측정)막대차트 시각화
#airmax->79.66 / disrupter2->20.34
barplot(chart_data, ylim=c(0,100), ylab='Rate',xlab='Products',
        col=c('purple','skyblue'),
        space=1,
        main='각 제품별 비율 분석(인기도)')

#3.에어맥스97/디스럽터2 일별 검색 비율 차이 분석(1활용)-추이그래프
#일자별의 데이터를 sum-코딩변경
#그래프에 열별로 두개의 데이터가 같이 보여지게-

#인스타그램 post_date 날짜값을 날짜형식으로 변환 : as.POSIXct()
#변환된 날짜 post_date2 컬럼으로 재정의
ins_airmax_data$post_date2<-as.POSIXct(ins_airmax_data$post_date, origin='1970-01-01')
sort(ins_airmax_data$post_date2)
#View(ins_airmax_data)

ins_dis2_data$post_date2<-as.POSIXct(ins_dis2_data$post_date, origin='1970-01-01')
sort(ins_dis2_data$post_date2)
#View(ins_dis2_data)

#네이버 검색 추이 시계열로 그래프 시각화

#datalab.xls : 일별로 네이버 검색어 추이 가져오기.(2018.4.28~5.24)
library(rJava)
library(xlsx)
setwd('C:\\Rwork\\data\\dataset')
datalab<-read.xlsx(file='datalab.xlsx', header=T, encoding='UTF-8', sheetIndex = 1)
View(datalab)

#dygraphs패키지 설치
install.packages('dygraphs')
library(dygraphs)

#시간 순서 속성을 지닌 xts데이터 타입
#xts()함수 사용하여 xts데이터 타입으로 변환
#xts패키지 로딩
library(xts)
na1<-xts(datalab$에어맥스97, order.by=as.Date(datalab$날짜1)) #order.by=datalab$날짜 이렇게 갖고 오니까 오류가 났습니다. 날짜형식으로 지정해주니까 오류 해결.
head(na1) #에어맥스97

na2<-xts(datalab$디스럽터2, order.by=as.Date(datalab$날짜2))
head(na2)#디스럽터2

#데이터 정제-두 데이터 cbind()가로로 통합+변수명 변경
naverlab<-cbind(na1, na2)
colnames(naverlab)<-c('naver_Airmax97','naver_Disrupter2')
head(naverlab)

dygraph(naverlab)


instalab<-cbind(insta_air,insta_dis)
colnames(instalab)<-c('insta_Airmax97', 'insta_Disrupter2')
head(instalab)

dygraph(instalab)

#그래프를 보기 좋게 하기 위하여, ins_airmax_data 데이터에서 2017년10월/2018년4월3일/2018년4월5일 데이터 행 지우기
ins_airmax_data<-ins_airmax_data[-654,] #2017년10월
ins_airmax_data<-ins_airmax_data[-388,] #2018년4월3일
ins_airmax_data<-ins_airmax_data[-389,] #2018년4월5일
#View(ins_airmax_data)

#airmax97 of instagram : like_rate 컬럼 생성
ins_airmax_data$like_rate<-(ins_airmax_data$like_count/max(ins_airmax_data$like_count))*100
View(ins_airmax_data)

#airmax97 of instagram xts 데이터 타입
insta_air<-xts(ins_airmax_data$like_rate, order.by=as.Date(ins_airmax_data$post_date2))
head(insta_air)

#disrupter2 of instagram : like_rate 컬럼 생성
ins_dis2_data$like_rate<-(ins_dis2_data$like_count/max(ins_dis2_data$like_count))*100
View(ins_dis2_data)

#disrupter2 of instagram xts 데이터 타입
insta_dis<-xts(ins_dis2_data$like_rate, order.by=as.Date(ins_dis2_data$post_date2))
head(insta_dis)

#like_rate컬럼 추가한 데이터셋 .json파일로 저장
exportJson<-toJSON(ins_airmax_data)
write(exportJson, file='C:\\Rwork\\data\\dataset\\ins_airmax_data.json')
exportJson<-toJSON(ins_dis2_data)
write(exportJson, file='C:\\Rwork\\data\\dataset\\ins_dis2_data.json')

#naver+instagram
lab<-cbind(na1, na2, insta_air, insta_dis)
colnames(lab)<-c('naver_Airmax97','naver_Disrupter2', 'insta_Airmax97','insta_Disrupter2')
head(lab)

dygraph(lab)
