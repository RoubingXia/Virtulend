import wixData from 'wix-data';
import { fetch } from 'wix-fetch';
// $w(`#name${i + 1}`).text = items[i].name;
function callPythonApi(context) {
    // The URL of your Python API
    
    const apiUrl = 'https://fd8b-2600-4041-44c4-7300-509-656a-1305-ddc2.ngrok-free.app/recommendation';
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
        const array = data.response;

        // Check if the array has at least 1 element
        if (array && array.length >= 3) {
            // Display the first element on the page
            for (let i = 0; i < 3; i++) {
                // Assuming you have elements with IDs like #name1, #price1, ...
                $w(`#name${i + 1}`).text = array[i][0]; // name
                $w(`#name${i + 1}`).fontColor = "black";
                $w(`#price${i + 1}`).text = array[i][1].toString(); // price
                $w(`#price${i + 1}`).fontColor = "black";
            }
            $w(`#text${42}`).text = "Most Recommended Apps";
        } else {
            for (let i = 0; i < array.length; i++) {
                // Assuming you have elements with IDs like #name1, #price1, ...
                $w(`#name${i + 1}`).text = array[i][0]; // name
                $w(`#price${i + 1}`).text = array[i][1].toString(); // price
            }
            for(let j=array.length; j<3;j++){
                $w(`#name${j + 1}`).text = " "; // name
                $w(`#price${j + 1}`).text = " "; // price
            }
        }
    })
    .catch(err => {
        console.log('Error calling Python API:', err);
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