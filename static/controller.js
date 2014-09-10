'use strict';

angular.module('gutenrecsApp', ['ui.bootstrap', 'ngRoute' ])
    .controller('MyController', ['$scope', '$http',
        function($scope, $http) {
            $scope.bookchoice = "";
            $scope.CSVToArray = function(strData, strDelimiter) {
                // Check to see if the delimiter is defined. If not,
                // then default to comma.
                strDelimiter = (strDelimiter || ",");
                // Create a regular expression to parse the CSV values.
                var objPattern = new RegExp((
                    // Delimiters.
                    "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +
                    // Quoted fields.
                    "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
                    // Standard fields.
                    "([^\"\\" + strDelimiter + "\\r\\n]*))"), "gi");
                // Create an array to hold our data. Give the array
                // a default empty first row.
                var arrData = [
                    []
                ];
                // Create an array to hold our individual pattern
                // matching groups.
                var arrMatches = null;
                // Keep looping over the regular expression matches
                // until we can no longer find a match.
                while (arrMatches = objPattern.exec(strData)) {
                    // Get the delimiter that was found.
                    var strMatchedDelimiter = arrMatches[1];
                    // Check to see if the given delimiter has a length
                    // (is not the start of string) and if it matches
                    // field delimiter. If id does not, then we know
                    // that this delimiter is a row delimiter.
                    if (strMatchedDelimiter.length && (strMatchedDelimiter != strDelimiter)) {
                        // Since we have reached a new row of data,
                        // add an empty row to our data array.
                        arrData.push([]);
                    }
                    // Now that we have our delimiter out of the way,
                    // let's check to see which kind of value we
                    // captured (quoted or unquoted).
                    if (arrMatches[2]) {
                        // We found a quoted value. When we capture
                        // this value, unescape any double quotes.
                        var strMatchedValue = arrMatches[2].replace(
                            new RegExp("\"\"", "g"), "\"");
                    } else {
                        // We found a non-quoted value.
                        var strMatchedValue = arrMatches[3];
                    }
                    // Now that we have our value string, let's add
                    // it to the data array.
                    arrData[arrData.length - 1].push(strMatchedValue);
                }
                // Return the parsed data.
                return (arrData);
            }

            $scope.CSV2JSON = function(csv) {
                var array = $scope.CSVToArray(csv);
                var objArray = [];
                for (var i = 1; i < array.length; i++) {
                    objArray[i - 1] = {};
                    for (var k = 0; k < array[0].length && k < array[i].length; k++) {
                        var key = array[0][k];
                        objArray[i - 1][key] = array[i][k]
                    }
                }

                var json = JSON.stringify(objArray);
                var str = json.replace(/},/g, "},\r\n");

                return str;
            }
            
            $scope.getBooks = function(partial){
                return $http.get('/getbooks/'+partial, {
                    //params: {
                    //    text: partial
                    //}
                }
                ).then(function(response){
                    var books = [];
                    //console.log(response.data.data)
                    angular.forEach(response.data.data, function(item){
                        books.push(item);
                    });
                    //console.log(books);
                    return books;
                });
            };

            $scope.searchBook = function(bookid){
                //return $http.get('/searchbook/'+bookid);
                alert("searching book " +bookid);
                var bookid = $scope.bookchoice.id;
                window.location.href = '/searchbook/'+bookid;
            };

            //$http.get('/getbooks/').success(function(response) {
            //    $scope.books = $scope.CSV2JSON(response);
            //});

            //alert($scope.books);
    }
    ]);