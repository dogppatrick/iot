a = ReadList["/home/pi/iot/sensor.log"]
b = FromDigits[a]
c = x^3-x^2-x-1 /. (x-> b) 

Print[c]

