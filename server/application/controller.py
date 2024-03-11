import telegram

class Controller():
    def __init__(self) -> None:
        self._temperature = 0.0
        self._htt = 38.0 # high temperature threshold
        self._door = "closed"

    def setDoorState(self, state):
        if self._door == state:
            return

        self._door = state

        if state == "open":
            telegram.send_telegram_message(f'puerta abierta')
        elif state == "closed":
            telegram.send_telegram_message(f'puerta cerrada')
        else:
            return False

    def getDoorState(self):
        return self._door

    def setTemperature(self, temp):
        self._temperature = temp

        if temp >= self._htt:
            telegram.send_telegram_message(f'la temperatura es alta: {temp}')

    def getTemperature(self):
        return self._temperature

    def setHighTemperatureThreshold(self, temp):
        self._htt = temp

    def getHighTemperatureThreshold(self):
        return self._htt