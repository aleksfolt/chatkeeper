import time
import asyncio


async def _line_to_sec(zov, svo):
    if svo in ['год', 'года', 'г', 'лет', 'y', 'year', 'years']:
        return int(zov) * 31536000
    elif svo in ['месяц', 'месяцев', 'month','months']:
        return int(zov) * 2592000
    elif svo in ['неделя', 'недель', 'недели', 'н', 'week', 'weeks', 'w']:
        return int(zov) * 604800
    elif svo in ['день', 'дней', 'дня', 'days', 'day', 'd', 'д']:
        return int(zov) * 86400
    elif svo in ['час', 'часов', 'часа', 'hour', 'hours', 'h', 'ч']:
        return int(zov) * 3600
    elif svo in ['минут', 'минута', 'минутка', 'минуточек', 'мин', 'min', 'minutes', 'm', 'м']:
        return int(zov) * 60
    else:
        return None


async def time_to_seconds(line):
        zov = ''
        svo = ''
        flag = True
        for i in line:
            if i in '1234567890' and flag:
                zov += i
                continue
            elif i == ' ' and flag:
                flag = False
                continue
            else:
                flag = False
            if i not in '1234567890 ' and not flag:
                svo += i
            elif not flag:
                break
        if zov == '':
            zov = '1'
        print(f'{zov} {svo}')
        return _line_to_sec(zov.strip(), svo.strip())


async def seconds_to_time(sec):
    sec = int(sec - time.time())
    line = ''
    goida = {
        'year': False,
        'month': False,
        'day': False,
        'hour': False,
        'min': False,
        'sec': False
    }

    if sec > 31536000: #year
        temp = sec // 31536000
        if temp % 100 == 0:
            line = line + str(temp) + 'лет '
        temp = temp // 100
        hui = temp % 100
        if hui > 20:
            hui = hui % 10
        if hui == 1:
            line = line + str(temp) + 'год '
        elif hui >= 2 and hui <= 4:
            line = line + str(temp) + 'года '
        elif hui >= 5 and hui <= 21:
            line = line + str(temp) + 'лет '
        sec = sec % 31536000
        goida['year'] = True

    if sec > 2592000:
        temp = sec // 2592000
        if temp == 1:
            line = line + str(temp) + 'месяц '
        elif temp >= 2 and temp <= 4:
            line = line + str(temp) + 'месяца '
        else:
            line = line + str(temp) + 'месяцев '
        sec = sec % 2592000
        goida['month'] = True

    if sec > 86400:
        temp = sec // 86400
        if temp == 1 or temp == 21:
            line = line + str(temp) + 'день '
        elif (temp >= 2 and temp <= 4) or (temp >= 22 and temp <= 24):
            line = line + str(temp) + 'дня '
        elif (temp >= 5 and temp <= 20) or (temp >= 25 and temp <= 30):
            line = line + str(temp) + 'дней '
        sec = sec % 2592000
        goida['day'] = True

    if not goida['year'] and not goida['month']:
        if sec > 3600:
            temp = sec // 3600
            if temp > 20:
                hui = temp % 10
            else:
                hui = temp
            if hui == 1:
                line = line + str(temp) + 'час '
            elif hui >= 2 and hui <= 4:
                line = line + str(temp) + 'часа '
            elif hui >= 5 and hui <= 20:
                line = line + str(temp) + 'часов '
            sec = sec % 3600
            goida['hour'] = True

        if not goida['day']:
            if sec > 60:
                temp = sec // 60
                if temp > 20:
                    hui = temp % 10
                else:
                    hui = temp
                if hui == 1:
                    line = line + str(temp) + 'минута '
                elif hui >= 2 and hui <= 4:
                    line = line + str(temp) + 'минуты '
                elif hui >= 5 and hui <= 20:
                    line = line + str(temp) + 'минут '
                sec = sec % 60
                goida['min'] = True

            if not goida['hour'] and not goida['min']:
                temp = sec
                if temp > 20:
                    hui = temp % 10
                else:
                    hui = temp
                if hui == 1:
                    line = line + str(temp) + 'секунда '
                elif hui >= 2 and hui <= 4:
                    line = line + str(temp) + 'секунды '
                elif hui >= 5 and hui <= 20 or hui == 0:
                    line = line + str(temp) + 'секунд '
                goida['sec'] = True
    return line.strip()  # всем привет это я гей
