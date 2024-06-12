import asyncio
from pyppeteer import launch

async def send_message_to_gradio_api(prompt):
    browser = await launch(headless=True)  # Запускаем браузер в обычном режиме, чтобы видеть действия
    page = await browser.newPage()

    # Открываем сайт
    await page.goto('https://chat.lmsys.org', {'waitUntil': 'networkidle2'})
    
    # Подождём, пока страница полностью загрузится
    await asyncio.sleep(5)  # Возможно, потребуется увеличить время ожидания
    
    # Симулируем действия пользователя
    await page.mouse.move(100, 100)
    await page.mouse.move(200, 200)
    await page.mouse.click(300, 300)
    await page.keyboard.press('ArrowDown')
    await page.keyboard.press('ArrowUp')
    await asyncio.sleep(10)  # Возможно, потребуется увеличить время ожидания
    
    # Создание скриншота для диагностики
    await page.screenshot({'path': 'screenshot.png'})
    
    # Найдите текстовое поле для ввода сообщения
    await page.waitForSelector('input[placeholder="Type a message..."]', {'timeout': 10000})
    input_box = await page.querySelector('input[placeholder="Type a message..."]')
    
    if input_box:
        # Введите сообщение
        await input_box.type(prompt)
        await input_box.press('Enter')
        
        # Подождите, пока придет ответ
        await asyncio.sleep(10)  # Возможно, потребуется увеличить время ожидания
        
        # Найдите элемент с ответом и прочитайте его
        response_elements = await page.querySelectorAll('div[class*="message-in"]')
        if response_elements:
            response = await page.evaluate('(element) => element.textContent', response_elements[-1])
            await browser.close()
            return response
        else:
            await browser.close()
            return "No response found"
    else:
        await browser.close()
        return "Input box not found"

prompt = "Привет, как дела?"
response = asyncio.get_event_loop().run_until_complete(send_message_to_gradio_api(prompt))

print("Response:", response)