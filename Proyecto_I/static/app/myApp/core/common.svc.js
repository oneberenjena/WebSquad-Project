((function () {
    'use strict';

    /* @ngInject */
    function common($location, $compile, $q, $rootScope, $timeout, $http, $state, $stateParams, $window, $log) {
        var service = {};

        service.$broadcast = function () {
            return $rootScope.$broadcast.apply($rootScope, arguments);
        };

        service.isNumber = function (val) {
            // negative or positive
            return (/^[-]?\d+$/).test(val);
        };

        service.textContains = function (text, searchText) {
            return text && -1 !== text.toLowerCase().indexOf(searchText.toLowerCase());
        };

        service.toggleAddArray = function (array, item) {
            var index = array.indexOf(item);

            if (index >= 0) {
                array.splice(index, 1);
            } else {
                array.push(item);
            }

            return array;
        };

        service.removeFromArray = function (array, item) {
            var index = array.indexOf(item);

            if (index >= 0) {
                array.splice(index, 1);
            }

            return array;
        };

        service.isEmpty = function (obj) {
            var prop;

            for (prop in obj) {
                if (obj.hasOwnProperty(prop)) {
                    return false;
                }
            }

            return true;
        };

        /*jshint -W001 */
        service.$q = $q;
        service.$log = $log;
        service.$compile = $compile;
        service.$state = $state;
        service.$stateParams = $stateParams;
        service.$http = $http;
        service.$timeout = $timeout;
        service.$rootScope = $rootScope;
        service.$location = $location;
        service.$window = $window;

        return service;
    }

    angular
        .module('hiraApp.core')
        .factory('common', common);

})());