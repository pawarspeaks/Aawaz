const axios = require('axios');

exports.handler = async function (context, event, callback) {
  // const pnrnumber = event.pnrnumber.replace(/\s/g, ''); // Remove spaces from spoken PNR number
const pnrnumber = event.pnrnumber.replace(/[|\u।\s]/g, ''); // Remove spaces, vertical bar, and Devanagari Danda from spoken PNR number                        

  const apiKey = context.PNR_API_KEY_iampratappawar; // Retrieve API key from environment variable
  const pnrCheckUrl = `https://pnr-status-indian-railway.p.rapidapi.com/pnr-check/${pnrnumber}`;
  const translateUrl = 'https://microsoft-translator-text.p.rapidapi.com/translate';

 const hindiTranslationOptions = {
    method: 'POST',
    url: translateUrl,
    params: {
      'to': 'hi',
      'api-version': '3.0', 
      profanityAction: 'NoAction',
      textType: 'plain'
    },
    headers: {
      'content-type': 'application/json',
      'X-RapidAPI-Key': 'fdddad6e9dmsh9ab0d76df71814ap171e54jsn45a373332045', // Replace with your Translator API key
      'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    },
    data: [
      {
        Text: '' // Placeholder for English text to be translated
      }
    ]
  };

  // Configuring the Microsoft Translator API request for Tamil translation
  const tamilTranslationOptions = {
    method: 'POST',
    url: translateUrl,
    params: {
      'to': 'ta',
      'api-version': '3.0',
      profanityAction: 'NoAction',
      textType: 'plain'
    },
    headers: {
      'content-type': 'application/json',
      'X-RapidAPI-Key': 'fdddad6e9dmsh9ab0d76df71814ap171e54jsn45a373332045', // Replace with your Translator API key
      'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    },
    data: [
      {
        Text: '' // Placeholder for English text to be translated
      }
    ]
  };

  const germanTranslationOptions = {
    method: 'POST',
    url: translateUrl,
    params: {
      'to': 'de', // Language code for German
      'api-version': '3.0',
      profanityAction: 'NoAction',
      textType: 'plain'
    },
    headers: {
      'content-type': 'application/json',
      'X-RapidAPI-Key': 'fdddad6e9dmsh9ab0d76df71814ap171e54jsn45a373332045', // Replace with your Translator API key
      'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    },
    data: [
      {
        Text: '' // Placeholder for English text to be translated
      }
    ]
  };

  // Configuring the Microsoft Translator API request for French translation
  const frenchTranslationOptions = {
    method: 'POST',
    url: translateUrl,
    params: {
      'to': 'fr',
      'api-version': '3.0',
      profanityAction: 'NoAction',
      textType: 'plain'
    },
    headers: {
      'content-type': 'application/json',
      'X-RapidAPI-Key': 'fdddad6e9dmsh9ab0d76df71814ap171e54jsn45a373332045', // Replace with your Translator API key
      'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
    },
    data: [
      {
        Text: '' // Placeholder for English text to be translated
      }
    ]
  };

  try {
    // Fetching PNR status from Indian Railways API using Axios
    const pnrResponse = await axios.get(pnrCheckUrl, {
      headers: {
        'X-RapidAPI-Key': '1be3e190e5msh599033cddb5b637p14a752jsn092af95696fc', // Replace with your RapidAPI key
        'X-RapidAPI-Host': 'pnr-status-indian-railway.p.rapidapi.com'
      }
    });

    const responseData = pnrResponse.data;
    const trainInfo = responseData.data?.trainInfo || {};
    const passengerInfo = responseData.data?.passengerInfo || [];
    const boardingInfo = responseData.data?.boardingInfo || {};

    let passengersMessage = '';

    if (passengerInfo.length > 0) {
      passengersMessage = passengerInfo.map(passenger => {
        return `Passenger: Coach - ${passenger.currentCoach}, Berth - ${passenger.currentBerthNo}`;
      }).join('\n');
    } else {
      passengersMessage = 'No passenger information available';
    }

    const englishMessage = `Your train is ${trainInfo.trainNo || 'N/A'} ${trainInfo.name || 'N/A'}. You will board at ${boardingInfo.stationName || 'N/A'}. Passenger details are as follows:\n${passengersMessage}\nThank you`;

    // Update the English text in the translation requests
    hindiTranslationOptions.data[0].Text = englishMessage;
    tamilTranslationOptions.data[0].Text = englishMessage;
    germanTranslationOptions.data[0].Text = englishMessage; // Update for German translation
    frenchTranslationOptions.data[0].Text = englishMessage; // Update for French translation

    // Use the Microsoft Translator API for Hindi translation
    const hindiTranslationResponse = await axios.request(hindiTranslationOptions);
    const hindiMessage = hindiTranslationResponse.data[0]?.translations[0]?.text || 'Translation failed';

    // Use the Microsoft Translator API for Tamil translation
    const tamilTranslationResponse = await axios.request(tamilTranslationOptions);
    const tamilMessage = tamilTranslationResponse.data[0]?.translations[0]?.text || 'Translation failed';

    // Use the Microsoft Translator API for German translation
    const germanTranslationResponse = await axios.request(germanTranslationOptions);
    const germanMessage = germanTranslationResponse.data[0]?.translations[0]?.text || 'Translation failed';

    
    // Use the Microsoft Translator API for French translation
    const frenchTranslationResponse = await axios.request(frenchTranslationOptions);
    const frenchMessage = frenchTranslationResponse.data[0]?.translations[0]?.text || 'Translation failed';

    const responseObject = {
      pnrnumber: pnrnumber,
      status: responseData.status,
      trainNumber: trainInfo.trainNo || 'N/A',
      boardingStation: boardingInfo.stationName || 'N/A',
      englishMessage: englishMessage, // Original English message
      hindiMessage: hindiMessage, // Translated Hindi message
      tamilMessage: tamilMessage, // Translated Tamil message
      germanMessage: germanMessage, // Translated German message
      frenchMessage: frenchMessage // Translated French message

    };

    console.log('Fetched Data:', responseObject); // Log fetched data for verification
    return callback(null, responseObject); // Return the fetched data
  } catch (error) {
    console.error('Error:', error);
    return callback(error); // Return an error
  }
}
