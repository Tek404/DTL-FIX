# marketdata_request.py
import quickfix as fix

class MarketDataRequestApp(fix.Application):
    def onCreate(self, sessionID):
        print("Session created:", sessionID)

    def onLogon(self, sessionID):
        print("Logged on:", sessionID)
        self.sendNewOrder(sessionID)
        self.sendOrderCancelRequest(sessionID)

    def fromApp(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        msgTypeValue = msgType.getValue()

        if msgTypeValue == "3":  # Reject (35=3)
            self.handleReject(message, sessionID)
        elif msgTypeValue == "8":  # Execution Report (35=8)
            self.handleExecutionReport(message, sessionID)
        elif msgTypeValue == "9":  # Order Cancel Reject (35=9)
            self.handleOrderCancelReject(message, sessionID)
        else:
            print("Received unsupported message type:", msgTypeValue)

    def toApp(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        msgTypeValue = msgType.getValue()

        if msgTypeValue == "0":  # Heartbeat (35=0)
            print("Sending Heartbeat message")
            heartbeat_message = fix.Message()
            heartbeat_message.getHeader().setField(fix.MsgType("0"))  # 35=0 for Heartbeat
            fix.Session.sendToTarget(heartbeat_message, sessionID)
        else:
            print("Received message:", message)

    def onLogout(self, sessionID):
        print("Logged out:", sessionID)

    def toAdmin(self, message, sessionID):
        pass

    def fromAdmin(self, message, sessionID):
        return

    def sendNewOrder(self, sessionID):
        new_order_message = fix.Message()
        new_order_message.getHeader().setField(fix.MsgType("D"))  # 35=D for New Order 
        fix.Session.sendToTarget(new_order_message, sessionID)

    def sendOrderCancelRequest(self, sessionID):
        cancel_request_message = fix.Message()
        cancel_request_message.getHeader().setField(fix.MsgType("F"))  # 35=F for Order Cancel Request

        fix.Session.sendToTarget(cancel_request_message, sessionID)

    def handleReject(self, message, sessionID):
        print("Received Reject message:", message)

    def handleExecutionReport(self, message, sessionID):
        print("Received Execution Report message:", message)

    def handleOrderCancelReject(self, message, sessionID):
        print("Received Order Cancel Reject message:", message)

def main():
    settings = fix.SessionSettings("marketdata.cfg")
    application = MarketDataRequestApp()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    initiator.start()
    print("Initiator started.")

    initiator.block()

if __name__ == "__main__":
    main()
