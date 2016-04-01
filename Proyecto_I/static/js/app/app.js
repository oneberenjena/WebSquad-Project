// Creación del módulo de la aplicación
var socialModule = angular.module('social', ['ngRoute', 'ngStorage', 'ngAnimate', 'ngTable', 'emoji', 'textAngular', 'ngDialog', 'ngSanitize', 'flash','btford.socket-io','ngMaterial']);
socialModule.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/', {
                controller: 'VLoginController',
                templateUrl: 'app/ident/VLogin.html'
            });
}]);

socialModule.controller('socialController_',  ['$scope', '$localStorage', '$http', '$location',
function($scope, $localStorage, $http, $location) {
    $scope.title = "Social";
    $scope.$storage = $localStorage;
    $scope.VForos3 = function(idUsuario) {
        $location.path('/VForos/'+idUsuario);
    };
    $scope.VPrincipal0 = function() {
        $location.path('/VPrincipal');
      };
    $scope.VLogin0 = function() {
        $location.path('/VLogin');
    };
    $scope.VPagina1 = function(idUsuario) {
        $location.path('/VPagina/'+idUsuario);
    };
    $scope.VMiPagina = function(idUsuario) {
        $location.path('/VMiPagina/'+idUsuario);
    };
    $scope.VContactos2 = function(idUsuario) {
        $location.path('/VContactos/'+idUsuario);
    };
}]);
socialModule.directive('sameAs', [function () {
    return {
        restrict: 'A',
        scope:true,
        require: 'ngModel',
        link: function (scope, elem , attrs, control) {
            var checker = function () {
                //get the value of the this field
                var e1 = scope.$eval(attrs.ngModel); 
 
                //get the value of the other field
                var e2 = scope.$eval(attrs.sameAs);
                return e1 == e2;
            };
            scope.$watch(checker, function (n) {
 
                //set the form control to valid if both 
                //fields are the same, else invalid
                control.$setValidity("unique", n);
            });
        }
    };
}]);
