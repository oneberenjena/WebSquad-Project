((function() {

    'use strict';

    /*@ngInject*/
    function serverMessage(common) {

        function getAttrs(data) {
            var attrs = [];
            var key, i, item;

            for (key in data) {
                if ((key === 'filter') && (!common.isEmpty(data[key]))) {
                    attrs.push({
                        key: key,
                        val: data[key]
                    });
                } else if ((key !== 'collection') && (key !== 'manager') && (data[key] !== 'null')) {
                    attrs.push({
                        key: key,
                        val: data[key]
                    });
                }
            }

            return attrs;
        }

        function addFilter(data) {
            var key, i, item, j;

            data = getAttrs(data);

            var route = '';

            for (i = 0; i < data.length; i += 1) {
                if (i !== 0) {
                    route += '&&';
                } else {
                    route += '?';
                }

                if (data[i].key === 'filter') {
                    for (j = 0; j < data[i].val.length; j++) {
                        item = data[i].val[j];
                        route += item.key + '=' + item.value;
                        if (j < data[i].val.length - 1) {
                            route += '&&';
                        }
                    }
                } else {
                    route += data[i].key + '=' + data[i].val;
                }
            }

            return route;
        }

        /*DEFINITON OF VARIABLES*/
        var service = {};

        /*PUBLIC FUNCTIONS*/
        service.getReq = function(routeType, data) {
            var route = 'api';

            if (data.collection === 'null') {
                console.log('You gotta have a collection [function use()]');
                return 'ERROR';
            }

            if (data.manager === 'null') {
                console.log('You gotta have a manager [function use()]');
                return 'ERROR';
            }

            route += '/' + data.collection;

            if (routeType) {
                route += '/' + routeType;
            }

            route += addFilter(data);

            return route;
        };


        return service;

    }

    angular
        .module('hiraApp.data')
        .factory('serverMessage', serverMessage);

})());