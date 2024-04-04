from flask import Flask, render_template, redirect, url_for, request
from ubidots import ApiClient

app = Flask(__name__)

API_TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"
LABEL_SWITCH = "65d060812df70c000c9ec776"
LABEL_POWER = "65a78f512b1149000b6718df"
LABEL_FEED1 = "65aa395aec1b72000ed90368"
LABEL_FEED2 = "65aa395f92fb80000ccb0e3d"
LABEL_TEMPHIGH = "65aa395aec1b72000ed90368"
LABEL_TEMPLOW = "65aa395f92fb80000ccb0e3d"
api = ApiClient(token=API_TOKEN)
variable_tombol1 = api.get_variable(LABEL_SWITCH)
variable_tombol2 = api.get_variable(LABEL_POWER)
variable_jadwal1 = api.get_variable(LABEL_FEED1)
variable_jadwal2 = api.get_variable(LABEL_FEED2)
variable_tempHigh = api.get_variable(LABEL_TEMPHIGH)
variable_tempLow = api.get_variable(LABEL_TEMPLOW)

@app.route('/')
def front():
    return render_template('front.html')

@app.route('/daya', methods=('GET','POST'))
def daya():
    switch_value = variable_tombol1.get_values(1)[0]['value']
    power_value = variable_tombol2.get_values(1)[0]['value']

    return render_template("daya.html", switch_value=switch_value, power_value=power_value)

# Route untuk mengganti nilai tombol switch
@app.route('/toggle_switch', methods=['POST'])
def toggle_switch():
    switch_value = variable_tombol1.get_values(1)[0]['value']
    new_value1 = toggle_value(switch_value)
    variable_tombol1.save_value({'value': new_value1})
    return redirect('/daya')

# Route untuk mengganti nilai tombol power
@app.route('/toggle_power', methods=['POST'])
def toggle_power():
    power_value = variable_tombol2.get_values(1)[0]['value']
    new_value2 = toggle_value(power_value)
    variable_tombol2.save_value({'value': new_value2})
    return redirect('/daya')

def toggle_value(current_value):
    if current_value == 0:
        return 1
    else:
        return 0

@app.route('/pakan', methods=('GET','POST'))
def pakan(): 
    if request.method == 'POST':
        feeding_schedule_1 = convert_to_HHMM(request.form['jamPakan1'])
        feeding_schedule_2 = convert_to_HHMM(request.form['jamPakan2'])
        variable_jadwal1.save_value({'value': feeding_schedule_1})
        variable_jadwal2.save_value({'value': feeding_schedule_2})

    feeding_schedule_1 = convert_to_time(int(variable_jadwal1.get_values(1)[0]['value']))
    feeding_schedule_2 = convert_to_time(int(variable_jadwal2.get_values(1)[0]['value']))
    return render_template("pakan.html", feeding_schedule_1 = feeding_schedule_1, feeding_schedule_2 = feeding_schedule_2)

def convert_to_HHMM(time_str):
    # Memisahkan jam dan menit dari string waktu
    hours, minutes = time_str.split(':')

    # Menggabungkan jam dan menit menjadi format HHMM
    time_HHMM = hours + minutes

    return time_HHMM

def convert_to_time(schedule_value):
    # Konversi angka ke string
    schedule_str = str(schedule_value)

    # Pastikan panjang string setidaknya 4 digit (hhmm)
    while len(schedule_str) < 4:
        schedule_str = '0' + schedule_str

    # Ambil dua digit pertama sebagai jam dan dua digit terakhir sebagai menit
    hours = int(schedule_str[:2])
    minutes = int(schedule_str[2:])

    # Format waktu ke string "hh:mm"
    time_str = f"{hours:02d}:{minutes:02d}"

    return time_str

@app.route('/suhu', methods=('GET','POST'))
def suhu ():
    if request.method == 'POST':
        temp_high = request.form['temp_high']
        temp_low = request.form['temp_low']
        variable_tempHigh.save_value({'value': temp_high})
        variable_tempLow.save_value({'value': temp_low})

    temp_high = int(variable_tempHigh.get_values(1)[0]['value'])
    temp_low = int(variable_tempLow.get_values(1)[0]['value'])

    return render_template("suhu.html", temp_high=temp_high, temp_low=temp_low)

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')

if __name__ == '__main__':
    app.run(debug=True)

