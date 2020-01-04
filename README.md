# Making a Android APP with Python

The aim of design is to conmunicate with a single-chip microcomputer by TCP to complete my practicum.

1. Development Environment 
2. Packaging
3. Twisted
4. Kivy
5. Issue

## 1.Development Environment

Ubantu18 -LTS

python3

Twisted

Kivy

Buildozer

All of the above are free to use and you can install them according to the offical document.

## 2.Packaging

```javascript
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()
```
A class inherits kivy.app.App. Then, Its build() method is the first function to be executed and it return a root. Finally, the class TestApp is instantiated and calls its run() method.

The result.

![Image of Hello World](https://github.com/SamHara/Make-an-Android-APP-with-python/blob/master/helloworld.png)

**Package the python file as apk**

First, make a new folder in Ubantu OS.

Second, make a python file nemed main.py, which is specified by the offical.

Third, input the following command.
```
buildozer init
```
Then, configure the buildozer.spec file and you should pay attention to the following sentences.
```
# (list) Application requirements 
requirements = kivy, twisted, datetime
```
```
# (list) Permissions
android.permissions = INTERNET
```
Last, input the following command.
```
buildozer android debug
```
It would take a little time to download and the apk file will appear to the bin folder.

## 3.Teisted

The most important thing is that understanding some concept.

* Reactor:
   * Event loop

* Transports:
 * The details of connection.Such as TCP, a  stream-oriented connection. Interface:
 * write:
   * Write data to the connection.

Protocols:
    e.g. http.Interface:
    connectionMade:
        Called when a connection is made.
    dataReceived:
        Called when data is received.

Protocol Factories:
    Create a protocol for each new connection.

#### The template of server code:
```javascript
class Protocol(protocol.Protocol):
    •••

class Factory(Factory):
    •••

reactor.listenTCP(8000, Factory())
reactor.run()
```
#### The template of client code:
```javascript
class Protocol(protocol.Protocol):
    •••

class ClientFactory(protocol.ClientFactory):
    •••

reactor.connectTCP('localhost',8000,ClientFactory())
reactor.run()
```
## 4.Kivy

```javascript
from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()
```
The build() method above returns a root called widget.

**(1) Widget**

e.g. Label, TextInput, Button

**(2) Layout**

It is sure that the code above only has a root called widget. If you want to have two widgets, you should add multiple widget to a container called Layout as a root. There are a series of Layouts in kivy, e.g. FloatLayout.

**(3) Multiple Screens**

There is an issue, all widgets are inside a single screen. Sometimes, we need to have more the one  screen to work. The kivy provides kivy.uix.screenmanager.ScreenManager class to manage screens which are created by the kivy.uix.screenmanager.Screen class. Obviously, it is suitable to use ScreenManager as a root.

**(4) Class Reference**

  Sometimes, we have to reference a widget in python file. However, how to access a widget in the kv file? Assume that every widget has an id.

Single Screen:
    You can use the root.ids dictionary, e.g.self.root.ids['text_input_port']. It will return a class reference.

Multiple Screens:
    In order to access the screens, you can use this statement self.root.screens[num]. The num of that represents the screen's index. For example, the screen called MainScreen is the first element and thus its index is 0.After returning the class reference, we can access any widget within it.
    self.root.screens[0].ids['text_input_port']

**(5) kivy file's name**

  We have a class nemed ClientApp in the python file. Kivy extracts the text Client before the word App. After converting the Client to lowercase, you get a kv file's name. Moreover, if the python file and the kv file are in the same folder. Kivy will locate the KV file.

## 5.Issue

*Network Issue*
    
  We have LAN and WAN. The WAN IP can't access the LAN IP  only if you implement intranet penetration. However, I don't do that

*Storage Issue*

  If you store data in the variables, the data would disapear when you close the APP. Therefore, one of the best ways is to store the data in a file.

Last, the offical document is unfriendly to beginners. All in all,  I advise them to find a book to read.




