((function () {
    'use strict';

    /*@ngInject*/
    function serverSpeaker(common, serverMessage) {
        /*jshint validthis:true */
        var $http = common.$http;

        var filtersHelper = {
            greaterThan: 'null',
            lessThan: 'null',
            sort: 'null',
            filter: [],
            size: 'null',
            searchTerm: 'null',
            collection: 'null',
            manager: 'null'
        };

        /*PRIVATE FUNCTIONS*/
        function clearFilter() {
            var key;

            for (key in filtersHelper) {
                if (key === 'filter') {
                    filtersHelper[key] = [];
                } else {
                    filtersHelper[key] = 'null';
                }
            }
        }

        /*DEFINITION OF VARIABLES*/
        var service = {};

        /*PUBLIC FUNCTIONS*/
        service.use = function (collect) {
            if (collect) {
                filtersHelper.collection = collect;
            }

            return this;
        };

        service.greaterThan = function (id) {
            if (id) {
                filtersHelper.greaterThan = id;
            }

            return this;
        };

        service.lessThan = function (id) {
            if (id) {
                filtersHelper.lessThan = id;
            }

            return this;
        };

        service.sort = function (attr) {
            if (attr) {
                filtersHelper.sort = attr;
            }

            return this;
        };

        service.size = function (number) {
            if (number) {
                filtersHelper.size = number;
            }

            return this;
        };

        service.searchTerm = function (term) {
            if (term) {
                filtersHelper.searchTerm = term;
            }

            return this;
        };

        service.filter = function (data) {
            if (data) {
                filtersHelper.filter = data;
            }

            return this;
        };

        service.manager = function (manager) {
            if (manager) {
                filtersHelper.manager = manager;
            }

            return this;
        };

        service.execute = function (route) {
            var req = serverMessage.getReq(route, filtersHelper);

            clearFilter();

            return $http.get(req);
        };


        return service;
    }

    angular
        .module('hiraApp.data')
        .factory('serverSpeaker', serverSpeaker);

})());
