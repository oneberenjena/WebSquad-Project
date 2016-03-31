((function () {
    'use strict';

    /*@ngInject*/
    function authToken(localStorageService) {
        var service = {};
        var storage = localStorageService;
        var cachedToken;
        var userToken = 'token';

        /*PUBLIC FUNCTIONS*/
        service.setToken = function (token) {
            cachedToken = token;
            storage.set(userToken, token);
        };

        service.getToken = function () {
            if (!cachedToken) {
                return storage.get(userToken);
            }

            return cachedToken;
        };

        service.isAuthenticated = function () {
            return !!service.getToken();
        };

        service.removeToken = function () {
            cachedToken = null;
            storage.remove(userToken);
            userToken = 'token';
        };

        return service;
    }

    angular
        .module('hiraApp')
        .factory('authToken', authToken);
})());