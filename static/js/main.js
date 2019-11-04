function startRecording()
{
//    console.log("Polling");
//    console.log("Current Url:"+document.URL);
    var btn = document.getElementById("recButton");
    currentURL = document.URL;

    if (btn.value == "0")
    {
        pollingReq = currentURL + "capture?startCapture=1";
    }
    else
    {
        pollingReq = currentURL + "capture?startCapture=0";
    }


//    console.log("Polling Request URL:"+pollingReq);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET",pollingReq, false ); // false for synchronous request
    xmlHttp.send(null);
    console.log("Response Text:"+xmlHttp.responseText);
    response = xmlHttp.responseText;

    if (response == "1")
    {
        btn.value="1";
        btn.innerHTML="Stop Recording";
    }
    else
    {
        btn.value="0";
        btn.innerHTML="Start Recording";
    }


}