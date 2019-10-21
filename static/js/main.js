function startRecording()
{
    console.log("Polling");
    console.log("Current Url:"+document.URL);

    currentURL = document.URL;
    pollingReq = currentURL + "poll";

    console.log("Polling Request URL:"+pollingReq);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET",pollingReq, false ); // false for synchronous request
    xmlHttp.send(null);
    console.log("Response Text:"+xmlHttp.responseText);
}