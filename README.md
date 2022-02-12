# Neural Transfer Style Telegram Bot

### Description:


*Нейронный перенос стиля* - это алгоритм, который принимает контент-изображение (например, черепаху), стиль-изображение (например, картинку известного художника) и возвращает изображение, которое будто бы нарисовано тем художником.

В этом боте используется алгоритм переноса стиля 
Леона А. Гатиса, Александра С. Эккера и Маттиаса Бетге.
[ссылка на статью Neural-Style](https://arxiv.org/abs/1508.06576)

Бот реализован на асинхронном фреймворке aiogram, в рамках итогового проекта в [Deep Learning School](https://www.dlschool.org) (осенний семестр 2021 базовый поток)

### Example
Original
![image](https://github.com/Ivanich-spb/TGbot_NNStyleTransfer/tree/master/images/example/content.jpg)
Style
![image](https://github.com/Ivanich-spb/TGbot_NNStyleTransfer/tree/master/images/example/style.jpg)
Result
![image](https://github.com/Ivanich-spb/TGbot_NNStyleTransfer/tree/master/images/example/result.png)
### Requirements

- Python 3.8
- PyTorch 
- TorchVision
- Pillow
- aiogram

_minimal hardware:_
- 1Gb Ram
- 1 core cpu

###Features
- aiogram FSM
- default styles
- asynchronous work (not realized yet)