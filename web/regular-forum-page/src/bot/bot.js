var steps = [];
var testindex = 0;
var loadInProgress = false;//This is set to true when a page is still loading

/*********SETTINGS*********************/
var system = require('system');
var env = system.env;
var webPage = require('webpage');
var page = webPage.create();
page.settings.userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36';
page.settings.javascriptEnabled = true;
page.settings.loadImages = true;//Script is much faster with this field set to false
phantom.cookiesEnabled = true;
phantom.javascriptEnabled = true;
if (env["DOMAIN"] === null) {
    domain = "127.0.0.1";
} else {
    domain = env["DOMAIN"];
}
if (env["PORT"] === null) {
    port = "8000";
} else {
    port = env["DOMAIN"];
}
url = "http://" + domain + ':' + env['PORT'] + "/";

phantom.addCookie({
    'name': 'flag',
    'value': 'COMPFEST13{html_t4g_1s_n0t_C4s3_5ent1t1v3_5bc733a9f8}',
    'domain': domain,
    'path': '/',
    'httponly': false
});
/*********SETTINGS END*****************/

for (var i in phantom.cookies) {
    console.log(phantom.cookies[i].name + '=' + phantom.cookies[i].value);
}

console.log('All settings loaded, start with execution');
page.onConsoleMessage = function (msg) {
    console.log(msg);
};
/**********DEFINE STEPS THAT FANTOM SHOULD DO***********************/
steps = [

    //Step 1 - Login Page
    function () {
        page.open(url + "login", function (status) { });
    },
    //Step 2 - Login Credentials
    function () {
        page.evaluate(function () {
            document.getElementsByName("username")[0].value = "Moderator";
            document.getElementsByName("password")[0].value = "PeopleShouldn'tknowth1s";
            document.getElementsByTagName("button")[0].click();
        });
    },
    //Step 3 - viewing forum
    function () {
        page.evaluate(function () {
            document.getElementsByTagName("a")[3].click()
        })
    },
    //Step 4 - Logout
    function () {
        page.open(url + "logout", function (status) { });
    },
];
/**********END STEPS THAT FANTOM SHOULD DO***********************/

//Execute steps one by one
interval = setInterval(executeRequestsStepByStep, 500);

function executeRequestsStepByStep() {
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
page.onLoadStarted = function () {
    loadInProgress = true;
    //console.log('Request started');
};
page.onLoadFinished = function () {
    loadInProgress = false;
    //console.log('Request finished');
};
page.onResourceReceived = function (response) {
    if (response.status !== 200 && response.status !== 302 && response.status !== 304) {
        console.log('[ERROR] Loading page failed: ' + response.status + ' - ' + response.statusText);
    }
};
page.onConsoleMessage = function (msg) {
    //console.log(msg);
};
page.onNavigationRequested = function (url, type, willNavigate, main) {
    //console.log("[URL] URL="+url);  
};