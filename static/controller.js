'use strict';

angular.module('gutenrecsApp', ['ui.bootstrap', 'ngRoute' ])
    .controller('MyController', ['$scope', '$http',
        function($scope, $http) {
            $scope.bookchoice = "";   
            
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

            $scope.searchBook = function(){
                //return $http.get('/searchbook/'+bookid);
                var bookid = $scope.bookchoice;
                //alert("searching book " +bookid);
                window.location.href = '/searchbook/'+bookid;
            };

    }
    ]);