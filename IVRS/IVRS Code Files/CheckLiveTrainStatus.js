const axios = require('axios');

exports.handler = function(context, event, callback) {
  // Check if event object and the required properties exist
  if (event && event.trainNo) {
    const trainNo = event.trainNo.replace(/[|\u।\s]/g, ''); // Removes spaces, vertical bar, and Devanagari Danda from spoken PNR number
    
    const url = `https://irctc1.p.rapidapi.com/api/v1/liveTrainStatus`;

    const options = {
      method: 'GET',
      url: url,
      params: {
        trainNo: trainNo,
        startDay: '1'
      },
      headers: {
        'X-RapidAPI-Key': '1be3e190e5msh599033cddb5b637p14a752jsn092af95696fc',
        'X-RapidAPI-Host': 'irctc1.p.rapidapi.com'
      }
    };

    // Function to extract Type 1 and Type 2 information from API response
    function extractLocationInfo(responseData) {
      const currentLocationInfo = responseData.data && responseData.data.current_location_info ? responseData.data.current_location_info : [];
      
      let type1Info = 'Not Available';
      let type2Info = 'Not Available';
      
      // Check for Type 1 info
      if (currentLocationInfo.length > 0 && currentLocationInfo[0].readable_message) {
        type1Info = currentLocationInfo[0].readable_message;
      }
      
      // Check for Type 2 info
      if (currentLocationInfo.length > 1 && currentLocationInfo[1].readable_message) {
        type2Info = currentLocationInfo[1].readable_message;
      }

      return { type1: type1Info, type2: type2Info };
    }

    // Making the API request using Axios
    axios.request(options)
      .then(async response => {
        const responseData = response.data;
        const upcomingStations = responseData.data && responseData.data.upcoming_stations ? responseData.data.upcoming_stations : [];
        
        const firstStation = upcomingStations.length > 0 ? upcomingStations[0] : {};
        const firstStationName = firstStation.station_name || 'Not Available';
        const arrivalDelay = firstStation.arrival_delay || 'Not Available';
        const platformNumber = firstStation.platform_number || 'Not Available';
        const eta = firstStation.eta || 'Not Available';
        
        const locationInfo = extractLocationInfo(responseData);

        const message = `Your train number is ${trainNo || 'Not Available'} , ${locationInfo.type1} and ${locationInfo.type2}. Upcoming station is ${firstStationName} for which the current arrival delay is ${arrivalDelay} minutes and will reach the station by ${eta} on platform ${platformNumber}`;

        // Function to translate text using Microsoft Translator API
        async function translateText(text, toLanguage) {
          const translateUrl = 'https://microsoft-translator-text.p.rapidapi.com/translate';
          
          const translationOptions = {
            method: 'POST',
            url: translateUrl,
            params: {
              'to': toLanguage,
              'api-version': '3.0',
              profanityAction: 'NoAction',
              textType: 'plain'
            },
            headers: {
              'content-type': 'application/json',
              'X-RapidAPI-Key': 'fdddad6e9dmsh9ab0d76df71814ap171e54jsn45a373332045',
              'X-RapidAPI-Host': 'microsoft-translator-text.p.rapidapi.com'
            },
            data: [
              {
                Text: text
              }
            ]
          };
          
          try {
            const translationResponse = await axios.request(translationOptions);
            return translationResponse.data[0]?.translations[0]?.text || 'Translation failed';
          } catch (error) {
            console.error('Error translating text:', error);
            return 'Translation failed';
          }
        }

        const englishMessage = await translateText(message, 'en');
        const hindiMessage = await translateText(message, 'hi');    
        const marathiMessage = await translateText(message, 'mr');
        const tamilMessage = await translateText(message, 'ta');
        const germanMessage = await translateText(message, 'de');
        const frenchMessage = await translateText(message, 'fr');


        const responseObject = {
          trainNumber: trainNo || 'Not Available',
          type1Info: locationInfo.type1 || 'Not Available',
          type2Info: locationInfo.type2 || 'Not Available',
          firstStationName: firstStationName || 'Not Available',
          arrivalDelay: arrivalDelay || 'Not Available',
          platformNumber: platformNumber || 'Not Available',
          eta: eta || 'Not Available',
          englishMessage: englishMessage || 'Translation failed',
          hindiMessage: hindiMessage || 'Translation failed',
          marathiMessage: marathiMessage || 'Translation failed',
          tamilMessage: tamilMessage || 'Translation failed',
          germanMessage: germanMessage || 'Translation failed',
          frenchMessage: frenchMessage || 'Translation failed'
        };

        console.log('Fetched Data:', responseObject); // Log fetched data for verification
        return callback(null, responseObject); // Return the fetched data
      })
      .catch(error => {
        console.error('Error fetching live train status:', error);
        return callback(error); // Return an error
      });
  } 
  // else {
  //   console.error('PNR number (event.trainNo) is undefined or not available.');
  //   // Handle the case where event.trainNo is undefined or not available
  //   return callback('PNR number is missing');
  // }
};
