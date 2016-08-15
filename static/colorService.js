window.addEventListener('DOMContentLoaded', yourFunction, false);
function colorTdAsPerParam(elem, param, val){
  val = parseInt(val);
  console.log("value received : "+val);
  if(param.toLowerCase() === "time"){
    $(elem).css("background-color", "#f4f4f4");
  } else if(param.toLowerCase() === "temperature"){
    $(elem).css("background-color", "#f4f4f4");
  } else if(param.toLowerCase() === "humidity"){
    $(elem).css("background-color", "#f4f4f4");
  } else if(param.toLowerCase() === "noise"){
    $(elem).css("background-color", "#f4f4f4");
  } else if(param.toLowerCase() === "aqi"){
    var colorVal = "#6ecc58";
    if(val < 51){
        colorVal = '#6ecc58';
    } else if (val > 50 && val < 101) {
        colorVal = '#bbcf4c';
    } else if (val > 100 && val < 201) {
        colorVal = '#eac736';
    } else if (val > 200 && val < 301) {
        colorVal = '#ed9a2e';
    } else if (val > 300 && val < 400) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "pm10"){
    var colorVal = "#6ecc58";
    if(val < 31){
        colorVal = '#6ecc58';
    } else if (val > 30 && val < 61) {
        colorVal = '#bbcf4c';
    } else if (val > 60 && val < 91) {
        colorVal = '#eac736';
    } else if (val > 90 && val < 121) {
        colorVal = '#ed9a2e';
    } else if (val > 120 && val < 251) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "pm2.5"){
    var colorVal = "#6ecc58";
    if(val < 51){
        colorVal = '#6ecc58';
    } else if (val > 50 && val < 101) {
        colorVal = '#bbcf4c';
    } else if (val > 100 && val < 251) {
        colorVal = '#eac736';
    } else if (val > 250 && val < 351) {
        colorVal = '#ed9a2e';
    } else if (val > 350 && val < 431) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "co2"){
    var colorVal = "#6ecc58";
    if(val < 351){
        colorVal = '#6ecc58';
    } else if (val > 350 && val < 1001) {
        colorVal = '#bbcf4c';
    } else if (val > 1000 && val < 2001) {
        colorVal = '#eac736';
    } else if (val > 2000 && val < 5001) {
        colorVal = '#ed9a2e';
    } else if (val > 5000 && val < 40000) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    if(isNaN(val)){
      colorVal = "#f4f4f4";
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "co"){
    var colorVal = "#6ecc58";
    if(val < 1.1){
        colorVal = '#6ecc58';
    } else if (val > 1.0 && val < 2.1) {
        colorVal = '#bbcf4c';
    } else if (val > 2.0 && val < 10.1) {
        colorVal = '#eac736';
    } else if (val > 10 && val < 17.1) {
        colorVal = '#ed9a2e';
    } else if (val > 17 && val < 34.1) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    if(isNaN(val)){
      colorVal = "#f4f4f4";
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "no2"){
    var colorVal = "#6ecc58";
    if(val < 41){
        colorVal = '#6ecc58';
    } else if (val > 40 && val < 81) {
        colorVal = '#bbcf4c';
    } else if (val > 80 && val < 181) {
        colorVal = '#eac736';
    } else if (val > 180 && val < 281) {
        colorVal = '#ed9a2e';
    } else if (val > 280 && val < 401) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    if(isNaN(val)){
      colorVal = "#f4f4f4";
    }
    $(elem).css("background-color", colorVal);
  } else if(param.toLowerCase() === "nh3"){
    var colorVal = "#6ecc58";
    if(val < 201){
        colorVal = '#6ecc58';
    } else if (val > 200 && val < 401) {
        colorVal = '#bbcf4c';
    } else if (val > 400 && val < 801) {
        colorVal = '#eac736';
    } else if (val > 800 && val < 1201) {
        colorVal = '#ed9a2e';
    } else if (val > 1200 && val < 1801) {
        colorVal = '#e8633a';
    } else {
        colorVal = '#d63636';
    }
    if(isNaN(val)){
      colorVal = "#f4f4f4";
    }
    $(elem).css("background-color", colorVal);
  }
}


function yourFunction() {
    var tables = document.getElementsByTagName("table");
    var elementsTd = tables[0].getElementsByTagName("td");
    var colHeads = document.getElementsByTagName("th");
    var headsCount = colHeads.length;
    var lengthOfArray = elementsTd.length;
    for(var i=0; i<headsCount; i++){
      console.log("came here with param : "+colHeads[i].innerHTML);
    }
    for(var i=0; i<lengthOfArray; i++){
      var moduleValue = ((i+1)%(headsCount));
      if(moduleValue == 0){
        var stringArray = colHeads[headsCount-1].innerHTML.split("<");
        var paramName = stringArray[0];
        console.log("sending param Name : "+paramName);
        colorTdAsPerParam(elementsTd[i], paramName, elementsTd[i].innerHTML);
      } else {
        var stringArray = colHeads[moduleValue-1].innerHTML.split("<");
        var paramName = stringArray[0];
        console.log("sending param Name 2 : "+paramName);
        colorTdAsPerParam(elementsTd[i], paramName, elementsTd[i].innerHTML);
      }
      
    }      
}
