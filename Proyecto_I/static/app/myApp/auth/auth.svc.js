((function() {
    'use strict';

    /*@ngInject*/
    function Auth(common, $http, authToken, datacontext, $cookies) {
        var service = {};
        var $q = common.$q;
        var $state = common.$state;
        var currentUser = {};

        service.login = function(user) {
            var promise = datacontext.users.login(user);

            datacontext.users.login(user).then(function(res){
                currentUser = JSON.stringify(res);
                $cookies.put("user",currentUser);
            });

            return promise;
        };

        service.getCurrentUser = function(){
            if (service.isLoggedIn()){
                return JSON.parse($cookies.get("user"));
            } else {
                return {}
            }
        };

        service.isLoggedIn = function() {
            return !!($cookies.get("user"));
        };

        service.isLoggedInAsync = function(cb) {
            return cb(service.isLoggedIn());
        };

        service.logout = function() {
            $cookies.remove("user",currentUser);
            //authToken.removeToken();
            $state.reload();
        };

        service.createUser = function(user) {
            function promise(resolve, reject) {
                $http.post('/auth/register', user)
                    .success(function(res) {
                        authToken.setToken(res.token);
                        console.log(res);
                        resolve(res);
                    })
                    .error(function(err) {
                        service.logout();
                        reject(err);
                    });
            }

            return $q(promise);
            /*var promise = datacontext.users.create(user);

            return promise;*/
        };

        service.changePassword = function(oldPassword, newPassword) {
            console.log('Falta pasar el userId');

            function promise(resolve, reject) {
                $http.put('/api/users/changePassword', {
                        oldPassword: oldPassword,
                        newPassword: newPassword
                    })
                    .success(function(res) {
                        authToken.setToken(res.token);
                        resolve(res);
                    })
                    .error(function(err) {
                        service.logout();
                        reject(err);
                    });
            }

            return ($q(promise));
        };

        return service;
    }

    angular
        .module('hiraApp')
        .factory('Auth', Auth);
})());
