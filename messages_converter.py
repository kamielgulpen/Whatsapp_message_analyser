import pandas as pd
import re
import dateparser


def message_converter(file_name):

    f = open(, "r",encoding="utf8")

    years = []
    months = []
    days = []
    hours = []
    names = []
    messages = []
    text = f.readlines()
    for line in text:
        # print(line)
        line = line.replace(',', '')
        line = str(line)
        try:
            date = re.match(r"[^[]*\[([^]]*)\]", line).groups()[0]
            years.append(dateparser.parse(date).year)
            months.append(dateparser.parse(date).month)
            days.append(dateparser.parse(date).day)  
            hours.append(dateparser.parse(date).hour)

            line = re.sub(r'[^[]*\[([^]]*)\]', '', line, flags=re.DOTALL)
        
            name = line.split(':')[0]
            names.append(name)
        
            message = line.replace(name + ':', '')
            messages.append(message)

        except:
            messages[-1] = messages[-1] + line


    df = pd.DataFrame()

    df['year'] = years
    df['month'] = months

    df['day'] = days
    df['hour'] = hours
    df['name'] = names
    df['message'] = messages

    df.to_csv('messages.csv')

if __name__ == "__main__":

    file_name = ''

    message_converter(file_name)