function progess_indicator(loops: number) {
    for (let index = 0; index < loops; index++) {
        led.toggle(2, 4)
        basic.pause(1000)
    }
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    basic.showString("temp:" + ("" + ("" + input.temperature())))
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    basic.showString("light:" + ("" + ("" + input.lightLevel())))
})
basic.showIcon(IconNames.Happy)
basic.pause(500)
basic.clearScreen()
basic.forever(function on_forever() {
    serial.writeLine("" + ("" + input.temperature()) + "," + ("" + ("" + input.lightLevel())))
    progess_indicator(30)
})
