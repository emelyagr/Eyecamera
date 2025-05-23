import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time

# Автор проекта: Емельянов Григорий Андреевич @emelyagr https://github.com/emelyagr
# Author of the project: Emelyanov Grigory Andreevich @emelyagr https://github.com/emelyagr -->

# Настройки SMTP-сервера mail.ru
smtp_server = 'smtp.mail.ru'
smtp_port = 465
smtp_login = 'youremail@mail.ru'
smtp_password = 'yourpassword'

# Функция для захвата изображения с камеры
def capture_image():
    # Инициализация камеры
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру")
        return None

    # Захват одного кадра
    ret, frame = cap.read()

    if not ret:
        print("Ошибка: Не удалось захватить изображение")
        return None

    # Освобождение камеры
    cap.release()

    # Сохранение изображения
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)
    return image_path

# Функция для отправки email
def send_email(image_path):
    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = smtp_login
    msg['To'] = smtp_login
    msg['Subject'] = 'Снимок с камеры'

    # Текстовое сообщение
    body = 'Приложен снимок, сделанный с камеры.'
    msg.attach(MIMEText(body, 'plain'))

    # Приложение изображения
    try:
        attachment = open(image_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(image_path)}')
        msg.attach(part)
    except Exception as e:
        print(f"Ошибка при присоединении файла: {e}")
        return

    # Отправка email
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_login, smtp_password)
        server.sendmail(smtp_login, smtp_login, msg.as_string())
        server.quit()
        print("Email успешно отправлен")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

# Автор проекта: Емельянов Григорий Андреевич @emelyagr https://github.com/emelyagr
# Author of the project: Emelyanov Grigory Andreevich @emelyagr https://github.com/emelyagr -->

# Основная функция
def main():
    while True:
        image_path = capture_image()
        if image_path:
            send_email(image_path)
        time.sleep(5)

if __name__ == "__main__":
    main()
