((function () {

    'use strict';

    /*@ngInject*/
    function metaData() {
        var service = {};
        var entities = {};

        /*PUBLIC FUNCTIONS*/
        service.entities = entities;

        service.getManager = function () {
            return entities;
        };

        service.hasItems = function (entity) {
            return entities.hasOwnProperty(entity);
        };

        service.init = function (data) {
            entities = data;
        };

        service.getCollections = function () {
            var collections = [];

            var key;

            for (key in entities) {
                if (key !== 'users' && key !== 'blocks' && key !== 'buttons' &&
                        key !== 'lists' && key !== 'forms') {
                    collections.push({name: key});
                }
            }

            return collections;
        };

        service.pushToEntity = function (entity, data) {
            var i;

            for (i = 0; i < data.length; i += 1) {
                entities[entity].push(data[i]);
            }
        };

        service.getEntity = function (entity) {
            return entities[entity];
        };

        return service;
    }

    angular
        .module('hiraApp.data')
        .factory('metaData', metaData);
})());