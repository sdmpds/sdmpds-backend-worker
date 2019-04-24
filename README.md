# MMS - application description.

**MMS** is a mobile, REST API application which is used to monitoring. The main purpose of this application is processing and analyzing photos which are uploaded by users in order to obtain information about people in the pictures. The big advantage of this application is that it is cross-platform. This fact cause that application can work under the control of Android and iOS. The application also uses native elements of mobile devices - GPS module, which provides the location of the user and the camera.\
MMS is based on client-server architecture. The client is responsible for collecting and sending data (photos / images), and the server is to analyze and store this data. The client part was written in JavaScript (using React-Native framework), and the server part in Python (using Flask framework).

## 1. Organization of the project team.

-	Tomasz Kozub - Project Manager and Front-End Developer
-	Jakub Wąsik – Back-End Developer
-	Alicja Piotrowska - Back-End Developer
-	Kamil Morawiecki - Back-End Developer (body detection part)
-	Paweł Gawlik - tester

## 2. Functionality description

The application consists of a mobile client for Android / iOS devices and a server which contains software used to detect objects (people) from images.

### 2.1. The application client’s tasks:
- Downloading the user's location
- Displaying the user's location on the map
- Sending two types of marker:
	- Sending images along with location data to the server for analysis
	- Sending a marker ["question mark"] with location of a given point on the map with a request to analyze of a given area by other users
- Downloading from the server and displaying markers which contain description with the number of recognized objects (peaople) in a given place and the date of analysis

### 2.2. The application server’s tasks:
- Collecting data on currently connected users
- Receiving two types of queries from users:
	- For image analysis by middleware
	- To display the ["question mark"] mark to all users
- Sending a list of tags to users along with attached data regarding the analyzed images
- Receiving pictures from users, processing these images thanks to the mechanism of body detection and, as a consequence, obtaining specific statistics from them

# Mobile client for MMS application

<img width="50%" height="50%" src="https://i.imgur.com/IkXPlbT.png"/><img width="50%" height="50%" src="https://i.imgur.com/BuxpbK3.png"/><img width="50%" height="50%" src="https://i.imgur.com/rkUfM4p.png"/><img width="50%" height="50%" src="https://i.imgur.com/QIjZt8W.png"/><img width="50%" height="50%" src="https://i.imgur.com/52TkNGg.png"/><img width="50%" height="50%" src="https://i.imgur.com/l4RZhdy.jpg"/>

## 1. Getting Started

Clone Repo

````
https://github.com/sdmms/sdmms-mobile-client.git
````

Install dependecies for react native

````
cd sdmms-mobile-client
npm install
````

## 2. React Native Requirements and Getting Started

<a href="https://facebook.github.io/react-native/docs/getting-started.html" target="_blank">Requirements and Getting Started</a>

<a href="https://facebook.github.io/react-native/docs/android-setup.html" target="_blank">Android Setup</a>

### IOS

````
Open sdmms-mobile-client.xcodeproj in XCode
````

### Android

````
navigate to sdmms-mobile-client
react-native run-android

````
