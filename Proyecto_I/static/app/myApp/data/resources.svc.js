((function() {

    'use strict';

    /*@ngInject*/
    function ResourcesSvc(Resources) {
        var service = {};

        service.get = function(collection) {
            return Resources[collection];
        };

        service.set = function(collection, data) {
            Resources[collection] = data;
        };

        service.drop = function(collection) {
            if (Resources[collection]) {
                delete Resources[collection];
            }
        };

        service.isEmpty = function(collection) {
            return !Resources[collection];
        };

        service.add = function(collection,data) {
            if (Array.isArray(Resources[collection])) {
                Resources[collection].push(data);
            }
        };

        service.update = function(collection, data) {
            var set = Resources[collection];
            var i;

            for (i = 0; i < set.length; i++) {
                if (set[i]._id === data._id){
                    set[i] = data;
                }
            }
        };

        service.remove = function(collection, id) {
            var set = Resources[collection];
            var i;

            for (i = 0; i < set.length; i++) {
                if (set[i]._id === id){
                    set.splice(i,1);
                }
            }
        };


        return service;

    }

    angular
        .module('hiraApp.data')
        .factory('ResourcesSvc', ResourcesSvc);

})());