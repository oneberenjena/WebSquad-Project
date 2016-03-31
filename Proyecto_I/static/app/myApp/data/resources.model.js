((function() {

    'use strict';

    /*@ngInject*/
    function Resources() {
        var collections = {};

        return collections;
    }

    angular
        .module('hiraApp.data')
        .factory('Resources', Resources);

})());
