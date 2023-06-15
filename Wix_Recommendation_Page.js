import wixData from 'wix-data';
import { fetch } from 'wix-fetch';
// $w(`#name${i + 1}`).text = items[i].name;

function callPythonApi(context) {
    // The URL of your Python API
    
    const apiUrl = 'https://bd4b-216-165-95-161.ngrok-free.app/recommendation';
    for (let i = 0; i < 3; i++) {
                // Assuming you have elements with IDs like #name1, #price1, ...
                $w(`#name${i + 1}`).text = ""; // name
                //$w(`#name${i + 1}`).fontColor = "black";
                $w(`#price${i + 1}`).text = ""; // price
                //$w(`#price${i + 1}`).fontColor = "black";
            }
    // Make a POST request to your API with the context
    fetch(apiUrl, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context: context })
    })
    .then(response => response.json())
    .then(data => {
        // Access the array using the key "response"
        const apps = data.response;
        $w(`#text${42}`).text = "Most Recommended Apps";
        if (apps.length > 0) {
            const appName = apps[0].name;
            const appid = apps[0].appid;
            const steamStoreUrl = `https://store.steampowered.com/app/${appid}/`;
            $w("#image1").src = apps[0].header_image; // Set the src of image1 to header_image of the first app
            $w(`#name${1}`).text = appName;
            attachHyperlinkToText(appName, steamStoreUrl);
            $w(`#price${1}`).text = apps[0].price.toString();
        }
        if (apps.length > 1) {
            $w("#image2").src = apps[1].header_image; // Set the src of image2 to header_image of the second app
            $w(`#name${2}`).text = apps[1].name;
            $w(`#price${2}`).text = apps[1].price.toString();
        }

        // Check if at least 3 apps were fetched
        if (apps.length > 2) {
            $w("#image3").src = apps[2].header_image; // Set the src of image3 to header_image of the third app
            $w(`#name${3}`).text = apps[2].name;
            $w(`#price${3}`).text = apps[2].price.toString();
        }
        
    })
    .catch(err => {
        console.log('Error calling Python API:', err);
    });
    


}
function attachHyperlinkToText(appName, url) {
    // Select the text element by its ID
    const textElement = $w("#text1");

    // Set the text of the element to the app name
    textElement.text = appName;

    // Add a click event handler to the text element
    textElement.onClick(() => {
        // Open the URL in a new tab when the text is clicked
        wixLocation.to(url);
    });
}

$w.onReady(function () {
    // Fetch data from 'UserInput' collection
    wixData.query('UserInput')
        .limit(1) // We just want the first inputText
        .find()
        .then(res => {
            // Check if an item is found
            if (res.items.length > 0) {
                // Get the context from the first item
                const context = res.items[0].inputText;
                
                
                // Call Python API
                callPythonApi(context);
            } else {
                console.log('No items found in UserInput collection');
            }
        })
        .catch(err => {
            console.log('Error fetching data from UserInput:', err);
        });
});