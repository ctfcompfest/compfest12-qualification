var steps=[];
var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading

/*********SETTINGS*********************/
var system = require('system');
var env = system.env;
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
page.settings.javascriptEnabled = true;
page.settings.loadImages = true;//Script is much faster with this field set to false
page.settings.webSecurityEnabled = false;
page.settings.localToRemoteUrlAccessEnabled = true;
page.settings.navigationLocked = false;
phantom.cookiesEnabled = true;
phantom.javascriptEnabled = true;
if (env["DOMAIN"] === null) {
    domain = "127.0.0.1:8080";
} else {
    domain = env["DOMAIN"];
}
url = "http://" + domain + '/';

/*********SETTINGS END*****************/

console.log('All settings loaded, start with execution');
page.onConsoleMessage = function(msg) {
    console.log(msg);
};
/**********DEFINE STEPS THAT FANTOM SHOULD DO***********************/
steps = [

    //Step 1 - Login Page
    function(){
        page.open(url+"login", function(status){});
    },
    //Step 2 - Login Credentials
    function(){
        page.evaluate(function(){
            document.getElementsByName("username")[0].value = "abcdef";
            document.getElementsByName("password")[0].value = "6fjvyW7pLjU2&062@N0d@M%T*";
            document.getElementsByTagName("button")[0].click();
        });
    },
    //Step 3 - Logout
    function(){
        page.open(url+"logout", function(status){});       
    },
];
/**********END STEPS THAT FANTOM SHOULD DO***********************/

//Execute steps one by one
interval = setInterval(executeRequestsStepByStep, 5000);

function executeRequestsStepByStep(){
    if (loadInProgress == false && typeof steps[testindex] == "function") {
        //console.log("step " + (testindex + 1));
        steps[testindex]();
        testindex++;

        if (typeof steps[testindex] != "function") {
            testindex = 0;
        }
    }
}

/**
 * These listeners are very important in order to phantom work properly. Using these listeners, we control loadInProgress marker which controls, weather a page is fully loaded.
 * Without this, we will get content of the page, even a page is not fully loaded.
 */
page.onLoadStarted = function() {
    loadInProgress = true;
    // console.log('Request started');
};
page.onLoadFinished = function() {
    loadInProgress = false;
    // console.log('Request finished');
};
page.onResourceReceived = function(response) {
    if (response.status !== 200 && response.status !== 302 && response.status !== 304) {
        console.log('[ERROR] Loading page failed: ' +  response.status + ' - ' + response.statusText);
    }
};
page.onConsoleMessage = function(msg) {
    console.log(msg);
};
page.onNavigationRequested = function(url, type, willNavigate, main) {
    console.log("[URL] URL="+url); 
};