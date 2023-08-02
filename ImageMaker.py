# -*- coding: utf-8 -*-

import cv2

"""
Метод для формирования изображения с данными о погоде на момент запроса.
Предоставляет класс со следующим функционалом:
подбора изображения;
внесение на него информации о погоде; 
демонстрации изображения в окне.
Сохранение готового изображения происходит в коренной папке с именем result.jpg

Use python 3.11
"""


class ImageMaker:

    def __init__(self, weather):
        self.temp = weather['temp']
        self.date = weather['date']
        self.weather = weather['weather']
        self.wind = weather['wind']
        self.city = weather['city']
        self.image = None
        self.result = None

    def image_choise(self):
        """Функция подбора изображения в зависимости от погоды."""
        if 'обл' in self.weather or 'пасм' in self.weather:
            self.image = cv2.imread('weather_img/cloud.png', cv2.IMREAD_UNCHANGED)
        elif 'дожд' in self.weather:
            self.image = cv2.imread('weather_img/rain.png', cv2.IMREAD_UNCHANGED)
        elif 'снег' in self.weather:
            self.image = cv2.imread('weather_img/snow.png', cv2.IMREAD_UNCHANGED)
        elif 'солн' in self.weather or 'ясн' in self.weather:
            self.image = cv2.imread('weather_img/sun.png', cv2.IMREAD_UNCHANGED)
        else:
            self.image = cv2.imread('weather_img/cloud.png', cv2.IMREAD_UNCHANGED)

    def image_make(self):
        """Функция формирования изображения с внесением на него данных о погоде."""
        self.image_choise()
        self.image = cv2.resize(self.image, (900, 900), interpolation=cv2.INTER_AREA)
        position_temp = (340, 480)
        self.result = cv2.putText(self.image, str(self.temp), position_temp,
                                  cv2.FONT_HERSHEY_COMPLEX, 3.5, (0, 0, 0), 4)
        position_weather = (40, 100)
        self.result = cv2.putText(self.image, str(self.weather), position_weather,
                                  cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        position_wind = (600, 200)
        self.result = cv2.putText(self.image, str(self.wind) + 'м/с', position_wind,
                                  cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        position_city = (100, 760)
        self.result = cv2.putText(self.image, str(self.city), position_city,
                                  cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        position_date = (100, 850)
        self.result = cv2.putText(self.image, str(self.date), position_date,
                                  cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.imwrite('result.jpg', self.result)

    def view_image(self):
        """Функция для демонстрации изображения."""
        cv2.namedWindow(f'Погода за {self.date}', cv2.WINDOW_NORMAL)
        cv2.imshow(f'Погода за {self.date}', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
