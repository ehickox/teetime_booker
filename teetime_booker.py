import sys
import requests
import datetime

config_lines = [line.strip() for line in open('config.txt')]
V_WEBSITE = config_lines[0]
V_USERNAME = config_lines[1]
V_PASSWORD = config_lines[2]
V_COURSE_NAME_ABBR = config_lines[3]
V_COURSE_NAME = config_lines[4]
V_SYSTEM = config_lines[5]

LOGIN_URL = V_WEBSITE+"/index.php/api/booking/users/login"
OPEN_TEE_TIMES_URL = V_WEBSITE+"/index.php/api/booking/times"
BOOK_URL = V_WEBSITE+"/index.php/api/booking/users/reservations"
DELETE_URL = V_WEBSITE+"/index.php/api/booking/users/reservations/"

def get_best_teetime(tee_times):
    my_time_available = False
    times = []
    times_9 = []
    best_time = None
    for teetime in tee_times:
        times.append(teetime.get('time'))
        if "09" in teetime.get('time'):
            times_9.append(teetime.get('time'))
        if "09:30" in teetime.get('time'):
            my_time_available = True
            best_time = teetime

    print("Hello, Mr. Hickox...")
    if my_time_available:
        print("Good news! Your usuall Sunday teetime of 9:30 AM is available!")
    elif len(times_9) > 0:
        print("Unfortunately, your usual Sunday teetime is unavailable. However, there are "+str(len(times_9))+" times open in the hour of 9.")
        best_time = times_9[0]

    return best_time
              
def login(username, password):
    v_headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    payload = {"api_key":"no_limits", "booking_class_id":None,
               "password":password, "username":username}
    response = requests.post(LOGIN_URL, data=payload)
    is_okay = response.status_code == requests.codes.ok
    if is_okay:
        print("Logged in!")
    else:
        response.raise_for_status()

def book_teetime(time):
    print("Booking teetime: "+str(time))
    payload = "{\"teesheet_id\":\"331\",\"teesheet_holes\":\"9\",\"time\":\""+time+"\",\"course_id\":\"18723\",\"course_name\":\""+V_COURSE_NAME_ABBR+"\",\"schedule_name\":\""+V_COURSE_NAME+"\",\"schedule_id\":\"331\",\"available_spots\":4,\"minimum_players\":2,\"holes\":\"9\",\"has_special\":false,\"special_discount_percentage\":0,\"group_id\":false,\"require_credit_card\":\"0\",\"booking_class_id\":false,\"green_fee_tax_rate\":false,\"cart_fee_tax_rate\":false,\"green_fee_tax\":0,\"cart_fee_tax\":0,\"special_id\":false,\""+V_SYSTEM+"_discount\":false,\"pay_online\":\"no\",\"green_fee\":21,\"rate_type\":\"walking\",\"players\":2,\"carts\":false,\"cart_fee\":false,\"promo_code\":\"\",\"promo_discount\":0,\"player_list\":false,\"hide_prices\":false,\"show_course_name\":false,\"min_players\":1,\"total\":42,\"purchased\":false,\"pay_players\":2,\"pay_carts\":false,\"pay_total\":31.5,\"pay_subtotal\":42,\"paid_player_count\":0,\"discount_percent\":0,\"discount\":10.5,\"subtotal\":42,\"show_course_info\":false,\"course\":false}"
    headers = {
            'x-newrelic-id': "VQ8GUFFQGwIAUFRbAgU=",
            'origin': V_WEBSITE,
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
            'content-type': "application/json",
            'accept': "application/json, text/javascript, */*; q=0.01",
            'x-requested-with': "XMLHttpRequest",
            'api-key': "no_limits",
            'referer': V_WEBSITE+"/index.php/booking/index/18723",
            'accept-encoding': "gzip, deflate",
            'accept-language': "en-US,en;q=0.8",
            'cookie': "PHPSESSID=us4fev8qfjdmr8titegb4g1b80; _ga=GA1.2.953912948.1460470675; _gat=1; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJleGFtcGxlLmNvbSIsImF1ZCI6ImV4YW1wbGUub3JnIiwiaWF0IjoxNDYwNDcwNzQ4LCJleHAiOjE0NjA0NzQzNDgsInVpZCI6IjU1MzIzNzEiLCJsZXZlbCI6MCwiY2lkIjoiMTg3MjMiLCJlbXBsb3llZSI6ZmFsc2V9._FUYou6knUnFzkuIRMnK0NnV-bOojA2sYoeLFJxMf-jTkIEqbKg4I_ahtTI4smVlhNP1NqUPWMpbPyxOXjagBA; PHPSESSID=us4fev8qfjdmr8titegb4g1b80; _ga=GA1.2.953912948.1460470675; _gat=1; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJleGFtcGxlLmNvbSIsImF1ZCI6ImV4YW1wbGUub3JnIiwiaWF0IjoxNDYwNDcwNzQ4LCJleHAiOjE0NjA0NzQzNDgsInVpZCI6IjU1MzIzNzEiLCJsZXZlbCI6MCwiY2lkIjoiMTg3MjMiLCJlbXBsb3llZSI6ZmFsc2V9._FUYou6knUnFzkuIRMnK0NnV-bOojA2sYoeLFJxMf-jTkIEqbKg4I_ahtTI4smVlhNP1NqUPWMpbPyxOXjagBA",
            'cache-control': "no-cache",
            'postman-token': "dddd01c1-8ddd-7ddd-1c1c-b1c80c9ec218"
            }
    if not dryrun:
        response = requests.request("POST", BOOK_URL, data=payload, headers=headers)
        print("Booking response status code: "+str(response.status_code))
        if response.status_code == requests.codes.ok:
            print("Booked teetime: "+str(time))
        else:
            response.raise_for_status()
    else:
        print("Not actually booking teetime. Dryrun requested")
        
def get_open_morning_teetimes(v_month, v_day, v_year=2016):
    v_time = "morning"
    v_holes = "9"
    v_players = "2"
    v_booking_class = False
    v_schedule_id = "331"
    v_specials_only = "0"
    v_api_key = "no_limits"
    v_date = str(v_month) + "-" + str(v_day) + "-" + str(v_year)

    payload = {"time":v_time, "date":v_date, "holes":v_holes, "players": v_players,
               "booking_class": v_booking_class, "schedule_id":v_schedule_id,
               "specials_only": v_specials_only, "api_key": v_api_key}

    resp = requests.get(OPEN_TEE_TIMES_URL, params=payload)

    open_tee_times = resp.json()
    date_readable = str(v_month) + "-" + str(v_day) + "-" + str(v_year)
    print("There are "+str(len(open_tee_times))+" morning tee times available for "+date_readable+".")
              
    return open_tee_times

if __name__ == '__main__':
    dryrun = False
    args = sys.argv
    if len(args) > 1:
        if args[1] == '--dry' or args[1] == '-d':
            dryrun = True
            
    d = datetime.date.today()
    while d.weekday() != 6:
        d += datetime.timedelta(1)

    print("This Sunday is: "+str(d))
    login(V_USERNAME, V_PASSWORD)
    teetimes = get_open_morning_teetimes(v_month=d.month, v_day=d.day, v_year=d.year)
    best_teetime = get_best_teetime(teetimes)
    if best_teetime != None:
        book_teetime(best_teetime)
    else:
        print("Unable to book preferred teetime. Please select a preffered time: ")
        time_dict = {}
        for idx, tt in enumerate(teetimes):
            time_dict[idx] = tt.get('time')
            print(str(idx)+") "+tt.get('time'))
            
        selected_time_idx = input("> ")
        selected_time = time_dict[selected_time_idx]
        book_teetime(best_time, dryrun)
