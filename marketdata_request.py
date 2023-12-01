# marketdata_request.py
import quickfix as fix

class MarketDataRequestApp(fix.Application):
    def onCreate(self, sessionID):
        print("Session created:", sessionID)

    def onLogon(self, sessionID):
        print("Logged on:", sessionID)
        self.sendMarketDataRequest(sessionID)

    def fromApp(self, message, sessionID):
        print("Received message:", message)

    def toApp(self, message, sessionID):
        print("Sending message:", message)

    def onLogout(self, sessionID):
        print("Logged out:", sessionID)

    def sendMarketDataRequest(self, sessionID):
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.BeginString("FIX.4.2"))
        header.setField(fix.MsgType("V"))

        message.setField(fix.Symbol("AAPL"))
        message.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
        message.setField(fix.MarketDepth(1))

        fix.Session.sendToTarget(message, sessionID)

    def toAdmin(self, message, sessionID):
        # This method is called when administrative messages are being sent
        # Add your custom logic for handling administrative messages here
        pass
    def fromAdmin(self, message, sessionID):
        # Implement actions upon receiving administrative messages
        return
if __name__ == "__main__":
    settings = fix.SessionSettings("marketdata.cfg")
    application = MarketDataRequestApp()
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)
    initiator.start()
    initiator.block()

