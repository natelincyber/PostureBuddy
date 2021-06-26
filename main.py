from flask import Flask
from flask import render_template
from flask import Response

import webbrowser, _thread, time

import poseModule

app = Flask(__name__)

detector = poseModule.poseDetector()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/demo')
def demo():
    detector.setarmsCounter(0)
    detector.setlegsCounter(0)
    detector.setswayCounter(0)
    detector.sethandsCounter(0)
    detector.setfidgetCounter(0)
    detector.setfocusCounter(0)
    detector.setuniversalCounter(0)
    return render_template('demo.html')


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def calculateGrade(arms, legs, sway, armsDown, fidget, focus):

    threshold = 0
    nums = [arms, legs, sway, armsDown, fidget, focus]

    for i in range(len(nums)):
        if nums[i] > 20:
            threshold += 1

    if threshold == 0:
        return "a"
    elif threshold == 1:
        return "b"
    elif threshold == 2:
        return "c"
    elif threshold == 3:
        return "d"
    else:
        return "d"


def generateTips(arms, legs, sway, armsDown, fidget, focus):

    nums = {"6": arms,
            "5": legs,
            "2": sway,
            "1": armsDown,
            "3": fidget,
            "4": focus
            }

    numsSorted = {k: v for k, v in sorted(
        nums.items(), key=lambda item: item[1])}

    tip1 = list(numsSorted.keys())[-1]
    tip2 = list(numsSorted.keys())[-2]

    return tip1, tip2


@app.route('/results')
def results():
    armscounter = int(detector.getarmsCounter())
    legscounter = int(detector.getlegsCounter())
    swaycounter = int(detector.getswayCounter())
    armsdowncounter = int(detector.gethandsCounter())
    fidgetcounter = int(detector.getfidgetCounter())
    focuscounter = int(detector.getfocusCounter())
    time = int(detector.getuniversalCounter())

    armsPercent = int((armscounter/time) * 100)
    legsPercent = int((legscounter/time) * 100)
    swayPercent = int((swaycounter/time) * 100)
    armsDownPercent = int((armsdowncounter/time) * 100)
    fidgetPercent = int((fidgetcounter/time) * 100)
    focusPercent = int((focuscounter/time) * 100)

    convertedTime = convert(time)
    armscounter = convert(armscounter)
    legscounter = convert(legscounter)
    swaycounter = convert(swaycounter)
    armsdowncounter = convert(armsdowncounter)
    fidgetcounter = convert(fidgetcounter)
    focuscounter = convert(focuscounter)

    grade = calculateGrade(armsPercent, legsPercent, swayPercent,
                           armsDownPercent, fidgetPercent, focusPercent)

    tip1, tip2 = generateTips(
        armsPercent, legsPercent, swayPercent, armsDownPercent, fidgetPercent, focusPercent)

    if tip2 < tip1:
        tip1, tip2 = tip2, tip1

    return render_template('results.html', armscounter=armscounter, legscounter=legscounter,
                           swaycounter=swaycounter, armsdowncounter=armsdowncounter,
                           fidgetcounter=fidgetcounter, focuscounter=focuscounter, time=time,
                           armsPercent=armsPercent, legsPercent=legsPercent, swayPercent=swayPercent,
                           armsDownPercent=armsDownPercent, fidgetPercent=fidgetPercent,
                           focusPercent=focusPercent, convertedTime=convertedTime, grade=grade,
                           tip1=tip1, tip2=tip2)


@app.route('/preloader')
def preloader():
    return render_template('preloader.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/video_feed')
def video_feed():
    return Response(poseModule.main(detector), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == "__main__":
    # host
    app.run(host='127.0.0.1', debug=True, port=5000)

    
