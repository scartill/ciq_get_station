using Toybox.WatchUi;
using Toybox.Timer;

class MoscowTransportWidgetView extends WatchUi.View {
    hidden var message = "Init";
    hidden var dataTimer;

    function initialize() {
        WatchUi.View.initialize();
    }

    // Load your resources here
    function onLayout(dc) {
        message = "Requesting";
        makeRequest();
        dataTimer = new Timer.Timer();
        dataTimer.start(method(:timerCallback), 60000, true);
    }

    // Restore the state of the app and prepare the view to be shown
    function onShow() {
    }

    // Update the view
    function onUpdate(dc) {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        dc.drawText(dc.getWidth()/2, dc.getHeight()/2, Graphics.FONT_MEDIUM, message, Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
    }

    // Called when this View is removed from the screen. Save the
    // state of your app here.
    function onHide() {
    }
    
    function makeRequest() {
	    var stationID = "stop__9712186";
        Communications.makeWebRequest(
            "https://s9blhw4mga.execute-api.us-east-2.amazonaws.com/default/ciq_get_station?station_id=" + stationID,
            {
            },
            {
                "Referrer" => "Garmin Fenix Widget"
            },
            method(:receiveCallback)
        );
    }
    
	function timerCallback() {
		makeRequest();
    }
    
    function receiveCallback(responseCode, data) {
        if (responseCode == 200) {
            message = data;
        } else {
            message = "Error: " + responseCode.toString();
        }
        
		WatchUi.requestUpdate();
    }
}
